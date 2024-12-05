import unittest
from src.rag import get_task
from src.config import GITHUB_REPOS
from src.etl.data_processor import DataProcessor
from src.database.mongo_client import MongoDBClient
from src.config import YOUTUBE_URLS
from src.database.qdrant_client import QdrantDBClient

def test_pipeline():
    task = get_task()
    processor = DataProcessor()
    mongo_client = MongoDBClient()
    qdrant_client = QdrantDBClient()

    # Process each repository
    for repo_url in GITHUB_REPOS:
        print(f"\nProcessing {repo_url}")
        success = processor.process_repo(repo_url)
        if success:
            print("Successfully processed repository")
        else:
            print("Failed to process repository")

    # Process each YouTube URL
    for url in YOUTUBE_URLS:
        print(f"\nProcessing {url}")
        success = processor.process_youtube(url)

    # Verify results
    print("\nVerification:")
    print(f"Documents in MongoDB: {mongo_client.count_documents()}")
    
    try:
        collection_stats = qdrant_client.client.get_collection(qdrant_client.collection_name)
        print(f"Vectors in Qdrant collection '{qdrant_client.collection_name}': {collection_stats.points_count}")
    except Exception as e:
        print(f"Error getting Qdrant statistics: {str(e)}")

if __name__ == "__main__":
    test_pipeline()