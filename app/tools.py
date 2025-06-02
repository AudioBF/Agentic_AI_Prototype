import requests
import re

def calculate(expression: str) -> str:
    """Calculate the result of a mathematical expression."""
    try:
        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Sorry, I couldn't calculate that: {str(e)}"

# Basic country information database
COUNTRY_DATA = {
    "Brazil": {
        "capital": "Brasília",
        "population": 214300000,
        "area": 8515770
    },
    "Japan": {
        "capital": "Tokyo",
        "population": 125700000,
        "area": 377975
    },
    "France": {
        "capital": "Paris",
        "population": 67390000,
        "area": 551695
    },
    "Canada": {
        "capital": "Ottawa",
        "population": 38250000,
        "area": 9984670
    },
    "Germany": {
        "capital": "Berlin",
        "population": 83240000,
        "area": 357022
    }
}

def get_country_info(country: str) -> dict:
    """Get information about a country."""
    country = country.strip().title()
    if country in COUNTRY_DATA:
        return COUNTRY_DATA[country]
    return {"error": f"Country {country} not found"}
