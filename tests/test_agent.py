from app.agent import Agent
import pytest
import logging
from unittest.mock import patch, MagicMock

def test_agent_initialization():
    agent = Agent()
    assert agent is not None
    assert hasattr(agent, 'generator')
    assert hasattr(agent, 'logger')
    assert hasattr(agent, '_cache')

def test_simple_math():
    agent = Agent()
    response = agent.process_question("What is 2 + 2?")
    assert "4" in response

def test_country_info():
    agent = Agent()
    response = agent.process_question("What is the capital of Brazil?")
    assert "Brasília" in response

def test_area_calculation():
    agent = Agent()
    response = agent.process_question("What is the area of France?")
    assert "km²" in response

def test_response_caching():
    agent = Agent()
    question = "What is 3 + 3?"
    
    # First call should generate new response
    response1 = agent.process_question(question)
    assert response1 is not None
    
    # Second call should use cached response
    response2 = agent.process_question(question)
    assert response2 == response1

def test_error_handling():
    agent = Agent()
    
    # Test invalid math expression
    response = agent.process_question("What is + ?")
    assert "couldn't find a valid mathematical expression" in response.lower()
    
    # Test invalid country
    response = agent.process_question("What is the capital of NonexistentCountry?")
    assert "couldn't find information" in response.lower()

def test_response_formatting():
    agent = Agent()
    
    # Test capital response format
    response = agent.process_question("What is the capital of Japan?")
    assert "capital" in response.lower()
    assert "vibrant city" in response.lower()
    
    # Test population response format
    response = agent.process_question("What is the population of Germany?")
    assert "population" in response.lower()
    assert "people" in response.lower()
    
    # Test area response format
    response = agent.process_question("What is the area of Italy?")
    assert "km²" in response
    assert "perspective" in response.lower()

@patch('app.agent.Agent._get_cached_response')
def test_cache_miss(mock_get_cached):
    agent = Agent()
    mock_get_cached.return_value = None
    
    response = agent.process_question("What is 5 + 5?")
    assert response is not None
    mock_get_cached.assert_called_once()

@patch('app.agent.Agent._get_cached_response')
def test_cache_hit(mock_get_cached):
    agent = Agent()
    mock_get_cached.return_value = "Cached response"
    
    response = agent.process_question("What is 5 + 5?")
    assert response == "Cached response"
    mock_get_cached.assert_called_once()

def test_logging():
    with patch('logging.Logger.info') as mock_info:
        agent = Agent()
        agent.process_question("What is 2 + 2?")
        assert mock_info.called 