"""
Alternative Gemini API client using direct HTTP requests.
This can help with quota management and provides more control over API calls.
"""

import requests
import json
import os
from typing import Optional, Dict, Any

class GeminiClient:
    """Direct HTTP client for Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
    
    def generate_content(self, text: str, model: str = "gemini-2.0-flash") -> Optional[str]:
        """
        Generate content using direct API call
        
        Args:
            text: Input text for the AI
            model: Model to use (default: gemini-2.0-flash)
            
        Returns:
            Generated text or None if error
        """
        url = f"{self.base_url}/models/{model}:generateContent"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0]['text']
            
            # Handle quota errors
            elif response.status_code == 429:
                error_data = response.json()
                print(f"Quota exceeded: {error_data.get('error', {}).get('message', 'Unknown error')}")
                return "I'm sorry, I've reached my daily limit. Please try again later."
            
            # Handle other errors
            else:
                print(f"API Error {response.status_code}: {response.text}")
                return "I'm sorry, I'm having trouble processing your request right now."
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return "I'm sorry, I'm having trouble connecting to the AI service."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "I'm sorry, something went wrong. Please try again."
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        url = f"{self.base_url}/models"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            else:
                print(f"Error getting models: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Error getting models: {e}")
            return []

def test_gemini_client():
    """Test the Gemini client"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("GEMINI_API_KEY not found in environment variables")
        return
    
    client = GeminiClient(api_key)
    
    # Test content generation
    print("Testing Gemini API client...")
    response = client.generate_content("Hello, how are you?")
    print(f"Response: {response}")
    
    # Test available models
    print("\nAvailable models:")
    models = client.get_available_models()
    for model in models[:5]:  # Show first 5 models
        print(f"  - {model}")

if __name__ == "__main__":
    test_gemini_client()
