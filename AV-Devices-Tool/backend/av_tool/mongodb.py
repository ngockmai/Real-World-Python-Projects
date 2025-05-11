from pymongo import MongoClient
from django.conf import settings
import logging
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)

def get_mongodb_connection():
    """
    Create and return a MongoDB connection using settings from Django settings
    """
    try:
        client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000  # 5 second timeout
        )
        # Verify the connection
        client.server_info()
        return client[settings.MONGODB_DB_NAME]
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

def get_collection(collection_name):
    """
    Get a specific collection from the MongoDB database
    """
    try:
        db = get_mongodb_connection()
        return db[collection_name]
    except Exception as e:
        logger.error(f"Failed to get collection {collection_name}: {str(e)}")
        raise

# Create a default connection
try:
    db = get_mongodb_connection()
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to establish default MongoDB connection: {str(e)}")
    db = None 