from pymongo import MongoClient
from app.config.config import MONGODB_URI, MONGODB_DB_NAME

def get_mongodb_client():
    """
    Returns a MongoDB client instance.
    """
    try:
        client = MongoClient(MONGODB_URI)
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB successfully!")
        return client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

def get_database():
    """
    Returns the database instance.
    """
    client = get_mongodb_client()
    return client[MONGODB_DB_NAME]

def get_collection(collection_name):
    """
    Returns a specific collection from the database.
    
    Args:
        collection_name (str): Name of the collection
        
    Returns:
        pymongo.collection.Collection: MongoDB collection
    """
    db = get_database()
    return db[collection_name] 