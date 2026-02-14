// MongoDB initialization script

// Create database
db = db.getSiblingDB('smartcity_unstructured');

// Create collections
db.createCollection('data_ingestion_logs');
db.createCollection('unstructured_data');
db.createCollection('ai_analytics_cache');
db.createCollection('user_sessions');

// Create indexes
db.data_ingestion_logs.createIndex({ "source_id": 1, "ingested_at": -1 });
db.data_ingestion_logs.createIndex({ "source_type": 1 });
db.data_ingestion_logs.createIndex({ "ingested_at": -1 });

db.unstructured_data.createIndex({ "source": 1, "timestamp": -1 });
db.unstructured_data.createIndex({ "tags": 1 });
db.unstructured_data.createIndex({ "metadata.type": 1 });

db.ai_analytics_cache.createIndex({ "query_hash": 1 }, { unique: true });
db.ai_analytics_cache.createIndex({ "created_at": 1 }, { expireAfterSeconds: 86400 }); // TTL 24 hours

db.user_sessions.createIndex({ "user_id": 1, "created_at": -1 });
db.user_sessions.createIndex({ "session_id": 1 }, { unique: true });
db.user_sessions.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 }); // TTL index

print('MongoDB initialization completed');
