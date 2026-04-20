Pi School LLM Chat API

A minimal backend service for an AI-powered chat assistant built with FastAPI.
The system supports authentication, streaming LLM responses, and persistent conversation history.

🚀 Features
JWT-based authentication (register/login)
Streaming chat responses (Server-Sent Events)
Conversation history per user
Persistent storage using SQLite (SQLAlchemy ORM)
LLM integration via OpenRouter / Groq
Dockerized deployment (single command setup)
🧱 Architecture Overview

The system follows a layered architecture:

API Layer → FastAPI routes
Service Layer → Business logic (chat orchestration)
Repository Layer → Database operations
LLM Layer → Provider abstraction (OpenRouter, Groq)
Database → SQLite (SQLAlchemy ORM)

This separation ensures maintainability and scalability.

🗄️ Database Design
User
id, email, hashed_password, created_at
Conversation
id, user_id, title, created_at
Message
id, conversation_id, role, content, created_at
Why SQL?
Strong relational structure (users → conversations → messages)
Data integrity via foreign keys
Simple querying and ordering
Easy migration from SQLite → PostgreSQL
🔐 Authentication
JWT-based authentication
Token includes user email (sub)
Protected endpoints:
/chat
/chat/history
🤖 LLM Integration

Supports multiple providers:

OpenRouter
Groq

Streaming is implemented token-by-token using Server-Sent Events (SSE).

💬 Chat System
POST /chat
Sends user message
Streams LLM response
Saves conversation + messages in DB
GET /chat/history
Returns all conversations for authenticated user
Includes full message history per conversation
🐳 Docker Setup
Run the project
docker compose up --build
Stop services
docker compose down
⚙️ Tech Stack
FastAPI
SQLAlchemy
SQLite
JWT (python-jose)
Docker
OpenRouter / Groq APIs
📌 Trade-offs & Design Decisions
Used SQLite for simplicity and zero setup
Streaming prioritized over full-response blocking
No full conversation memory sent to LLM (latency + token optimization)
Repository pattern used for separation of concerns
Minimal but extensible architecture
🧠 Future Improvements
Add contextual memory (sliding window / summarization)
PostgreSQL migration
Rate limiting per user
CI pipeline (GitHub Actions)
Request logging & monitoring
▶️ API Docs

Once running:

http://localhost:8000/docs