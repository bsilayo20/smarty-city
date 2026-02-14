"""
MongoDB database connection and utilities
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from typing import Dict, List, Optional, Any
from loguru import logger
from config import settings


class MongoDB:
    """MongoDB database connection manager"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self._initialize()
    
    def _initialize(self):
        """Initialize MongoDB connection"""
        try:
            connection_string = (
                f"mongodb://{settings.MONGODB_USER}:"
                f"{settings.MONGODB_PASSWORD}@"
                f"{settings.MONGODB_HOST}:"
                f"{settings.MONGODB_PORT}/"
                f"{settings.MONGODB_DB}"
                f"?authSource=admin"
            )
            
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[settings.MONGODB_DB]
            logger.info("MongoDB connection initialized")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Error initializing MongoDB: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error initializing MongoDB: {str(e)}")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a MongoDB collection"""
        return self.db[collection_name]
    
    async def insert_document(
        self,
        collection: str,
        document: Dict[str, Any]
    ) -> str:
        """
        Insert a document into a collection
        
        Args:
            collection: Collection name
            document: Document to insert
            
        Returns:
            Inserted document ID
        """
        try:
            result = self.db[collection].insert_one(document)
            logger.debug(f"Inserted document into {collection}: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document into {collection}: {str(e)}")
            raise
    
    async def insert_many(
        self,
        collection: str,
        documents: List[Dict[str, Any]]
    ) -> List[str]:
        """Insert multiple documents"""
        try:
            result = self.db[collection].insert_many(documents)
            logger.debug(f"Inserted {len(result.inserted_ids)} documents into {collection}")
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            logger.error(f"Error inserting documents into {collection}: {str(e)}")
            raise
    
    async def find_one(
        self,
        collection: str,
        query: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Find one document matching query"""
        try:
            return self.db[collection].find_one(query)
        except Exception as e:
            logger.error(f"Error finding document in {collection}: {str(e)}")
            return None
    
    async def find_many(
        self,
        collection: str,
        query: Dict[str, Any] = None,
        limit: int = 100,
        skip: int = 0,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        try:
            cursor = self.db[collection].find(query or {})
            
            if sort:
                cursor = cursor.sort(sort)
            
            cursor = cursor.skip(skip).limit(limit)
            
            return list(cursor)
        except Exception as e:
            logger.error(f"Error finding documents in {collection}: {str(e)}")
            return []
    
    async def update_one(
        self,
        collection: str,
        query: Dict[str, Any],
        update: Dict[str, Any]
    ) -> bool:
        """Update one document"""
        try:
            result = self.db[collection].update_one(query, {"$set": update})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document in {collection}: {str(e)}")
            return False
    
    async def delete_one(
        self,
        collection: str,
        query: Dict[str, Any]
    ) -> bool:
        """Delete one document"""
        try:
            result = self.db[collection].delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document in {collection}: {str(e)}")
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global instance
mongo_db = MongoDB()
