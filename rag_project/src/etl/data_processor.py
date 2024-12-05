from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL
from src.database.mongo_client import MongoDBClient
from src.database.qdrant_client import QdrantDBClient
from src.etl.github_scraper import GitHubScraper
from src.etl.github_scraper import ContentScraper
from src.config import YOUTUBE_URLS
from src.rag import get_task, Logger



class DataProcessor:
    def __init__(self):
        self.task = get_task()
        self.scraper = GitHubScraper()
        self.content_scraper = ContentScraper()
        self.mongo_client = MongoDBClient()
        self.qdrant_client = QdrantDBClient()
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    def process_repo(self, repo_url):
        self.task.get_logger().report_text(f"Processing repository: {repo_url}")
        # Scrape repository
        data = self.scraper.scrape_repo(repo_url)
        if not data:
            return False

        # Store in MongoDB
        mongo_result = self.mongo_client.insert_document(data)
        Logger.current_logger().report_scalar(
        title="Document Processing",
        series="Documents Processed",
        value=self.mongo_client.count_documents(),
        iteration=0
    )
        # Process each file
        for file in data['files']:
            try:
                # Create embeddings for the file content
                embeddings = self.embedding_model.encode(file['content'])
                
                # Prepare payload
                payload = {
                    'url': data['url'],
                    'path': file['path'],
                    'mongo_id': str(mongo_result.inserted_id)
                }
                
                # Store in Qdrant
                self.qdrant_client.store_embeddings(
                    id=file['sha'],  
                    embeddings=embeddings,
                    payload=payload
                )
            except Exception as e:
                print(f"Error processing file {file['path']}: {str(e)}")
                continue
        
        return True
    
    def process_youtube(self, url):
        self.task.get_logger().report_text(f"Processing youtube: {url}")
        if 'youtube.com' in url or 'youtu.be' in url:
            data = self.content_scraper.get_youtube_transcript(url)
        else:
            data = self.scraper.scrape_repo(url)
            
        if data:
            # Store in MongoDB and create embeddings as before
            self.store_and_embed(data)

    def store_and_embed(self, data):
        # Store in MongoDB
        mongo_result = self.mongo_client.insert_document(data)
        
        # Create embeddings
        embeddings = self.embedding_model.encode(data['content'])
        
        # Prepare payload
        payload = {
            'url': data['url'],
            'mongo_id': str(mongo_result.inserted_id)
        }

        # Store in Qdrant
        self.qdrant_client.store_embeddings(
            id=data['url'],
            embeddings=embeddings,
            payload=payload
        )
