from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage


class ResearcherAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.name = "Researcher"
        self.role = "Information gatherer and web search specialist"
    
    def execute(self, user_query: str, state: dict) -> dict:
        """Execute researcher tasks - primarily search for information"""
        
        # System prompt for the researcher
        system_prompt = """
        You are a Research Agent specialized in gathering information.
        Your role is to search for relevant information to answer the user's query.
        
        Available tools:
        - search: Use this to find information about the topic
        
        Your task is to:
        1. Identify what information needs to be searched
        2. Use the search tool to gather relevant data
        3. Summarize your findings for the next agent
        
        Be thorough but concise in your research.
        """
        
        # Determine what to search for
        search_query = self._extract_search_terms(user_query)
        
        # Use search tool
        search_tool = self.tools.get("search")
        if search_tool:
            search_results = search_tool._run(search_query)
        else:
            search_results = "Search tool not available"
        
        # Generate research summary
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            User Query: {user_query}
            Search Results: {search_results}
            
            Please summarize the key information found and what should be analyzed next.
            """)
        ]
        
        response = self.llm.invoke(messages)
        
        # Update state with research findings
        state["research_findings"] = search_results
        state["research_summary"] = response.content
        state["current_agent"] = "researcher"
        
        return state
    
    def _extract_search_terms(self, query: str) -> str:
        """Extract relevant search terms from user query"""
        # Simple keyword extraction - in production, use more sophisticated NLP
        keywords = []
        
        # Look for company names, stock symbols, financial terms
        financial_terms = ["stock", "price", "performance", "analysis", "market", "earnings", "revenue"]
        company_indicators = ["apple", "microsoft", "google", "amazon", "tesla", "meta", "netflix"]
        
        query_lower = query.lower()
        
        for term in financial_terms:
            if term in query_lower:
                keywords.append(term)
        
        for company in company_indicators:
            if company in query_lower:
                keywords.append(company)
        
        return " ".join(keywords) if keywords else query