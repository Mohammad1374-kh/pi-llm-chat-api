# Pi School LLM Chat API

A production-style backend service for an AI-powered chat assistant built with FastAPI.

The system supports authentication, streaming LLM responses, conversation persistence, and multi-provider LLM integration with performance benchmarking.

---

## 🚀 Features

- JWT-based authentication (register/login)
- Streaming chat responses (Server-Sent Events - SSE)
- Persistent conversation history per user
- Multi-provider LLM support (OpenRouter / Groq)
- Token-by-token streaming pipeline
- Latency benchmarking (TTFT, TTLT, tokens/sec)
- Dockerized deployment (single command setup)

---
## 🧱 Architecture Overview

The system follows a layered architecture:

- **API Layer** → FastAPI routes  
- **Service Layer** → Business logic (chat orchestration)  
- **Repository Layer** → Database operations  
- **LLM Layer** → Provider abstraction (OpenRouter, Groq)  
- **Database** → SQLite (SQLAlchemy ORM)

This separation ensures maintainability and scalability.

---

## 🗄️ Database Design

### Tables

**User**
- id
- email
- hashed_password
- created_at

**Conversation**
- id
- user_id
- title
- created_at

**Message**
- id
- conversation_id
- role
- content
- created_at

### Why SQL?

- Strong relational structure (users → conversations → messages)
- Data integrity via foreign keys
- Simple querying and ordering
- Optimized for chat-based retrieval patterns
- Easy migration from SQLite → PostgreSQL

---

## 🔐 Authentication

- JWT-based authentication (HS256)
- Token payload includes user email (`sub`)
- Secure endpoints protected via dependency injection

### Protected Routes

- `POST /chat`
- `GET /chat/history`
- `GET /chat/{conversation_id}`

---

## 🤖 LLM Design (Core System Component)

The system uses a **provider-agnostic LLM abstraction layer**.

### Design Pattern

- Factory Pattern → selects provider dynamically
- Strategy Pattern → each provider implements `stream(prompt)`
- Interface: `LLMProvider`

### Supported Providers

- OpenRouter
- Groq

### Why this design?

- Easily extensible (add new LLMs without modifying service layer)
- Decouples business logic from external APIs
- Enables benchmarking across providers

---

## 💬 Streaming Architecture (SSE)

### Endpoint: `POST /chat`

The chat system uses **Server-Sent Events (SSE)** for real-time streaming.

### Flow:

1. User sends message
2. Conversation is created or loaded
3. Message is stored in DB
4. LLM provider streams tokens
5. Tokens are forwarded instantly to client
6. Final response is saved to database

### Why streaming?

- Lower perceived latency
- Better UX (token-by-token response)
- Enables real-time chat experience

---

## 📊 LLM Benchmarking

The system includes a built-in performance benchmarking module:

### Metrics Collected

- **TTFT (Time To First Token)**  
- **TTLT (Time To Last Token)**  
- **Characters per second**
- Total response length

### Purpose

- Compare LLM providers (Groq vs OpenRouter)
- Evaluate latency differences
- Measure streaming efficiency
- Identify performance bottlenecks

---

## 🧪 Example Benchmark Output

```json
{
  "provider": "groq",
  "ttft_ms": 340.12,
  "ttlt_ms": 410.55,
  "chars_per_sec": 3200.45,
  "chars": 145
}
```

---

## 🐳 Docker Setup

### Build and run

```bash
docker compose up --build
```

### Stop services
```bash
docker compose down
```

## ⚙️ Tech Stack
- FastAPI
- SQLAlchemy ORM
- SQLite
- JWT (python-jose)
- Docker
- Requests
- Groq API
- OpenRouter API

## 📌 Trade-offs & Design Decisions
-  SQLite chosen for simplicity and zero setup overhead
- Streaming prioritized over blocking responses for UX
- No full conversation context sent to LLM (latency optimization)
-  Repository pattern used for clean separation of database logic
- Minimal architecture to prioritize readability and extensibility

## 🧠 Future Improvements
- PostgreSQL migration for production scaling
- Add contextual memory (sliding window / summarization)
- Add retry + circuit breaker for LLM API failures
- Introduce async DB layer (SQLAlchemy async)
- Implement rate limiting and request throttling for authentication and chat endpoints to improve API resilience and cost control

## 📖 API Documentation
Once running:
```bash
http://localhost:8000/docs
```
FastAPI Swagger UI is automatically generated.

