# Python AI Service Architecture - Quick Reference

## Architecture: Feature-Based Clean Architecture

**Why**: Easy to find code, clear boundaries, easy to add features, scales well

## Structure

```
vamu_ai_service/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                   # Configuration (Pydantic settings)
│   │
│   ├── core/                       # Core domain (shared)
│   │   ├── entities/
│   │   │   ├── prompt.py          # Prompt entity
│   │   │   ├── response.py        # AI Response entity
│   │   │   └── user_context.py    # User context entity
│   │   ├── value_objects/
│   │   │   ├── provider_type.py   # Provider enum
│   │   │   └── model_config.py    # Model configuration
│   │   └── services/
│   │       └── prompt_builder.py  # Shared prompt building
│   │
│   ├── features/                   # Feature modules
│   │   ├── inspiration/           # Inspiration feature
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   └── event_suggestion.py
│   │   │   │   └── services/
│   │   │   │       └── inspiration_prompt_builder.py
│   │   │   ├── application/
│   │   │   │   ├── use_cases/
│   │   │   │   │   └── inspire_me_use_case.py
│   │   │   │   └── ports/
│   │   │   │       └── context_repository.py  # Interface
│   │   │   ├── infrastructure/
│   │   │   │   └── repositories/
│   │   │   │       └── context_repository_impl.py
│   │   │   └── presentation/
│   │   │       ├── schemas.py      # Pydantic models
│   │   │       └── router.py       # FastAPI router
│   │   │
│   │   ├── chatbot/               # Chatbot feature
│   │   └── agent/                  # Agent feature
│   │
│   ├── infrastructure/             # Shared infrastructure
│   │   ├── providers/
│   │   │   ├── base_provider.py   # Abstract base
│   │   │   ├── openai_provider.py
│   │   │   └── anthropic_provider.py
│   │   ├── messaging/
│   │   │   ├── queue_consumer.py   # Redis queue consumer
│   │   │   └── event_publisher.py
│   │   └── cache/
│   │       └── redis_cache.py
│   │
│   └── shared/                     # Shared utilities
│       ├── exceptions.py
│       ├── decorators.py
│       └── utils.py
│
├── tests/
│   ├── unit/features/
│   ├── integration/
│   └── e2e/
│
├── requirements.txt
├── Dockerfile
└── README.md
```

## Feature Structure

Each feature contains all layers:

```
feature_name/
├── domain/              # Business logic (no external deps)
│   ├── entities/       # Domain entities
│   └── services/       # Domain services
│
├── application/         # Use cases
│   ├── use_cases/       # Business use cases
│   └── ports/           # Interfaces (what we need)
│
├── infrastructure/      # External implementations
│   └── repositories/    # Implementations of ports
│
└── presentation/        # API layer
    ├── schemas.py       # Request/Response models
    └── router.py        # FastAPI routes
```

## Key Code Examples

### Core Entities

```python
# app/core/entities/prompt.py
@dataclass
class Prompt:
    content: str
    system_message: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1000
    metadata: Dict[str, Any] = None

# app/core/entities/response.py
@dataclass
class AIResponse:
    content: str
    provider: str
    model: str
    tokens_used: int
    metadata: Dict[str, Any] = None
```

### LLM Provider (Shared Infrastructure)

```python
# app/infrastructure/providers/base_provider.py
class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: Prompt) -> AIResponse:
        pass
    
    @abstractmethod
    async def stream(self, prompt: Prompt):
        pass

# app/infrastructure/providers/openai_provider.py
class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate(self, prompt: Prompt) -> AIResponse:
        # Implementation...
```

### Use Case Example

```python
# app/features/inspiration/application/use_cases/inspire_me_use_case.py
class InspireMeUseCase:
    def __init__(
        self,
        llm_provider: BaseLLMProvider,
        context_repository: ContextRepositoryInterface,
    ):
        self.llm_provider = llm_provider
        self.context_repository = context_repository
    
    async def execute(self, user_id: str) -> List[EventSuggestion]:
        # 1. Get context
        interests = await self.context_repository.get_user_interests(user_id)
        past_events = await self.context_repository.get_past_events(user_id)
        
        # 2. Build prompt
        prompt = InspirationPromptBuilder.build(interests, past_events)
        
        # 3. Generate response
        response = await self.llm_provider.generate(prompt)
        
        # 4. Parse and return
        return self._parse_response(response)
```

### Router Example

```python
# app/features/inspiration/presentation/router.py
router = APIRouter(prefix="/inspiration", tags=["Inspiration"])

@router.post("/inspire", response_model=InspireMeResponse)
async def inspire_me(
    request: InspireMeRequest,
    use_case: InspireMeUseCase = Depends(get_inspire_use_case),
):
    suggestions = await use_case.execute(request.user_id)
    return InspireMeResponse(suggestions=suggestions, ...)
```

### Dependency Injection

```python
# app/presentation/dependencies.py
def get_inspire_use_case() -> InspireMeUseCase:
    llm_provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
    context_repo = ContextRepositoryImpl(api_url=settings.BACKEND_API_URL)
    return InspireMeUseCase(llm_provider=llm_provider, context_repository=context_repo)
```

### Main App Setup

```python
# app/main.py
app = FastAPI(title="VAMU AI Service")

app.include_router(inspiration_router)
app.include_router(chatbot_router)
app.include_router(agent_router)
```

## Key Principles

1. **Features are self-contained** - Each feature has all layers (domain → application → infrastructure → presentation)
2. **Shared infrastructure** - Providers, queue, cache shared across features
3. **Core domain** - Shared entities and value objects
4. **Dependency injection** - Use FastAPI dependencies
5. **Ports & Adapters** - Interfaces in application layer, implementations in infrastructure

## Benefits

- ✅ Easy to find code (all inspiration code in `features/inspiration/`)
- ✅ Clear feature boundaries
- ✅ Easy to add new features (copy structure, implement)
- ✅ Better for teams (each feature is self-contained)
- ✅ Scales well

## Adding a New Feature

1. Create `app/features/new_feature/`
2. Add `domain/`, `application/`, `infrastructure/`, `presentation/` folders
3. Implement use case in `application/use_cases/`
4. Add router in `presentation/router.py`
5. Register router in `app/main.py`

## Configuration

```python
# app/config.py
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str = ""
    DEFAULT_PROVIDER: str = "openai"
    BACKEND_API_URL: str = "http://localhost:3000"
    REDIS_URL: str = "redis://localhost:6379"
```

## Quick Commands

```bash
# Start service
uvicorn app.main:app --reload --port 8001

# Run tests
pytest tests/

# Format code
black app/
```

This architecture keeps code organized, testable, and easy to extend.
