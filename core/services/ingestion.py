
import os
import pypdf
import re
from .embeddings import EmbeddingService
from .vector_store import VectorStoreService

class IngestionService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()

    def ingest_directory(self, directory_path: str):
        """
        Scans a directory for .pdf and .txt files, processes them, and uploads to Supabase.
        """
        if not os.path.isdir(directory_path):
            print(f"Directory not found: {directory_path}")
            return

        # Get list of files in local directory
        local_files = set(os.listdir(directory_path))
        
        # Get list of sources in database
        db_sources = set(self.vector_store_service.get_all_sources())
        
        # Identify orphaned sources (in DB but not in local)
        orphaned_sources = db_sources - local_files
        
        # Delete orphaned sources
        for source in orphaned_sources:
            print(f"Deleting orphaned document from database: {source}")
            self.vector_store_service.delete_documents_by_source(source)

        for filename in local_files:
            file_path = os.path.join(directory_path, filename)

            # Check if file already exists in vector store
            if self.vector_store_service.document_exists(filename):
                print(f"Skipping {filename}: Already exists in database.")
                continue
            
            if filename.endswith(".pdf"):
                text = self._read_pdf(file_path)
            elif filename.endswith(".txt") or filename.endswith(".md"):
                text = self._read_text(file_path)
            else:
                continue

            if text:
                chunks = self._chunk_text(text)
                documents = []
                for chunk in chunks:
                    embedding = self.embedding_service.generate_embedding(chunk)
                    if embedding:
                        documents.append({
                            "content": chunk,
                            "metadata": {"source": filename},
                            "embedding": embedding
                        })
                
                if documents:
                    self.vector_store_service.add_documents(documents)
                    print(f"Ingested {filename} with {len(documents)} chunks.")

    def _read_pdf(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""

    def _read_text(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return ""



    def _chunk_text(self, text: str) -> list[str]:
        """
        Splits text based on Markdown headers (H1, H2, H3: #, ##, ###).
        Uses regex to identify headers and splits the content accordingly.
        """
        # Regex to find headers: line starting with 1 to 3 hashes followed by space
        # We use capturing group `(#{1,3} .*)` to keep the delimiter (the header itself) in the split result.
        # However, re.split with capturing group returns [pre_text, delimiter, post_text, delimiter...]
        
        pattern = r'(^#{1,3}\s.*)'
        segments = re.split(pattern, text, flags=re.MULTILINE)
        
        chunks = []
        current_chunk = ""
        
        for segment in segments:
            if not segment.strip():
                continue
            
            # Check if segment is a header
            if re.match(r'^#{1,3}\s', segment):
                # If we have a current chunk accumulating, push it to chunks
                if current_chunk:
                    chunks.append(current_chunk.strip())
                # Start new chunk with this header
                current_chunk = segment
            else:
                # Append content to current chunk
                current_chunk += "\n" + segment
        
        # Append the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        # Fallback if no headers found
        if not chunks and text.strip():
            chunks = [text.strip()]

        print(f"Split text into {len(chunks)} chunks based on Markdown headers (#, ##, ###).")
        return chunks
