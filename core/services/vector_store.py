
from supabase import create_client, Client
from django.conf import settings

class VectorStoreService:
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.table_name = "documents" # Assumed table name from n8n 

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """
        Searches for similar documents in Supabase using the 'match_documents' RPC function.
        This assumes an RPC function exists in Supabase:
        create or replace function match_documents (
          query_embedding vector(768),
          match_threshold float,
          match_count int
        )
        returns table (
          id bigint,
          content text,
          metadata jsonb,
          similarity float
        )
        language plpgsql
        as $$
        begin
          return query
          select
            documents.id,
            documents.content,
            documents.metadata,
            1 - (documents.embedding <=> query_embedding) as similarity
          from documents
          where 1 - (documents.embedding <=> query_embedding) > match_threshold
          order by documents.embedding <=> query_embedding
          limit match_count;
        end;
        $$;
        """
        try:
            # Using the RPC call which is standard for vector search in Supabase
            response = self.supabase.rpc(
                'match_documents',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.5, # Adjust threshold as needed
                    'match_count': top_k
                }
            ).execute()
            
            return response.data
            
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []

    def add_documents(self, documents: list[dict]) -> None:
        """
        Adds documents to the Supabase vector store.
        documents: list of dicts with keys 'content', 'metadata', 'embedding'
        """
        try:
            self.supabase.table(self.table_name).insert(documents).execute()
        except Exception as e:
            print(f"Error adding documents: {e}")
            raise e

    def document_exists(self, source_filename: str) -> bool:
        """
        Checks if a document with the given source filename already exists in the metadata.
        """
        try:
            # metadata is a JSONB column, we query for the 'source' key
            response = self.supabase.table(self.table_name)\
                .select("id", count="exact")\
                .eq("metadata->>source", source_filename)\
                .limit(1)\
                .execute()
            
            # If count > 0, the document exists
            return response.count > 0
        except Exception as e:
            print(f"Error checking document existence: {e}")
            print(f"Error checking document existence: {e}")
            return False

    def get_all_sources(self) -> list[str]:
        """
        Retrieves a list of all unique source filenames currently in the database.
        """
        try:
            # We select the metadata column. 
            # Note: distinct on metadata->>source might need raw sql or careful query construction
            # For simplicity, we fetch all sources and dedup in python if scale allows, 
            # or better: use an RPC for distinct sources if possible.
            # Here we try a direct query approach:
            
            response = self.supabase.table(self.table_name)\
                .select("metadata")\
                .execute()
                
            sources = set()
            for row in response.data:
                source = row.get('metadata', {}).get('source')
                if source:
                    sources.add(source)
            return list(sources)
        except Exception as e:
            print(f"Error fetching sources: {e}")
            return []

    def delete_documents_by_source(self, source_filename: str) -> None:
        """
        Deletes all documents associated with a specific source filename.
        """
        try:
            self.supabase.table(self.table_name)\
                .delete()\
                .eq("metadata->>source", source_filename)\
                .execute()
        except Exception as e:
            print(f"Error deleting documents for {source_filename}: {e}")

