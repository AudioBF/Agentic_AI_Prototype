from app.response.response_engine import ResponseEngine

def test_math_response():
    engine = ResponseEngine()
    
    # Test successful calculation
    context = {
        "expression": "2 + 2",
        "result": "4"
    }
    response = engine.generate_response("What is 2 + 2?", context, "math")
    assert "The result of 2 + 2 is 4" in response
    
    # Test calculation error
    context = {
        "expression": "2 + abc",
        "error": "Invalid expression"
    }
    response = engine.generate_response("What is 2 + abc?", context, "math")
    assert "I couldn't calculate" in response
    assert "Invalid expression" in response

def test_country_response():
    engine = ResponseEngine()
    
    # Test successful country info
    context = {
        "country": "Brazil",
        "property": "capital",
        "value": "Brasília"
    }
    response = engine.generate_response("What is the capital of Brazil?", context, "country")
    assert "Brazil has a capital of Brasília" in response
    
    # Test country error
    context = {
        "country": "NonexistentCountry",
        "error": "Country not found"
    }
    response = engine.generate_response("What is the capital of NonexistentCountry?", context, "country")
    assert "I couldn't find information about NonexistentCountry" in response

def test_general_response():
    engine = ResponseEngine()
    
    # Test greeting
    response = engine.generate_response("Hello!", {}, "general")
    assert "Hello! How can I help you today?" in response
    
    # Test unknown question
    response = engine.generate_response("What is the meaning of life?", {}, "general")
    assert "I'm not sure about that" in response

def test_conversation_history():
    engine = ResponseEngine()
    
    # Add some interactions
    engine.generate_response("Hello!", {}, "general")
    engine.generate_response("What is 2 + 2?", {"expression": "2 + 2", "result": "4"}, "math")
    
    # Check history
    history = engine.get_conversation_history()
    assert len(history) == 2
    assert history[0]["question"] == "Hello!"
    assert history[1]["question"] == "What is 2 + 2?"
    
    # Test clearing history
    engine.clear_history()
    assert len(engine.get_conversation_history()) == 0 