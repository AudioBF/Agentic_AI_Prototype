from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Dict, List, Optional
import json
import os

class ResponseEngine:
    def __init__(self, model_name: str = "gpt2-medium"):
        """
        Initialize the response engine with a language model.
        
        Args:
            model_name: Name of the pre-trained model to use
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Load response templates
        self.templates = self._load_templates()
        
        # Initialize conversation history
        self.conversation_history: List[Dict] = []
        
    def _load_templates(self) -> Dict:
        """Load response templates from JSON file."""
        template_path = os.path.join(os.path.dirname(__file__), 'templates.json')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._create_default_templates()
            
    def _create_default_templates(self) -> Dict:
        """Create default response templates."""
        return {
            "math": {
                "success": "The result of {expression} is {result}.",
                "error": "I couldn't calculate {expression}. {error}"
            },
            "country": {
                "success": "{country} has a {property} of {value}.",
                "error": "I couldn't find information about {country}."
            },
            "general": {
                "greeting": "Hello! How can I help you today?",
                "farewell": "Goodbye! Have a great day!",
                "unknown": "I'm not sure about that. Could you rephrase your question?"
            }
        }
        
    def generate_response(self, 
                         question: str, 
                         context: Dict,
                         template_type: str = "general") -> str:
        """
        Generate a natural language response based on the question and context.
        
        Args:
            question: The user's question
            context: Additional context for the response
            template_type: Type of response template to use
            
        Returns:
            A natural language response
        """
        # Add to conversation history
        self.conversation_history.append({
            "question": question,
            "context": context,
            "type": template_type
        })
        
        # Get appropriate template
        template = self._get_template(template_type, context)
        
        # Generate response
        if template_type == "math":
            return self._format_math_response(template, context)
        elif template_type == "country":
            return self._format_country_response(template, context)
        else:
            return self._format_general_response(template, context)
            
    def _get_template(self, template_type: str, context: Dict) -> str:
        """Get the appropriate response template."""
        templates = self.templates.get(template_type, {})
        return templates.get("success" if "error" not in context else "error", 
                           self.templates["general"]["unknown"])
                           
    def _format_math_response(self, template: str, context: Dict) -> str:
        """Format a mathematical response."""
        if "error" in context:
            return template.format(
                expression=context.get("expression", "the expression"),
                error=context["error"]
            )
            
        return template.format(
            expression=context.get("expression", "the calculation"),
            result=context.get("result", "the result")
        )
        
    def _format_country_response(self, template: str, context: Dict) -> str:
        """Format a country information response."""
        if "error" in context:
            return template.format(country=context.get("country", "that country"))
            
        return template.format(
            country=context.get("country", "The country"),
            property=context.get("property", "information"),
            value=context.get("value", "the value")
        )
        
    def _format_general_response(self, template: str, context: Dict) -> str:
        """Format a general response."""
        return template.format(**context)
        
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history."""
        return self.conversation_history
        
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = [] 