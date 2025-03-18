# ai_engine/common.py
import os
import logging
from typing import List, Dict, Any, Optional
import openai
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

class AIError(Exception):
    """Custom exception for AI-related errors"""
    pass

def get_completion(
    prompt: str,
    system_message: Optional[str] = None,
    max_tokens: int = 300,
    temperature: float = 0.7,
    model: str = "gpt-4"
) -> str:
    """
    Get a completion from OpenAI API
    
    Args:
        prompt: The user prompt to send to the API
        system_message: Optional system message to guide the AI
        max_tokens: Maximum number of tokens to generate
        temperature: Temperature parameter (0-1), lower is more deterministic
        model: Model to use (default: gpt-4)
        
    Returns:
        The generated text response
    """
    try:
        messages = []
        
        # Add system message if provided
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"Error getting completion: {str(e)}")
        raise AIError(f"Failed to get AI completion: {str(e)}")

def analyze_text(text: str, analysis_type: str) -> Dict[str, Any]:
    """
    Analyze text using AI
    
    Args:
        text: The text to analyze
        analysis_type: Type of analysis to perform (sentiment, keywords, summary, etc.)
        
    Returns:
        Dictionary containing analysis results
    """
    if analysis_type == "sentiment":
        system_message = "Analyze the sentiment of the following text and return a JSON object with 'score' (from -1 to 1) and 'explanation'."
    elif analysis_type == "keywords":
        system_message = "Extract the most important keywords from the following text and return a JSON array of keywords."
    elif analysis_type == "summary":
        system_message = "Summarize the following text in a concise paragraph and return it as a string."
    else:
        system_message = f"Analyze the following text for {analysis_type} and provide a structured analysis."
    
    prompt = f"Text to analyze: {text}"
    
    try:
        result = get_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=500,
            temperature=0.3
        )
        
        # In a real implementation, parse the JSON response
        # For now, return a dummy structured response
        if analysis_type == "sentiment":
            return {
                "score": 0.5,  # Dummy positive sentiment
                "explanation": "The text appears to have a generally positive tone."
            }
        elif analysis_type == "keywords":
            return {
                "keywords": ["AI", "learning", "management", "system"]  # Dummy keywords
            }
        elif analysis_type == "summary":
            return {
                "summary": result
            }
        else:
            return {
                "analysis": result
            }
    
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        return {
            "error": f"Failed to analyze text: {str(e)}"
        }

def generate_response(
    context: Dict[str, Any],
    response_type: str
) -> str:
    """
    Generate a context-aware response
    
    Args:
        context: Dictionary containing context information
        response_type: Type of response to generate (email, message, etc.)
        
    Returns:
        Generated response as string
    """
    try:
        # Create a prompt based on the context
        prompt_parts = [f"Generate a {response_type} based on the following information:"]
        
        for key, value in context.items():
            if isinstance(value, str):
                prompt_parts.append(f"{key}: {value}")
            else:
                prompt_parts.append(f"{key}: {str(value)}")
        
        prompt = "\n".join(prompt_parts)
        
        system_message = f"You are an AI assistant helping to generate a {response_type}."
        
        return get_completion(
            prompt=prompt,
            system_message=system_message,
            max_tokens=1000,
            temperature=0.7
        )
    
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f"Error generating response: {str(e)}"

# Utility function for date/time handling
def parse_date_ranges(
    period: str,
    end_date: Optional[datetime] = None
) -> Dict[str, datetime]:
    """
    Parse date ranges based on period string
    
    Args:
        period: String representing period ('day', 'week', 'month', 'year')
        end_date: Optional end date, defaults to now
        
    Returns:
        Dictionary with start_date and end_date
    """
    if end_date is None:
        end_date = datetime.now()
    
    if period == "day":
        start_date = datetime(end_date.year, end_date.month, end_date.day, 0, 0, 0)
    elif period == "week":
        # Start from beginning of week (Monday)
        weekday = end_date.weekday()
        start_date = end_date - timedelta(days=weekday)
        start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    elif period == "month":
        # Start from beginning of month
        start_date = datetime(end_date.year, end_date.month, 1, 0, 0, 0)
    elif period == "year":
        # Start from beginning of year
        start_date = datetime(end_date.year, 1, 1, 0, 0, 0)
    else:
        # Default to last 24 hours
        start_date = end_date - timedelta(days=1)
    
    return {
        "start_date": start_date,
        "end_date": end_date
    }
