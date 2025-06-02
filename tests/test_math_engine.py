from app.calculators.math_engine import MathEngine

def test_basic_calculations():
    engine = MathEngine()
    
    # Test addition
    result = engine.calculate("2 + 2")
    assert result["result"] == "4"
    assert result["type"] == "integer"
    
    # Test multiplication
    result = engine.calculate("3 * 4")
    assert result["result"] == "12"
    assert result["type"] == "integer"
    
    # Test division
    result = engine.calculate("10 / 2")
    assert result["result"] == "5"
    assert result["type"] == "integer"

def test_complex_calculations():
    engine = MathEngine()
    
    # Test with parentheses
    result = engine.calculate("(2 + 3) * 4")
    assert result["result"] == "20"
    
    # Test with decimals
    result = engine.calculate("3.14 * 2")
    assert result["type"] == "decimal"
    
    # Test with exponents
    result = engine.calculate("2^3")
    assert result["result"] == "8"

def test_invalid_expressions():
    engine = MathEngine()
    
    # Test invalid characters
    result = engine.calculate("2 + abc")
    assert "error" in result
    
    # Test unbalanced parentheses
    result = engine.calculate("(2 + 3")
    assert "error" in result
    
    # Test consecutive operators
    result = engine.calculate("2++3")
    assert "error" in result

def test_expression_cleaning():
    engine = MathEngine()
    
    # Test with spaces
    result = engine.calculate("2 + 2")
    assert result["result"] == "4"
    
    # Test with different multiplication symbols
    result = engine.calculate("2×3")
    assert result["result"] == "6"
    
    # Test with different division symbols
    result = engine.calculate("6÷2")
    assert result["result"] == "3" 