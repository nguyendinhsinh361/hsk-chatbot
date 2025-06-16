# Migration Guide: Pinecone to Qdrant

This guide explains how to migrate from Pinecone to Qdrant as the vector database for the HSK Chatbot.

## Changes Made

1. **Dependencies**:
   - Removed `langchain_pinecone` and `pinecone-client`
   - Added `langchain_qdrant` and `qdrant-client`

2. **Configuration**:
   - Replaced Pinecone environment variables with Qdrant ones:
     - `PINECONE_API_KEY` → `QDRANT_API_KEY`
     - `PINECONE_ENVIRONMENT` → `QDRANT_URL`
     - `PINECONE_INDEX_NAME` → `QDRANT_COLLECTION_NAME`

3. **Vector Store Implementation**:
   - Updated `app/models/vector_store.py` to use Qdrant instead of Pinecone
   - Changed the initialization process to create Qdrant collections instead of Pinecone indexes
   - Updated the filter format for Qdrant's search

4. **Docker Compose**:
   - Added a Qdrant service to the docker-compose.yml file
   - Added a persistent volume for Qdrant data

## Migration Steps

1. **Update Environment Variables**:
   Update your `.env` file to replace Pinecone variables with Qdrant ones:
   ```
   # Remove these lines
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=gcp-starter
   PINECONE_INDEX_NAME=hsk-chatbot
   
   # Add these lines
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=
   QDRANT_COLLECTION_NAME=hsk-chatbot
   ```

2. **Install New Dependencies**:
   ```bash
   pip uninstall langchain_pinecone pinecone-client
   pip install langchain_qdrant qdrant-client
   ```

3. **Start Qdrant**:
   You can either:
   - Use the Docker Compose setup: `docker-compose up -d qdrant`
   - Install Qdrant locally following the [official documentation](https://qdrant.tech/documentation/quick-start/)
   - Use a hosted Qdrant service

4. **Run the Application**:
   ```bash
   # With Docker
   docker-compose up
   
   # Without Docker
   python run.py
   ```

## Notes

- The application will automatically create the necessary collections in Qdrant on first run
- Existing vector data from Pinecone will not be migrated automatically
- If you need to migrate existing vectors, you'll need to implement a migration script to:
  1. Retrieve all vectors from Pinecone
  2. Insert them into Qdrant with the same metadata

## Advantages of Qdrant

- Can be run locally or self-hosted
- No API key required for local instances
- More flexible filtering capabilities
- Better performance for many use cases
- Active open-source development 