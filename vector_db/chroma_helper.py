import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import uuid
import os
from dotenv import load_dotenv

load_dotenv(override=True)

class ChromaDBHelper:
    def __init__(self, persist_directory="./chroma_db", collection_name="kpi_knowledge"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # Initialize Google Generative AI Embeddings
        # Uses GEMINI_API_KEY from environment by default
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        
        # Initialize local ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def generate_embedding(self, text: str) -> list[float]:
        """Generate embedding utilizing Gemini API."""
        return self.embeddings.embed_query(text)

    def add_document(self, text: str, metadata: dict = None):
        """Add a single document to the collection."""
        doc_id = str(uuid.uuid4())
        embedding = self.generate_embedding(text)
        
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}]
        )
        return doc_id

    def add_documents(self, texts: list[str], metadatas: list[dict] = None):
        """Add multiple documents efficiently."""
        if not metadatas:
            metadatas = [{} for _ in texts]
            
        ids = [str(uuid.uuid4()) for _ in texts]
        embeddings = self.embeddings.embed_documents(texts)
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        return ids

    def query(self, query_text: str, n_results: int = 3) -> list[dict]:
        """Query the vector database for relevant documents."""
        query_embedding = self.generate_embedding(query_text)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Formulate cleaner return structure
        formatted_results = []
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "document": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        
        return formatted_results

    def retrieve_context(self, query_text: str, n_results: int = 3) -> str:
        """Helper to get just the joined string context for prompt injection."""
        results = self.query(query_text, n_results)
        return "\n\n".join([r['document'] for r in results])

    def seed_knowledge_base(self):
        """Seeds initial data to the vector DB if empty."""
        if self.collection.count() > 0:
            return  # Already seeded
            
        knowledge_texts = [
            "Hackathons are excellent for demonstrating real-world problem-solving skills and teamwork, making them highly valued by top tech recruiters.",
            "Industrial visits provide practical exposure to manufacturing and operational processes that standard coursework often misses.",
            "Certifications from NPTEL or Coursera validate specialized knowledge outside the core curriculum, proving a student's self-drive to learn.",
            "If a student's Career Readiness Score is below 50, they should immediately focus on acquiring a relevant internship and participating in coding competitions.",
            "To boost your KPI score rapidly, prioritize high-weight tasks like securing an Internship (weight 25) or publishing a Paper (weight 25) over smaller activities like attending a single workshop (weight 5).",
            "Project Mentorship shows leadership and deep understanding of a topic. It is highly recommended for students aiming for research or senior technical roles."
        ]
        
        metadatas = [{"source": "kpi_system_rules"} for _ in knowledge_texts]
        self.add_documents(knowledge_texts, metadatas)
        print("Vector database seeded with initial knowledge.")

# Initialize a global instance for the application to share
chroma_db = ChromaDBHelper()
