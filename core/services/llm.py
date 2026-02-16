
import requests
import json
from django.conf import settings

class LLMService:
    def __init__(self, model: str = "deepseek-v3.1:671b"):
        self.host = settings.OLLAMA_HOST
        self.api_key = settings.OLLAMA_API_KEY
        self.model = model
        
        # Ensure host doesn't end with slash for cleaner URL joining
        if self.host.endswith('/'):
            self.host = self.host[:-1]

    def generate_response(self, prompt: str, system_message: str = None) -> str:
        """
        Generates a response from the Ollama model.
        """
        url = f"{self.host}/api/chat"
        
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add Authorization header if API Key is present (though Ollama usually runs without auth locally/internally)
        # But user mentioned providing keys in .env, so we support it.
        if self.api_key:
             headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)
            response.raise_for_status()
            
            result = response.json()
            return result.get('message', {}).get('content', '')
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            return f"Error connecting to AI Provider: {str(e)}"
