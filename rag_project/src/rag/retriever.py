# src/rag/retriever.py
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from src.rag import get_task, init_clearml

task = init_clearml()   

class Retriever:
    def __init__(self, model_name='all-MiniLM-L6-v2', top_k=5):
        self.task = init_clearml()
        self.embedding_model = SentenceTransformer(model_name)
        self.qdrant_client = QdrantClient("localhost", port=6333)
        self.top_k = top_k
        self.collection_name = "github_repos"

    def get_relevant_chunks(self, query):
        self.task.get_logger().report_text(f"Retrieving relevant chunks for query: {query}")
        # Generate embedding for the query
        query_vector = self.embedding_model.encode(query).tolist()

        # Search in Qdrant
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=self.top_k
        )

        # Format results
        results = []
        for result in search_result:
            results.append({
                'content': result.payload.get('content', ''),
                'url': result.payload.get('url', ''),
                'path': result.payload.get('path', ''),
                'score': result.score
            })

        return results