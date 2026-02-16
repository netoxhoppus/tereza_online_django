
from supabase import create_client, Client
from django.conf import settings

class MemoryService:
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.table_name = "tereza_chat_history"

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """
        Adds a message to the conversation history.
        """
        try:
            message = {
                "session_id": session_id,
                "role": role,
                "content": content
            }
            self.supabase.table(self.table_name).insert(message).execute()
        except Exception as e:
            print(f"Error adding message to memory: {e}")

    def get_history(self, session_id: str, limit: int = 20) -> list[dict]:
        """
        Retrieves the conversation history for a given session.
        Returns a list of dicts with 'role' and 'content' keys.
        """
        try:
            response = self.supabase.table(self.table_name)\
                .select("role, content")\
                .eq("session_id", session_id)\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            # Reverse to return in chronological order for the context window
            return response.data[::-1] if response.data else []
            
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []
