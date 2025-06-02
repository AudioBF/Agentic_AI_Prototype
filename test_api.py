import requests
import json
from typing import Dict, Any

def test_api():
    base_url = "http://localhost:8000"
    headers = {"X-API-Key": "development-key"}
    
    # Lista de testes
    tests = [
        # Testes de área multiplicada
        "What is the area of Brazil multiplied by 3?",
        "Multiply the area of France by 2",
        "Japan's area times 4",
        "Area of Canada times 5",
        
        # Testes de capital
        "What is the capital of Brazil?",
        "France's capital",
        "What is Japan capital?",
        "Canada has a capital",
        
        # Testes de população
        "What is the population of Brazil?",
        "France's population",
        "Population of Japan",
        "How many people live in Canada?",
        
        # Testes de área
        "What is the area of Brazil?",
        "France's area",
        "Area of Japan",
        "How big is Canada?",
        
        # Testes de densidade populacional
        "What is the population density of Brazil?",
        "Population density of France",
        "Density of Japan",
        "How dense is Canada's population?",
        
        # Testes com pronomes
        "And its capital?",
        "What about its population?",
        "And the area?",
        
        # Testes matemáticos
        "What is 2 + 2?",
        "Calculate 5 * 10",
        "What is 100 / 4?",
        
        # Testes gerais
        "Who are you?",
        "What can you do?",
        "How are you?"
    ]
    
    # Executa os testes
    for i, question in enumerate(tests, 1):
        print(f"\nTeste {i}: {question}")
        try:
            response = requests.get(f"{base_url}/ask", params={"question": question}, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Resposta: {response.json()['response']}")
        except Exception as e:
            print(f"Erro: {str(e)}")

if __name__ == "__main__":
    test_api() 