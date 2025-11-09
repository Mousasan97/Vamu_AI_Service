# VAMU System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Flutter Mobile App                         │
│  - iOS & Android                                             │
│  - HTTP REST API                                             │
│  - WebSocket (Real-time)                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│            TypeScript Backend (NestJS)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Auth   │  │  Users   │  │  Events  │  │   AI     │  │
│  │ Module  │  │ Module   │  │ Module   │  │ Module   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌─────────┐         ┌─────────┐         ┌─────────┐
    │PostgreSQL│         │  Redis  │         │   S3    │
    └─────────┘         └─────────┘         └─────────┘
                            ↓ Queue
┌─────────────────────────────────────────────────────────────┐
│         Python AI Service (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Features: Inspiration | Chatbot | Agent            │   │
│  │  Architecture: Feature-Based Clean Architecture      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓
    ┌─────────┐         ┌─────────┐
    │ OpenAI  │         │Anthropic│
    └─────────┘         └─────────┘
```

## Components

### 1. Flutter Mobile App
- **Platform**: iOS & Android
- **Communication**: 
  - HTTP REST API for standard requests
  - WebSocket for real-time updates (AI results, notifications)
- **Features**: Events, Users, AI-powered features

### 2. TypeScript Backend (NestJS)
- **Architecture**: Modular Monolith
- **Framework**: NestJS with TypeScript
- **Modules**: Auth, Users, Events, AI (client)
- **Database**: PostgreSQL with PostGIS
- **Cache/Queue**: Redis (BullMQ for background jobs)
- **Storage**: S3-compatible storage
- **Real-time**: Socket.IO (WebSocket)

### 3. Python AI Service (FastAPI)
- **Architecture**: Feature-Based Clean Architecture
- **Framework**: FastAPI
- **Features**: Inspiration, Chatbot, Agent
- **Providers**: OpenAI, Anthropic (easily swappable)
- **Communication**: 
  - HTTP REST (synchronous)
  - Redis Queue (asynchronous)
  - WebSocket (streaming)

## Communication Patterns

### Pattern 1: Synchronous HTTP
```
Flutter App → TypeScript API → Python AI Service → LLM Provider
                ↓                    ↓                    ↓
            Return Result ← JSON Response ← AI Response
```
**Use for**: Quick operations (< 5 seconds)

### Pattern 2: Async Queue (Recommended)
```
Flutter App → TypeScript API → Queue Job → Return Immediately
                                    ↓
                            Python AI Service Processes
                                    ↓
                            Store Result → Notify via WebSocket
```
**Use for**: Long AI operations (> 5 seconds)

### Pattern 3: WebSocket Streaming
```
Flutter App ← WebSocket ← TypeScript API ← Python AI Service
                ↓              ↓                    ↓
            Stream Chunks ← Stream ← LLM Stream
```
**Use for**: Chat, real-time generation

## Architecture Patterns

### TypeScript Backend
- **Modular Monolith**: Clear domain boundaries, easy to extract later
- **Event-Driven**: Async processing for AI operations
- **CQRS**: Separate read/write operations (optional)

### Python AI Service
- **Feature-Based Clean Architecture**: Organized by features (inspiration, chatbot, agent)
- **Hexagonal Architecture**: Clean boundaries, provider independence
- **Ports & Adapters**: Easy to swap LLM providers

## Data Flow Example: AI Inspiration

```
1. User taps "Inspire Me" in Flutter app
   ↓
2. Flutter → POST /v1/ai/inspire → TypeScript API
   ↓
3. TypeScript API queues job → Returns job ID immediately
   ↓
4. Redis Queue → Python AI Service consumes job
   ↓
5. Python AI Service:
   - Gets user context from TypeScript API
   - Builds prompt
   - Calls LLM (OpenAI/Anthropic)
   - Processes response
   ↓
6. Stores result in PostgreSQL (via TypeScript API)
   ↓
7. Notifies Flutter app via WebSocket: "inspiration-ready"
   ↓
8. Flutter app fetches result and displays to user
```

## Technology Stack

### Flutter App
- Framework: Flutter (Dart)
- State Management: Provider/Riverpod
- HTTP: Dio
- WebSocket: Socket.IO client

### TypeScript Backend
- Framework: NestJS
- Language: TypeScript
- Database: PostgreSQL + PostGIS
- ORM: Prisma
- Cache/Queue: Redis + BullMQ
- Storage: S3-compatible
- Real-time: Socket.IO

### Python AI Service
- Framework: FastAPI
- Language: Python 3.11+
- AI Libraries: OpenAI SDK, Anthropic SDK, LangChain
- Queue: Redis (consumes from BullMQ)
- Architecture: Feature-Based Clean Architecture

## Key Architectural Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| **Backend Architecture** | Modular Monolith | Team size, simplicity, easy to extract later |
| **AI Service** | Separate Python Service | Best tools, independent scaling |
| **AI Communication** | Queue + HTTP + WebSocket | Right tool for each use case |
| **Python Architecture** | Feature-Based Clean | Easy to find code, clear boundaries |
| **Async Processing** | Event-Driven | Better UX, scalability |

## Benefits

1. **Scalability**: Each component scales independently
2. **Performance**: Async processing, no blocking
3. **UX**: Immediate responses, background processing
4. **Cost**: Optimize AI calls separately
5. **Maintainability**: Clear boundaries, testable
6. **Flexibility**: Easy to add new AI features

## Deployment

### Development
- All services run locally
- Docker Compose for PostgreSQL, Redis
- TypeScript API: `npm run start:api`
- Python AI: `uvicorn app.main:app --reload`

### Production
- Flutter app: App Store / Play Store
- TypeScript API: Deploy separately (scales horizontally)
- Python AI Service: Deploy separately (scales independently)
- Database: Managed PostgreSQL
- Redis: Managed Redis
- Storage: S3

## Detailed Documentation

- **TypeScript Backend**: See `DOCUMENTATION.md`
- **AI Architecture**: See `AI_ARCHITECTURE.md`
- **Python AI Structure**: See `PYTHON_AI_ARCHITECTURE.md`
- **Clean Architecture**: See `AI_CLEAN_ARCHITECTURE.md`

## Quick Reference

**Start Development:**
```bash
# Backend
docker-compose up -d
npm run prisma:migrate
npm run start:api

# AI Service
cd vamu_ai_service
uvicorn app.main:app --reload --port 8001
```

**Communication:**
- TypeScript API: `http://localhost:3000`
- Python AI Service: `http://localhost:8001`
- WebSocket: `ws://localhost:3000`

This architecture scales with your needs and keeps all systems maintainable and independent.
