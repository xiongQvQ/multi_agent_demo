from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage


class AnalystAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {tool.name: tool for tool in tools}
        self.name = "Analyst"
        self.role = "Data analysis and calculation specialist"
    
    def execute(self, user_query: str, state: dict) -> dict:
        """Execute analyst tasks - analyze data and perform calculations"""
        
        # System prompt for the analyst
        system_prompt = """
        You are an Analysis Agent specialized in data analysis and calculations.
        Your role is to analyze the information provided by the researcher and perform relevant calculations.
        
        Available tools:
        - calculator: Use this for mathematical calculations and financial analysis
        
        Your task is to:
        1. Review the research findings
        2. Identify what calculations or analysis are needed
        3. Use the calculator tool for numerical analysis
        4. Provide insights based on your analysis
        
        Be analytical and focus on quantitative insights.
        """
        
        research_findings = state.get("research_findings", "")
        research_summary = state.get("research_summary", "")
        
        # Determine what calculations to perform
        calc_request = self._identify_calculations(user_query, research_findings)
        
        # Use calculator tool
        calc_tool = self.tools.get("calculator")
        if calc_tool and calc_request:
            calculation_results = calc_tool._run(calc_request)
        else:
            calculation_results = "No specific calculations needed based on available data"
        
        # Generate analysis
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
            User Query: {user_query}
            Research Findings: {research_findings}
            Research Summary: {research_summary}
            Calculation Results: {calculation_results}
            
            Please provide analytical insights and identify key metrics or trends.
            """)
        ]
        
        response = self.llm.invoke(messages)
        
        # Update state with analysis results
        state["calculation_results"] = calculation_results
        state["analysis_insights"] = response.content
        state["current_agent"] = "analyst"
        
        return state
    
    def _identify_calculations(self, query: str, research_data: str) -> str:
        """Identify what calculations should be performed"""
        calculations = []
        
        query_lower = query.lower()
        data_lower = research_data.lower()
        
        # Extract numbers from research data
        import re
        numbers = re.findall(r'\d+\.?\d*', research_data)
        
        # Look for specific financial calculations
        if "p/e" in query_lower or "pe ratio" in query_lower or "p/e" in data_lower:
            if len(numbers) >= 2:
                calculations.append(f"P/E ratio calculation with values {numbers[0]} {numbers[1]}")
            else:
                calculations.append("P/E ratio analysis")
        
        if "percentage" in query_lower or "change" in query_lower or "%" in data_lower:
            if len(numbers) >= 2:
                calculations.append(f"percentage change calculation {numbers[0]} {numbers[1]}")
            else:
                calculations.append("percentage change calculation")
        
        if "market cap" in query_lower or "valuation" in query_lower:
            if len(numbers) >= 2:
                calculations.append(f"market cap calculation {numbers[0]} {numbers[1]}")
            else:
                calculations.append("market cap analysis")
        
        # If we have numbers but no specific calculation type, do general analysis
        if numbers and not calculations:
            calculations.append(f"analysis of values: {', '.join(numbers[:5])}")
        
        # Default analysis if no specific calculations identified
        if not calculations:
            calculations.append("general financial analysis of available data")
        
        return "; ".join(calculations)