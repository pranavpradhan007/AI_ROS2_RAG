# src/database/qdrant_client.py
from src.rag import get_task
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from clearml import Logger

class QdrantDBClient:
    def __init__(self):
        self.task = get_task()
        self.client = QdrantClient(
            host="localhost",
            port=6333
        )
        self.collection_name = "github_repos"
        self._create_collection()
        self._embedding_count = 0

    def _create_collection(self):
        try:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,  
                    distance=Distance.COSINE
                )
            )
        except Exception as e:
            print(f"Error creating collection: {str(e)}")

    def store_embeddings(self, id, embeddings, payload):
        try:
            point_id = str(uuid.uuid4())
            point = PointStruct(
                id=point_id,
                vector=embeddings.tolist(),
                payload=payload
            )
            
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            # Report scalar with iteration counter
            Logger.current_logger().report_scalar(
                title="Vector Storage",
                series="Embeddings Size",
                value=len(embeddings),
                iteration=self._embedding_count
            )
            self._embedding_count += 1  
            
            return point_id
        except Exception as e:
            print(f"Error storing embeddings: {str(e)}")
            return None

    def get_collection_info(self):
        try:
            return self.client.get_collection(self.collection_name)
        except Exception as e:
            print(f"Error getting collection info: {str(e)}")
            return None