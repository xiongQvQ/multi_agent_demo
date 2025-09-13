#!/usr/bin/env python3
"""
Test script to verify that all tools are working correctly
"""

from tools.search_tool import SearchTool
from tools.calc_tool import CalculatorTool
from tools.file_tool import FileTool


def test_search_tool():
    """Test the search tool"""
    print("🔍 Testing Search Tool...")
    search_tool = SearchTool()
    
    # Test with different queries
    test_queries = [
        "Apple stock",
        "Microsoft earnings",
        "Tesla performance"
    ]
    
    for query in test_queries:
        result = search_tool._run(query)
        print(f"Query: {query}")
        print(f"Result: {result[:200]}...")
        print("-" * 50)


def test_calculator_tool():
    """Test the calculator tool"""
    print("\n📊 Testing Calculator Tool...")
    calc_tool = CalculatorTool()
    
    # Test with different calculation types
    test_expressions = [
        "185.50 + 2.3",  # Simple math
        "P/E ratio 185.50 28.5",  # P/E calculation
        "percentage change 185.50 190.80",  # Percentage change
        "market cap 185.50 15.7",  # Market cap
        "analysis of values: 185.50, 2.3, 28.5",  # General analysis
        "general financial analysis"  # Default case
    ]
    
    for expr in test_expressions:
        result = calc_tool._run(expr)
        print(f"Expression: {expr}")
        print(f"Result: {result}")
        print("-" * 50)


def test_file_tool():
    """Test the file tool"""
    print("\n📝 Testing File Tool...")
    file_tool = FileTool()
    
    # Test write operation
    test_content = """# Test Report
    
This is a test report to verify the file tool is working.

## Key Points
- Search tool integration: ✅
- Calculator tool integration: ✅
- File tool integration: ✅

## Conclusion
All tools are functioning properly.
    """
    
    # Write test file
    result = file_tool._run("create_report", "test_report.md", test_content)
    print(f"Write result: {result}")
    
    # Read test file
    result = file_tool._run("read", "test_report.md")
    print(f"Read result: {result[:200]}...")
    
    print("-" * 50)


def main():
    """Run all tool tests"""
    print("🧪 Multi-Agent Tool Testing")
    print("=" * 60)
    
    try:
        test_search_tool()
        test_calculator_tool()
        test_file_tool()
        
        print("\n✅ All tools tested successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")


if __name__ == "__main__":
    main()