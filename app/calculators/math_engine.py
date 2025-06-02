from sympy import sympify, solve, Symbol
from decimal import Decimal, getcontext
from typing import Dict, Union, List
import re

class MathEngine:
    def __init__(self):
        # Set decimal precision
        getcontext().prec = 10
        
        # Define allowed operations
        self.allowed_operations = {
            '+': 'addition',
            '-': 'subtraction',
            '*': 'multiplication',
            '/': 'division',
            '^': 'exponentiation',
            '(': 'parentheses',
            ')': 'parentheses'
        }
        
    def calculate(self, expression: str) -> Dict[str, Union[str, List[str], str]]:
        """
        Calculate the result of a mathematical expression with detailed steps.
        
        Args:
            expression (str): The mathematical expression to calculate
            
        Returns:
            Dict containing:
                - result: The final result
                - steps: List of calculation steps
                - type: Type of calculation
                - error: Error message if any
        """
        try:
            # Clean and validate expression
            clean_expr = self._clean_expression(expression)
            if not self._validate_expression(clean_expr):
                return {"error": "Invalid mathematical expression"}
            
            # Parse expression
            expr = sympify(clean_expr)
            
            # Calculate result
            result = expr.evalf()
            
            # Get calculation steps
            steps = self._get_calculation_steps(expr)
            
            return {
                "result": str(result),
                "steps": steps,
                "type": self._get_result_type(result),
                "expression": clean_expr
            }
            
        except Exception as e:
            return {"error": f"Calculation error: {str(e)}"}
    
    def _clean_expression(self, expression: str) -> str:
        """Clean the expression by removing unwanted characters and normalizing format."""
        # Remove all whitespace
        expr = expression.replace(" ", "")
        
        # Replace common mathematical symbols
        expr = expr.replace("×", "*").replace("÷", "/")
        
        # Ensure proper decimal points
        expr = re.sub(r'\.+', '.', expr)
        
        return expr
    
    def _validate_expression(self, expression: str) -> bool:
        """Validate the mathematical expression."""
        # Check for empty expression
        if not expression:
            return False
            
        # Check for balanced parentheses
        if expression.count('(') != expression.count(')'):
            return False
            
        # Check for valid characters
        valid_chars = set('0123456789+-*/.()^')
        if not all(c in valid_chars for c in expression):
            return False
            
        # Check for consecutive operators
        if re.search(r'[\+\-\*\/\^]{2,}', expression):
            return False
            
        return True
    
    def _get_calculation_steps(self, expression) -> List[str]:
        """Generate step-by-step calculation process."""
        steps = []
        
        # If expression is simple, return single step
        if isinstance(expression, (int, float, Decimal)):
            return [f"Final result: {expression}"]
            
        # For more complex expressions, break down steps
        if expression.is_Add:
            terms = expression.args
            steps.append(f"Adding terms: {terms}")
        elif expression.is_Mul:
            factors = expression.args
            steps.append(f"Multiplying factors: {factors}")
        elif expression.is_Pow:
            base, exp = expression.args
            steps.append(f"Calculating power: {base}^{exp}")
            
        return steps
    
    def _get_result_type(self, result) -> str:
        """Determine the type of the result."""
        if result.is_integer:
            return "integer"
        elif result.is_rational:
            return "fraction"
        elif result.is_real:
            return "decimal"
        else:
            return "complex"
    
    def format_result(self, result: Dict) -> str:
        """Format the calculation result for display."""
        if "error" in result:
            return f"Error: {result['error']}"
            
        steps_str = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(result['steps'])])
        
        return f"""
Calculation: {result['expression']}
Type: {result['type']}
Steps:
{steps_str}
Result: {result['result']}
""" 