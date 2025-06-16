# HSK Chatbot

A Vietnamese language chatbot application built with LangChain, LangGraph, and FastAPI.

## Features

- Interacts with users in Vietnamese
- Supports both simple chain-based and graph-based conversation patterns
- Can switch between OpenAI and Google Gemini models
- Persists chat history in MongoDB
- Semantic retrieval using Qdrant vector database for relevant context
- Optional LangSmith tracing for debugging and analytics

## Architecture

The application follows a layered architecture pattern for better organization and extensibility:

```
hsk-chatbot/
├── app/                       # Application package
│   ├── api/                   # API layer
│   │   └── routes.py          # API routes
│   │   └── chat.py            # Chat-related schemas
│   ├── core/                  # Core modules
│   │   ├── config.py          # Configuration settings
│   │   ├── init.py            # Application initialization
│   │   └── langsmith.py       # LangSmith integration
│   ├── repositories/          # Data access layer
│   │   ├── mongodb.py         # MongoDB client
│   │   └── chat_session.py    # Chat session repository
│   ├── schemas/               # Data models (Pydantic)
│   ├── services/              # Business logic layer
│   │   ├── chat.py            # Chat service
│   │   ├── llm.py             # LLM model service
│   │   └── memory.py          # Memory management service
│   ├── chains/                # LangChain chains
│   │   └── simple_chat_chain.py  # Simple chat chain
│   ├── graph/                 # LangGraph components
│   │   └── chat_graph.py      # Chat graph
│   ├── models/                # Model definitions
│   ├── data/                  # Data files
│   └── utils/                 # Utility functions
├── requirements.txt           # Dependencies
├── run.py                     # Application entry point
├── Dockerfile                 # Docker configuration
└── docker-compose.yml         # Docker Compose configuration
```

## Design Patterns

This project implements several design patterns to make it more extensible:

1. **Repository Pattern**: Separates data access logic from business logic.
2. **Factory Pattern**: Creates objects without specifying their concrete classes.
3. **Dependency Injection**: Components receive dependencies rather than creating them.
4. **Service Layer**: Implements business logic independent of the API layer.
5. **Application Factory**: Creates the application with all necessary configurations.

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB
- OpenAI API key and/or Google API key

### Environment Variables

Create a `.env` file with the following variables:

```
# Database settings
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=hsk_chatbot

# Qdrant settings
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=hsk-chatbot

# LLM API settings
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
DEFAULT_MODEL_PROVIDER=openai  # or gemini

# LangSmith settings (optional)
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=hsk-chatbot
LANGSMITH_TRACING=false
```

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hsk-chatbot.git
   cd hsk-chatbot
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python run.py
   ```

### Using Docker

You can also run the application using Docker:

```
docker-compose up
```

## API Endpoints

- `GET /api/` - Root endpoint
- `POST /api/chat` - Chat endpoint
- `GET /api/health` - Health check endpoint

### Chat Request Schema

```json
{
  "user_input": "Xin chào",
  "session_id": "optional-session-id",
  "model_provider": "openai",
  "use_graph": true
}
```

### Chat Response Schema

```json
{
  "response": {
    "output": "Xin chào! Tôi có thể giúp gì cho bạn?",
    "other_fields": "..."
  },
  "session_id": "session-id"
}
```

## Extending the Application

### Adding a New Model Provider

1. Add the new provider in `app/services/llm.py`
2. Update the factory function to support the new provider

### Adding New Chat Patterns

1. Create a new module in `app/chains/` or `app/graph/`
2. Implement the new pattern
3. Add a new method in `app/services/chat.py`
4. Update the API routes to support the new pattern

## License

[MIT License](LICENSE)

## Setting up Qdrant

This application uses Qdrant as a vector database for semantic search of chat history.

1. You can use the built-in Qdrant service in docker-compose
2. Or install Qdrant locally following instructions at [Qdrant](https://qdrant.tech/documentation/quick-start/)
3. If you're using a hosted Qdrant service, add your API key to the `.env` file as `QDRANT_API_KEY`

The application will automatically create the necessary collections on first run. By default, it connects to the local Qdrant instance at http://localhost:6333.

## How Semantic Retrieval Works

Instead of just retrieving the most recent messages, this chatbot:

1. Embeds the user's query using the sentence-transformers model
2. Searches the vector store for semantically similar previous messages
3. Retrieves the most relevant context based on the current question
4. Combines recent messages with semantically relevant ones
5. Passes this optimized context to the LLM for a more informed response

This allows the chatbot to provide more consistent and relevant responses by maintaining context across the conversation, even when discussing topics from earlier in the chat history. 