# src/database/mongo_client.py
from src.rag import get_task
from pymongo import MongoClient
from src.config import MONGO_URI

class MongoDBClient:
    def __init__(self):
        self.task = get_task()
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['rag_database']
        self.collection = self.db['github_repos']
        print("MongoDB connection successful")

    def insert_document(self, data):        
        result = self.collection.insert_one(data)
        self.task.current_task().set_tags([f"Document_{result.inserted_id}"])
        return result  

    def get_all_documents(self):
        return list(self.collection.find())

    def count_documents(self):
        return self.collection.count_documents({})