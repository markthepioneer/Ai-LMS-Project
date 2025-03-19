"""
Email AI Service Module

This module provides AI-powered email processing capabilities including:
- Email summarization
- Smart response generation
- Priority classification
- Action item extraction
- Sentiment analysis
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
import openai
from transformers import pipeline
from app.utils.logger import get_logger

logger = get_logger(__name__)

class EmailAI:
    def __init__(self):
        """Initialize the Email AI service with necessary models and configurations."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.openai_api_key
        
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline('sentiment-analysis')
        
        # Email priority levels
        self.PRIORITY_LEVELS = {
            'urgent': 1,
            'high': 2,
            'medium': 3,
            'low': 4
        }

    async def analyze_email(self, email_content: str, subject: str) -> Dict:
        """
        Analyze email content and provide comprehensive insights.
        
        Args:
            email_content: The body of the email
            subject: The email subject line
            
        Returns:
            Dict containing analysis results including summary, priority, actions, etc.
        """
        try:
            # Generate email summary
            summary = await self.summarize_email(email_content)
            
            # Extract action items
            action_items = await self.extract_action_items(email_content)
            
            # Determine priority
            priority = await self.classify_priority(subject, email_content)
            
            # Analyze sentiment
            sentiment = self.analyze_sentiment(email_content)
            
            # Generate smart reply suggestions
            reply_suggestions = await self.generate_reply_suggestions(email_content)
            
            return {
                'summary': summary,
                'action_items': action_items,
                'priority': priority,
                'sentiment': sentiment,
                'reply_suggestions': reply_suggestions,
                'analyzed_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error analyzing email: {str(e)}")
            raise

    async def summarize_email(self, content: str) -> str:
        """Generate a concise summary of the email content."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Summarize the following email content in a concise way, highlighting key points:"},
                    {"role": "user", "content": content}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error summarizing email: {str(e)}")
            return "Error generating summary"

    async def extract_action_items(self, content: str) -> List[str]:
        """Extract action items and tasks from the email content."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Extract specific action items and tasks from the following email content. Return them as concise bullet points:"},
                    {"role": "user", "content": content}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            # Process the response into a list of action items
            action_items_text = response.choices[0].message.content.strip()
            action_items = [item.strip('- ') for item in action_items_text.split('\n') if item.strip()]
            return action_items
        except Exception as e:
            logger.error(f"Error extracting action items: {str(e)}")
            return []

    async def classify_priority(self, subject: str, content: str) -> str:
        """
        Classify email priority based on subject and content.
        Returns: 'urgent', 'high', 'medium', or 'low'
        """
        try:
            combined_text = f"Subject: {subject}\n\nContent: {content}"
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Classify the priority of this email as 'urgent', 'high', 'medium', or 'low' based on its content and subject. Consider urgency, importance, and time-sensitivity."},
                    {"role": "user", "content": combined_text}
                ],
                max_tokens=50,
                temperature=0.3
            )
            priority = response.choices[0].message.content.strip().lower()
            return priority if priority in self.PRIORITY_LEVELS else 'medium'
        except Exception as e:
            logger.error(f"Error classifying priority: {str(e)}")
            return 'medium'

    def analyze_sentiment(self, content: str) -> Dict:
        """Analyze the sentiment of the email content."""
        try:
            # Use transformers pipeline for sentiment analysis
            result = self.sentiment_analyzer(content[:512])[0]  # Limit content length
            return {
                'label': result['label'],
                'score': round(result['score'], 3)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {'label': 'NEUTRAL', 'score': 0.5}

    async def generate_reply_suggestions(self, content: str) -> List[str]:
        """Generate smart reply suggestions based on email content."""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Generate 3 different appropriate reply suggestions for this email. Make them professional, concise, and contextually relevant:"},
                    {"role": "user", "content": content}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            suggestions = response.choices[0].message.content.strip().split('\n')
            # Clean up and format suggestions
            suggestions = [s.strip('123. -') for s in suggestions if s.strip()]
            return suggestions[:3]  # Ensure we return at most 3 suggestions
        except Exception as e:
            logger.error(f"Error generating reply suggestions: {str(e)}")
            return ["Thank you for your email. I will review and respond soon."]

    async def generate_professional_response(self, 
                                          email_content: str,
                                          tone: str = 'professional',
                                          length: str = 'medium') -> str:
        """
        Generate a complete professional response to an email.
        
        Args:
            email_content: Original email content
            tone: Desired tone (professional, friendly, formal, etc.)
            length: Desired response length (short, medium, long)
            
        Returns:
            Generated response text
        """
        try:
            prompt = f"""
            Generate a {length} length, {tone} tone response to the following email.
            Make it contextually appropriate and maintain professional etiquette.
            
            Original Email:
            {email_content}
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant helping to draft professional email responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating professional response: {str(e)}")
            return "I apologize, but I was unable to generate a response at this time."

    async def categorize_email(self, subject: str, content: str) -> List[str]:
        """
        Categorize email into relevant categories/tags.
        Returns list of applicable categories.
        """
        try:
            combined_text = f"Subject: {subject}\n\nContent: {content}"
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze this email and provide relevant category tags (e.g., 'meeting', 'project', 'request', 'information', etc.). Return only the category names separated by commas:"},
                    {"role": "user", "content": combined_text}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            categories = response.choices[0].message.content.strip().split(',')
            return [cat.strip().lower() for cat in categories if cat.strip()]
        except Exception as e:
            logger.error(f"Error categorizing email: {str(e)}")
            return ["uncategorized"] 