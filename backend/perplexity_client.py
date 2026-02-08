import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class PerplexityClient:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        
        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar"  # Premium model 
    
    async def ask(self, prompt: str, system_prompt: Optional[str] = None) -> str: # optional
        """
        Send a query to Perplexity API and return the response
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1,  # Lower temp for more factual responses
            "max_tokens": 250
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.base_url,
                headers=headers,
                json=payload
            )
            
            # Better error handling
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"Perplexity API Error {response.status_code}: {error_detail}")
            
            data = response.json()
            return data["choices"][0]["message"]["content"]

