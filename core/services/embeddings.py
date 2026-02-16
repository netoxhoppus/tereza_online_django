
import google.generativeai as genai
from django.conf import settings

class EmbeddingService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = 'models/gemini-embedding-001' # Corrected model name based on list_models check
    
    import time

    def _generate_with_retry(self, text, task_type, retries=3, delay=2):
        for attempt in range(retries):
            try:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                    task_type=task_type
                )
                return result['embedding']
            except Exception as e:
                if "504" in str(e) or "Deadline Exceeded" in str(e):
                    if attempt < retries - 1:
                        print(f"Gemini API timeout (504). Retrying in {delay}s...")
                        self.time.sleep(delay)
                        continue
                print(f"Error generating embedding: {e}")
                return []
        return []

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generates embeddings for the given text using Google Gemini.
        """
        return self._generate_with_retry(text, "retrieval_document")
            
    def generate_query_embedding(self, text: str) -> list[float]:
         """
         Generates embeddings specifically for a query.
         """
         return self._generate_with_retry(text, "retrieval_query")
