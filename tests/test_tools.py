"""
Unit tests for the tools module
"""
import pytest
from unittest.mock import Mock, patch
import requests
from tools.search_tool import SearchTool
from tools.calc_tool import CalculatorTool
from tools.file_tool import FileTool
import os
import tempfile


class TestSearchTool:
    """Test cases for SearchTool"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.search_tool = SearchTool()
    
    def test_search_tool_initialization(self):
        """Test SearchTool initialization"""
        assert self.search_tool.name == "search"
        assert "search for information" in self.search_tool.description.lower()
    
    @patch('requests.get')
    def test_search_with_serper_api_success(self, mock_get):
        """Test successful search with Serper API"""
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "organic": [
                {
                    "title": "Test Result",
                    "snippet": "Test snippet",
                    "link": "https://test.com"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        with patch.dict(os.environ, {'SERPER_API_KEY': 'test_key'}):
            result = self.search_tool._run("test query")
        
        assert "Test Result" in result
        assert "Test snippet" in result
        assert "https://test.com" in result
    
    @patch('requests.get')
    def test_search_with_serper_api_failure(self, mock_get):
        """Test search fallback when Serper API fails"""
        # Mock API failure
        mock_get.side_effect = requests.RequestException("API Error")
        
        with patch.dict(os.environ, {'SERPER_API_KEY': 'test_key'}):
            result = self.search_tool._run("test query")
        
        # Should fallback to simulated results
        assert "simulated search result" in result.lower()
    
    def test_search_without_api_key(self):
        """Test search without API key (simulated mode)"""
        with patch.dict(os.environ, {}, clear=True):
            result = self.search_tool._run("test query")
        
        assert "simulated search result" in result.lower()
        assert "test query" in result.lower()
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        result = self.search_tool._run("")
        assert "error" in result.lower() or "invalid" in result.lower()
    
    def test_search_malicious_query(self):
        """Test search with potentially malicious query"""
        malicious_query = "<script>alert('xss')</script>"
        result = self.search_tool._run(malicious_query)
        # Should not contain raw script tags
        assert "<script>" not in result


class TestCalculatorTool:
    """Test cases for CalculatorTool"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.calc_tool = CalculatorTool()
    
    def test_calculator_initialization(self):
        """Test CalculatorTool initialization"""
        assert self.calc_tool.name == "calculator"
        assert "calculate" in self.calc_tool.description.lower()
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations"""
        test_cases = [
            ("2 + 3", "5"),
            ("10 - 4", "6"),
            ("3 * 7", "21"),
            ("15 / 3", "5"),
            ("2 ** 3", "8"),  # exponentiation
        ]
        
        for expression, expected in test_cases:
            result = self.calc_tool._run(expression)
            assert expected in result
    
    def test_complex_expressions(self):
        """Test complex mathematical expressions"""
        test_cases = [
            ("(2 + 3) * 4", "20"),
            ("sqrt(16)", "4"),
            ("sin(0)", "0"),
            ("log(10)", "2.3"),  # natural log
        ]
        
        for expression, expected_substring in test_cases:
            result = self.calc_tool._run(expression)
            # Check if result contains expected value (allowing for floating point precision)
            assert any(expected_substring in result for expected_substring in [expected_substring])
    
    def test_invalid_expressions(self):
        """Test handling of invalid expressions"""
        invalid_expressions = [
            "2 + ",  # incomplete
            "2 / 0",  # division by zero
            "undefined_function(5)",  # undefined function
            "2 +* 3",  # syntax error
        ]
        
        for expr in invalid_expressions:
            result = self.calc_tool._run(expr)
            assert "error" in result.lower()
    
    def test_security_expressions(self):
        """Test security against malicious expressions"""
        malicious_expressions = [
            "__import__('os').system('ls')",  # code injection
            "exec('print(\"hack\")')",  # exec injection
            "eval('__import__(\"os\").getcwd()')",  # eval injection
        ]
        
        for expr in malicious_expressions:
            result = self.calc_tool._run(expr)
            # Should return error, not execute code
            assert "error" in result.lower()
            assert "hack" not in result.lower()


class TestFileTool:
    """Test cases for FileTool"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.file_tool = FileTool()
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_file_tool_initialization(self):
        """Test FileTool initialization"""
        assert self.file_tool.name == "file_operations"
        assert "save" in self.file_tool.description.lower()
    
    def test_save_file_success(self):
        """Test successful file saving"""
        content = "Test content for file saving"
        filename = "test_report.txt"
        
        # Use the file tool to save content
        result = self.file_tool._run(f"save:{filename}:{content}")
        
        # Check if file was created and contains correct content
        assert "successfully" in result.lower()
        assert filename in result
        
        # Verify file exists and has correct content
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert content in saved_content
            # Clean up
            os.remove(filename)
    
    def test_save_file_with_chinese_content(self):
        """Test saving file with Chinese content"""
        content = "这是一个包含中文的测试文件内容"
        filename = "chinese_test.txt"
        
        result = self.file_tool._run(f"save:{filename}:{content}")
        
        assert "successfully" in result.lower()
        
        # Verify Chinese content is preserved
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert content in saved_content
            # Clean up
            os.remove(filename)
    
    def test_save_file_invalid_format(self):
        """Test file saving with invalid format"""
        # Missing parts in the command
        invalid_commands = [
            "save:filename_only",
            "save:",
            "invalid_command:filename:content",
            "",
        ]
        
        for cmd in invalid_commands:
            result = self.file_tool._run(cmd)
            assert "error" in result.lower() or "invalid" in result.lower()
    
    def test_save_file_security(self):
        """Test file saving security (path traversal)"""
        malicious_filenames = [
            "../../../etc/passwd",  # path traversal
            "..\\..\\windows\\system32\\config\\sam",  # windows path traversal
            "/etc/hosts",  # absolute path
        ]
        
        for filename in malicious_filenames:
            result = self.file_tool._run(f"save:{filename}:malicious content")
            # Should either error or sanitize the filename
            assert not os.path.exists(filename), f"Security vulnerability: {filename} was created"
    
    def test_large_file_handling(self):
        """Test handling of large file content"""
        # Create large content (1MB)
        large_content = "x" * (1024 * 1024)
        filename = "large_test.txt"
        
        result = self.file_tool._run(f"save:{filename}:{large_content}")
        
        # Should handle large files gracefully
        if "successfully" in result.lower():
            assert os.path.exists(filename)
            # Clean up
            if os.path.exists(filename):
                os.remove(filename)
        else:
            # If it fails, it should fail gracefully with an error message
            assert "error" in result.lower()


class TestToolIntegration:
    """Integration tests for tools working together"""
    
    def test_tools_can_be_imported(self):
        """Test that all tools can be imported successfully"""
        from tools.search_tool import SearchTool
        from tools.calc_tool import CalculatorTool
        from tools.file_tool import FileTool
        
        tools = [SearchTool(), CalculatorTool(), FileTool()]
        
        # All tools should have required attributes
        for tool in tools:
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'description')
            assert hasattr(tool, '_run')
            assert callable(tool._run)
    
    def test_workflow_simulation(self):
        """Test a simplified workflow using all tools"""
        search_tool = SearchTool()
        calc_tool = CalculatorTool()
        file_tool = FileTool()
        
        # Simulate a research workflow
        # 1. Search for information
        search_result = search_tool._run("Apple stock price")
        assert len(search_result) > 0
        
        # 2. Perform calculation
        calc_result = calc_tool._run("100 * 1.05")  # Simple growth calculation
        assert "105" in calc_result
        
        # 3. Save report
        report_content = f"Search: {search_result[:100]}...\nCalculation: {calc_result}"
        file_result = file_tool._run(f"save:integration_test_report.md:{report_content}")
        
        # Clean up if file was created
        if os.path.exists("integration_test_report.md"):
            os.remove("integration_test_report.md")
        
        # All operations should complete without critical errors
        assert not any("critical error" in result.lower() 
                      for result in [search_result, calc_result, file_result])