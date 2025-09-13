#!/usr/bin/env python3
"""
ReadyTensor Multi-Agent Demo
A simple multi-agent system demonstrating agent coordination and tool usage.
"""

import os
import sys
from dotenv import load_dotenv
from workflow import MultiAgentWorkflow


def main():
    """Main entry point for the multi-agent demo"""
    
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please set your Google API key in the .env file")
        sys.exit(1)
    
    print("🤖 ReadyTensor Multi-Agent Demo")
    print("=" * 50)
    print("This demo showcases a multi-agent system with:")
    print("• 3 Agents: Researcher, Analyst, Reporter")
    print("• 3 Tools: Search, Calculator, File Processing")
    print("• LangGraph Orchestration")
    print("=" * 50)
    
    # Initialize the workflow
    try:
        workflow = MultiAgentWorkflow()
        print("✅ Multi-agent system initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing workflow: {str(e)}")
        sys.exit(1)
    
    # Demo scenarios
    demo_queries = [
        "分析一下苹果公司的股价趋势",
        "Analyze Tesla's stock performance",
        "Research Microsoft's latest quarterly earnings"
    ]
    
    while True:
        print("\n" + "="*50)
        print("DEMO OPTIONS:")
        print("1. Use predefined demo queries")
        print("2. Enter your own query")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            print("\nAvailable demo queries:")
            for i, query in enumerate(demo_queries, 1):
                print(f"{i}. {query}")
            
            try:
                demo_choice = int(input("\nSelect a demo query (1-3): ")) - 1
                if 0 <= demo_choice < len(demo_queries):
                    query = demo_queries[demo_choice]
                else:
                    print("Invalid selection. Using default query.")
                    query = demo_queries[0]
            except ValueError:
                print("Invalid input. Using default query.")
                query = demo_queries[0]
        
        elif choice == "2":
            query = input("\nEnter your query: ").strip()
            if not query:
                print("Empty query. Please try again.")
                continue
        
        elif choice == "3":
            print("👋 Thank you for using the Multi-Agent Demo!")
            break
        
        else:
            print("Invalid option. Please try again.")
            continue
        
        # Run the multi-agent workflow
        try:
            print(f"\n🚀 Processing query: '{query}'")
            print("-" * 50)
            
            # Execute the workflow
            final_state = workflow.run(query)
            
            # Display results
            workflow.print_summary(final_state)
            
            # Ask if user wants to see the full report
            show_full = input("\n📄 Would you like to see the full report? (y/n): ").strip().lower()
            if show_full == 'y':
                print("\n" + "="*60)
                print("FULL REPORT")
                print("="*60)
                print(workflow.get_final_report(final_state))
                print("="*60)
        
        except Exception as e:
            print(f"❌ Error during workflow execution: {str(e)}")
            print("Please check your API keys and network connection.")
        
        # Ask if user wants to continue
        continue_demo = input("\n🔄 Would you like to run another query? (y/n): ").strip().lower()
        if continue_demo != 'y':
            print("👋 Thank you for using the Multi-Agent Demo!")
            break


if __name__ == "__main__":
    main()