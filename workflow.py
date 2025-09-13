from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
from agents.reporter import ReporterAgent
from tools.search_tool import SearchTool
from tools.calc_tool import CalculatorTool
from tools.file_tool import FileTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MultiAgentWorkflow:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Initialize tools
        self.tools = [
            SearchTool(),
            CalculatorTool(),
            FileTool()
        ]
        
        # Initialize agents
        self.researcher = ResearcherAgent(self.llm, self.tools)
        self.analyst = AnalystAgent(self.llm, self.tools)
        self.reporter = ReporterAgent(self.llm, self.tools)
        
        # Build workflow graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Define the state structure
        workflow = StateGraph(dict)
        
        # Add nodes for each agent
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("analyst", self._analyst_node)
        workflow.add_node("reporter", self._reporter_node)
        
        # Define the workflow edges (sequential execution)
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "analyst")
        workflow.add_edge("analyst", "reporter")
        workflow.add_edge("reporter", END)
        
        return workflow.compile()
    
    def _researcher_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Researcher agent node"""
        user_query = state.get("user_query", "")
        print(f"🔍 Researcher Agent: Searching for information about '{user_query}'...")
        
        updated_state = self.researcher.execute(user_query, state)
        
        print(f"✅ Research completed. Found: {updated_state.get('research_summary', 'No summary')[:100]}...")
        return updated_state
    
    def _analyst_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyst agent node"""
        user_query = state.get("user_query", "")
        print(f"📊 Analyst Agent: Analyzing data and performing calculations...")
        
        updated_state = self.analyst.execute(user_query, state)
        
        print(f"✅ Analysis completed. Insights: {updated_state.get('analysis_insights', 'No insights')[:100]}...")
        return updated_state
    
    def _reporter_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Reporter agent node"""
        user_query = state.get("user_query", "")
        print(f"📝 Reporter Agent: Generating final report...")
        
        updated_state = self.reporter.execute(user_query, state)
        
        print(f"✅ Report generated and saved: {updated_state.get('save_result', 'Not saved')}")
        return updated_state
    
    def run(self, user_query: str) -> Dict[str, Any]:
        """Execute the multi-agent workflow"""
        print(f"\n🚀 Starting Multi-Agent Analysis for: '{user_query}'\n")
        
        # Initial state
        initial_state = {
            "user_query": user_query,
            "current_agent": None,
            "completed": False
        }
        
        # Run the workflow
        final_state = self.graph.invoke(initial_state)
        
        print(f"\n🎉 Multi-Agent Analysis Complete!\n")
        
        return final_state
    
    def get_final_report(self, state: Dict[str, Any]) -> str:
        """Extract the final report from the state"""
        return state.get("final_report", "No report generated")
    
    def print_summary(self, state: Dict[str, Any]) -> None:
        """Print a summary of the workflow execution"""
        print("=" * 60)
        print("MULTI-AGENT WORKFLOW SUMMARY")
        print("=" * 60)
        
        print(f"Query: {state.get('user_query', 'N/A')}")
        print(f"\n🔍 Research Findings:")
        print(state.get('research_findings', 'No research findings'))
        
        print(f"\n📊 Calculation Results:")
        print(state.get('calculation_results', 'No calculations performed'))
        
        print(f"\n📝 File Operations:")
        print(state.get('save_result', 'No file operations'))
        
        print(f"\n📋 Final Report:")
        final_report = state.get('final_report', 'No final report generated')
        # Print first 500 characters of the report
        print(final_report[:500] + "..." if len(final_report) > 500 else final_report)
        
        print("=" * 60)