from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from app.agent import process_question
from app.config import Config
import time
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format=Config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agentic AI API",
    description="API for the Agentic AI Prototype",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
request_times: Dict[str, List[float]] = {}

def check_rate_limit(request: Request):
    """Check if the request is within rate limits."""
    client_ip = request.client.host
    current_time = time.time()
    
    # Initialize or clean old requests
    if client_ip not in request_times:
        request_times[client_ip] = []
    request_times[client_ip] = [t for t in request_times[client_ip] 
                              if current_time - t < 60]
    
    # Check rate limit
    if len(request_times[client_ip]) >= Config.RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
    
    # Add current request
    request_times[client_ip].append(current_time)

# API key security
api_key_header = APIKeyHeader(name=Config.API_KEY_HEADER)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify the API key."""
    # In development, accept the development key
    if api_key == "development-key":
        return api_key
        
    # In a real application, you would validate against a database or environment variable
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key is missing"
        )
    return api_key

@app.get("/ping")
async def ping():
    """Health check endpoint."""
    return {"message": "pong", "status": "healthy"}

@app.get("/ask")
async def ask(
    question: str,
    request: Request,
    api_key: str = Depends(verify_api_key)
):
    """
    Process a question and return the agent's response.
    
    Args:
        question: The question to process
        request: The FastAPI request object
        api_key: The API key for authentication
        
    Returns:
        dict: The response containing the agent's answer
    """
    try:
        # Check rate limit
        check_rate_limit(request)
        
        # Process the question
        logger.info(f"Processing question: {question}")
        response = process_question(question)
        
        return {
            "response": response,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question"
        )

@app.get("/config")
async def get_config(api_key: str = Depends(verify_api_key)):
    """Get the current configuration (excluding sensitive values)."""
    config = Config.get_all()
    # Remove sensitive information
    config.pop("API_KEY_HEADER", None)
    return config

if __name__ == "__main__":
    import uvicorn
    
    # Validate configuration
    Config.validate()
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        workers=Config.API_WORKERS
    )
