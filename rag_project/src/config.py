import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "mongodb://localhost:27017/?authSource=admin"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

GITHUB_REPOS = [
    'https://github.com/ros-infrastructure/www.ros.org',
    'https://github.com/ros-navigation/docs.nav2.org',
    'https://github.com/moveit/moveit2',
    'https://github.com/gazebosim/gz-sim'
]

YOUTUBE_URLS = [
    'https://www.youtube.com/watch?v=UBhG_UMuFEo',
    'https://www.youtube.com/watch?v=Gg25GfA456o',
    'https://www.youtube.com/watch?v=GHb6Wr_exxI'
]

EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
VECTOR_SIZE = 384