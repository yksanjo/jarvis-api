# Jarvis API - Standalone Backend Service

A standalone REST API server for Jarvis AI assistant. Can be used by all Jarvis clients (CLI, Widget, Mobile, Web).

## Features

- 🌐 **REST API** - Full RESTful endpoints
- 📝 **Tasks API** - CRUD operations for tasks
- 📅 **Events API** - Calendar event management
- 🤖 **AI Chat** - Ollama LLM integration
- 🔒 **Local Only** - No external dependencies
- ⚡ **Fast** - Built with FastAPI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Start the server
python main.py

# Server runs on http://localhost:8000
# API docs at http://localhost:8000/docs
```

## API Endpoints

### Tasks
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Events
- `GET /api/events` - List events
- `POST /api/events` - Create event
- `DELETE /api/events/{id}` - Delete event

### Chat
- `POST /api/chat` - Chat with AI
- `GET /api/llm/status` - Check LLM status

## Docker

```bash
docker build -t jarvis-api .
docker run -p 8000:8000 jarvis-api
```

## Requirements

- Python 3.9+
- FastAPI
- Ollama (optional, for AI features)

## License

MIT
