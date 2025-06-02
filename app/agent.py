from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.tools import calculate, get_country_info
from app.memory import set_last_country, get_last_country
from app.config import Config
import re
import logging
import torch

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT,
    handlers=[logging.StreamHandler()]
)

class Agent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing T5 model...")
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(Config.MODEL_NAME)
        
        # Move model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        
        self.logger.info(f"Model loaded successfully on {self.device}")

    def process_question(self, question: str) -> str:
        self.logger.info(f"Processing question: {question}")
        response = None
        q = question.strip().lower()

        try:
            # Função auxiliar para limpar o nome do país
            def clean_country_name(name: str) -> str:
                # Remove possessivos, palavras comuns e pontuação
                name = re.sub(r"'s$", "", name)
                name = re.sub(r"^(what is|how many|how big|how dense|the|a|an)\s+", "", name)
                # Remove palavras extras do final
                name = re.sub(r"\s+(capital|population|area|times|multiplied|multiply|by|in|has|a|an)$", "", name)
                # Remove pontuação final
                name = re.sub(r"[\?\.,!]+$", "", name)
                return name.strip(" .!?").title()

            # Função auxiliar para processar resposta de país
            def process_country_response(country: str, info_type: str, value: str) -> str:
                set_last_country(country)
                return value

            # 1. Área multiplicada (vários formatos)
            area_mult_patterns = [
                r"area of ([a-zA-Z\s]+?)(?=\s+(?:multiplied|multiply|times)\s+(?:by\s+)?\d+)",
                r"([a-zA-Z\s]+?)'s?\s+area(?=\s+(?:multiplied|multiply|times)\s+(?:by\s+)?\d+)",
                r"multiply the area of ([a-zA-Z\s]+?)(?=\s+(?:by\s+)?\d+)",
                r"([a-zA-Z\s]+?)'s?\s+area(?=\s+times\s+\d+)",
                r"area of ([a-zA-Z\s]+?)(?=\s+times\s+\d+)"
            ]
            for pat in area_mult_patterns:
                m = re.search(pat, q)
                if m:
                    country = clean_country_name(m.group(1))
                    # Extrair o multiplicador separadamente
                    mult_match = re.search(r"(?:multiplied|multiply)\s+by\s+(\d+)|times\s+(\d+)", q)
                    if not mult_match:
                        continue
                    multiplier = int(mult_match.group(1) or mult_match.group(2))
                    country_info = get_country_info(country)
                    if "error" in country_info:
                        response = f"I couldn't find information about {country}."
                        continue
                    area = float(country_info["area"])
                    result = calculate(f"{area} * {multiplier}")
                    if result.startswith("Sorry"):
                        response = result
                    else:
                        response = process_country_response(
                            country,
                            "area_mult",
                            f"The area of {country} is {area:,.0f} km². Multiplied by {multiplier}, that is {float(result):,.0f} km²."
                        )
                    return response

            # 2. Densidade populacional
            dens_patterns = [
                r"population density of ([a-zA-Z\s]+)",
                r"density of ([a-zA-Z\s]+)",
                r"([a-zA-Z\s]+)'s population density",
                r"how dense is ([a-zA-Z\s]+)'s population"
            ]
            for pat in dens_patterns:
                m = re.search(pat, q)
                if m:
                    country = clean_country_name(m.group(1))
                    country_info = get_country_info(country)
                    if "error" in country_info:
                        response = f"I couldn't find information about {country}."
                        continue
                    pop = country_info["population"]
                    area = country_info["area"]
                    density = pop / area
                    response = process_country_response(
                        country,
                        "density",
                        f"The population density of {country} is {density:,.2f} people per km²."
                    )
                    return response

            # 4. Perguntas com pronomes
            if any(word in q for word in ["its capital", "its population", "its area", "and its capital", "and its population", "and its area", "what about its", "and the area"]):
                country = get_last_country()
                if not country:
                    response = "I don't know which country you're referring to. Please mention a country first."
                    return response
                country_info = get_country_info(country)
                if "error" in country_info:
                    response = f"I couldn't find information about {country}."
                    return response
                if "capital" in q:
                    response = f"The capital of {country} is {country_info['capital']}."
                elif "population" in q:
                    response = f"The population of {country} is {int(country_info['population']):,} people."
                elif "area" in q:
                    response = f"The area of {country} is {float(country_info['area']):,.0f} km²."
                return response

            # 3. Perguntas sobre capital, população, área (vários formatos)
            info_patterns = [
                (r"(capital|population|area) of ([a-zA-Z\s]+)", 1, 2),
                (r"([a-zA-Z\s]+?)'s (capital|population|area)", 2, 1),
                (r"([a-zA-Z\s]+) (capital|population|area)", 2, 1),
                (r"what is the (capital|population|area) of ([a-zA-Z\s]+)", 1, 2),
                (r"([a-zA-Z\s]+) (?:has )?(?:a )?(capital|population|area)", 2, 1),
                (r"how many people live in ([a-zA-Z\s]+)[\?\.!]*", "population", 1),
                (r"how big is ([a-zA-Z\s]+)[\?\.!]*", "area", 1),
                (r"what is ([a-zA-Z\s]+)'s (capital|population|area)", 2, 1),
                (r"([a-zA-Z\s]+) (?:has )?(?:a )?(?:population|area|capital)[\?\.!]*", "area", 1),
                (r"([a-zA-Z\s]+) (?:has )?(?:a )?(?:population|area|capital)[\?\.!]*", "population", 1),
                (r"([a-zA-Z\s]+) (?:has )?(?:a )?(?:population|area|capital)[\?\.!]*", "capital", 1)
            ]
            for pat in info_patterns:
                if len(pat) == 3:
                    pattern, topic_idx, country_idx = pat
                    m = re.search(pattern, q)
                    if m:
                        topic = m.group(topic_idx).lower()
                        country = clean_country_name(m.group(country_idx))
                        country_info = get_country_info(country)
                        if "error" in country_info:
                            response = f"I couldn't find information about {country}."
                            continue
                        if topic == "capital":
                            response = process_country_response(
                                country,
                                "capital",
                                f"The capital of {country} is {country_info['capital']}."
                            )
                        elif topic == "population":
                            response = process_country_response(
                                country,
                                "population",
                                f"The population of {country} is {int(country_info['population']):,} people."
                            )
                        elif topic == "area":
                            response = process_country_response(
                                country,
                                "area",
                                f"The area of {country} is {float(country_info['area']):,.0f} km²."
                            )
                        return response
                else:
                    pattern, topic, country_idx = pat
                    m = re.search(pattern, q)
                    if m:
                        country = clean_country_name(m.group(country_idx))
                        country_info = get_country_info(country)
                        if "error" in country_info:
                            response = f"I couldn't find information about {country}."
                            continue
                        if topic == "population":
                            response = process_country_response(
                                country,
                                "population",
                                f"The population of {country} is {int(country_info['population']):,} people."
                            )
                        elif topic == "area":
                            response = process_country_response(
                                country,
                                "area",
                                f"The area of {country} is {float(country_info['area']):,.0f} km²."
                            )
                        return response

            # 5. Perguntas matemáticas simples
            if re.search(r"\d+\s*[\+\-\*/\^]\s*\d+", question):
                match = re.search(r"(\d+\s*[\+\-\*/\^]\s*\d+)", question)
                expression = match.group(1) if match else ""
                if not expression:
                    response = "I couldn't find a valid mathematical expression."
                else:
                    result = calculate(expression)
                    if result.startswith("Sorry"):
                        response = result
                    else:
                        response = f"{expression} = {result}"
                return response

            # 6. Perguntas gerais
            if "who are you" in q:
                return "I am an AI assistant that can help you with information about countries, calculations, and general knowledge questions."
            if "what can you do" in q:
                return "I can help you with: 1) Country information (capital, population, area), 2) Mathematical calculations, 3) General knowledge questions."
            if "how are you" in q:
                return "I'm functioning well and ready to help you! What would you like to know?"

            # Fallback: detectar país conhecido na frase e responder com info básica
            known_countries = ["Brazil", "France", "Japan", "Canada", "Germany"]
            for country in known_countries:
                if country.lower() in q:
                    country_info = get_country_info(country)
                    if "error" not in country_info:
                        set_last_country(country)
                        if "capital" in q:
                            response = f"The capital of {country} is {country_info['capital']}."
                        elif "population" in q:
                            response = f"The population of {country} is {int(country_info['population']):,} people."
                        elif "area" in q:
                            response = f"The area of {country} is {float(country_info['area']):,.0f} km²."
                        else:
                            response = (
                                f"{country}: Capital: {country_info['capital']}, "
                                f"Population: {int(country_info['population']):,} people, "
                                f"Area: {float(country_info['area']):,.0f} km²."
                            )
                        return response

            # Se chegou aqui, nenhum padrão foi encontrado
            self.logger.error("No response generated")
            return "I'm sorry, I couldn't process your question. Please try again."
                
        except Exception as e:
            self.logger.error(f"Error processing question: {str(e)}")
            return "I'm sorry, I encountered an error while processing your question. Please try again."

# Create a global agent instance
agent = Agent()

def process_question(question: str) -> str:
    return agent.process_question(question)
