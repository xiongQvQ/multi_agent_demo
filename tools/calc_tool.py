from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import math
import re


class CalculatorInput(BaseModel):
    expression: str = Field(description="Mathematical expression or calculation request")


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Perform mathematical calculations and analysis"
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(
        self,
        expression: str,
        run_manager: Optional[any] = None,
    ) -> str:
        try:
            # Handle common financial calculations first
            if "p/e" in expression.lower() or "pe ratio" in expression.lower():
                # Extract numbers for P/E calculation
                numbers = re.findall(r'\d+\.?\d*', expression)
                if len(numbers) >= 2:
                    price = float(numbers[0])
                    earnings = float(numbers[1])
                    pe_ratio = price / earnings if earnings != 0 else 0
                    return f"P/E Ratio calculation: {price} / {earnings} = {pe_ratio:.2f}"
            
            if "market cap" in expression.lower():
                # Extract numbers for market cap calculation
                numbers = re.findall(r'\d+\.?\d*', expression)
                if len(numbers) >= 2:
                    price = float(numbers[0])
                    shares = float(numbers[1])
                    market_cap = price * shares
                    return f"Market Cap calculation: {price} * {shares} = ${market_cap:.2f}B"
            
            if "percentage change" in expression.lower() or "%" in expression:
                numbers = re.findall(r'\d+\.?\d*', expression)
                if len(numbers) >= 2:
                    old_value = float(numbers[0])
                    new_value = float(numbers[1])
                    change = ((new_value - old_value) / old_value) * 100
                    return f"Percentage change: ({new_value} - {old_value}) / {old_value} * 100 = {change:.2f}%"
            
            # Handle analysis requests with numbers
            if "analysis" in expression.lower():
                numbers = re.findall(r'\d+\.?\d*', expression)
                if numbers:
                    nums = [float(n) for n in numbers[:5]]  # Take first 5 numbers
                    results = []
                    
                    if len(nums) >= 1:
                        results.append(f"Values found: {nums}")
                    
                    if len(nums) >= 2:
                        # Calculate basic statistics
                        avg = sum(nums) / len(nums)
                        max_val = max(nums)
                        min_val = min(nums)
                        results.append(f"Average: {avg:.2f}")
                        results.append(f"Range: {min_val:.2f} to {max_val:.2f}")
                        
                        # Calculate percentage changes if we have enough numbers
                        if len(nums) >= 2:
                            change = ((nums[1] - nums[0]) / nums[0]) * 100
                            results.append(f"Change from first to second value: {change:.2f}%")
                    
                    return "Financial Analysis:\n" + "\n".join(results)
            
            # Basic mathematical expression evaluation
            # Only allow safe mathematical operations
            safe_chars = set('0123456789+-*/.() ')
            if all(c in safe_chars for c in expression):
                # Additional safety check - no consecutive operators
                if not re.search(r'[+\-*/]{2,}', expression):
                    try:
                        result = eval(expression)
                        return f"Calculation result: {expression} = {result}"
                    except:
                        pass
            
            # If no specific calculation can be performed, try to extract and analyze numbers
            numbers = re.findall(r'\d+\.?\d*', expression)
            if numbers:
                nums = [float(n) for n in numbers[:3]]
                return f"Numbers extracted from '{expression}': {nums}. For specific calculations, please provide clear mathematical operations."
            
            return f"Unable to perform calculation on: '{expression}'. Please provide a clear mathematical expression or specify the type of financial analysis needed."
            
        except Exception as e:
            return f"Calculation error: {str(e)}. Please provide a simpler mathematical expression."

    async def _arun(
        self,
        expression: str,
        run_manager: Optional[any] = None,
    ) -> str:
        return self._run(expression, run_manager)