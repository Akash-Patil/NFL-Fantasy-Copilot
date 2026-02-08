# FastAPI Mastery Guide for Building a Smart LLM Router

**You can build a production-ready LLM router with FastAPI in 4-6 weeks** by following this interactive, project-focused learning path. FastAPI's async-first design, automatic validation through Pydantic, and built-in OpenAPI documentation make it ideal for LLM orchestration—where you need non-blocking API calls, strict request/response contracts, and easy testing. This guide skips unnecessary theory and focuses on exactly what you need: async endpoints for LLM calls, conversation state management, dependency injection for clean architecture, and Docker deployment.

---

## Start here: your first FastAPI endpoint in 10 minutes

Before diving into concepts, get something running. FastAPI's magic becomes obvious when you see it work.

**Install and create your first endpoint:**

```bash
pip install "fastapi[standard]" uvicorn httpx
```

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-4"

class ChatResponse(BaseModel):
    response: str
    model_used: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Placeholder - you'll add LLM logic here
    return ChatResponse(
        response=f"Echo: {request.message}",
        model_used=request.model
    )
```

**Run it:**
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` and you'll see interactive API documentation generated automatically. This is FastAPI's superpower—type hints become validation, documentation, and IDE support simultaneously.

---

## The four concepts that power your LLM router

FastAPI has many features, but your router project depends on four core concepts. Master these deeply; the rest you can learn as needed.

### 1. Async/await determines your router's throughput

LLM APIs have high latency (**2-30 seconds per call**). Without async, your server blocks during each call. With async, it handles hundreds of concurrent requests on a single thread. This distinction is critical for a router that orchestrates multiple LLM calls.

**The decision framework is simple:**

| Scenario | Use | Why |
|----------|-----|-----|
| Calling LLM APIs (httpx, openai) | `async def` | Non-blocking I/O with `await` |
| Sync-only libraries (some DB drivers) | `def` | FastAPI runs these in a thread pool |
| CPU-heavy computation | `def` or `run_in_executor` | Doesn't benefit from async |
| Unsure | `def` | Safe default; FastAPI handles it |

**Critical mistake to avoid—blocking the event loop:**

```python
# ❌ TERRIBLE - Blocks entire server for 10 seconds
@app.get("/bad")
async def bad_endpoint():
    import time
    time.sleep(10)  # All other requests wait!
    return {"status": "done"}

# ✅ CORRECT - Non-blocking
@app.get("/good")
async def good_endpoint():
    import asyncio
    await asyncio.sleep(10)  # Other requests process normally
    return {"status": "done"}
```

**For your LLM router, use httpx for async HTTP calls:**

```python
import httpx

async def call_openai(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]},
            timeout=60.0
        )
        return response.json()["choices"][0]["message"]["content"]
```

**Concurrent LLM calls with `asyncio.gather`:**

```python
async def route_to_multiple_models(prompt: str):
    results = await asyncio.gather(
        call_openai(prompt),
        call_anthropic(prompt),
        call_local_model(prompt)
    )
    return {"openai": results[0], "anthropic": results[1], "local": results[2]}
```

### 2. Pydantic models enforce your API contract

Every request and response in your router should flow through Pydantic models. They provide validation, serialization, and documentation in one place.

**Pattern for LLM router requests:**

```python
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional

class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"

class Message(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1, max_length=100000)

class RouterRequest(BaseModel):
    messages: list[Message]
    preferred_provider: ModelProvider | None = None
    max_tokens: int = Field(default=1000, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0, le=2)
    
    @field_validator("messages")  # doubt here, pydantic way for checking for messages
    @classmethod
    def validate_messages_not_empty(cls, v):
        if not v:
            raise ValueError("At least one message required")
        return v

class RouterResponse(BaseModel):
    response: str
    provider_used: ModelProvider
    tokens_used: int
    latency_ms: float
```

**Separate models for input vs output (security best practice):**

```python
# Never return internal data accidentally
class ConversationInDB(BaseModel):
    id: str
    messages: list[Message]
    api_key_hash: str  # Internal only!
    
class ConversationResponse(BaseModel):
    id: str
    messages: list[Message]
    # api_key_hash excluded from response

@app.get("/conversations/{conv_id}", response_model=ConversationResponse)
async def get_conversation(conv_id: str):
    # Even if you return ConversationInDB, FastAPI filters to ConversationResponse
    return await db.get_conversation(conv_id)
```

### 3. Dependency injection structures your router cleanly

Dependencies in FastAPI handle cross-cutting concerns: database connections, authentication, configuration, and shared services. For an LLM router, they're essential for managing API clients and conversation state.

**Core pattern with `Depends`:**

```python
from fastapi import Depends
from typing import Annotated

# Dependency function
async def get_llm_client():
    client = LLMRouter(
        openai_key=settings.OPENAI_KEY,
        anthropic_key=settings.ANTHROPIC_KEY
    )
    return client

# Type alias for reuse
LLMClient = Annotated[LLMRouter, Depends(get_llm_client)]

@app.post("/chat")
async def chat(request: ChatRequest, llm: LLMClient):
    return await llm.route(request)
```

**Managing conversation state with dependencies:**

```python
from fastapi import HTTPException

class ConversationStore:
    def __init__(self):
        self.conversations: dict[str, list[Message]] = {}
    
    def get(self, conv_id: str) -> list[Message]:
        return self.conversations.get(conv_id, [])
    
    def append(self, conv_id: str, message: Message):
        if conv_id not in self.conversations:
            self.conversations[conv_id] = []
        self.conversations[conv_id].append(message)

# Singleton store (in production, use Redis or database)
store = ConversationStore()

def get_store() -> ConversationStore:
    return store

async def get_conversation(
    conv_id: str,
    store: ConversationStore = Depends(get_store)
) -> list[Message]:
    messages = store.get(conv_id)
    if not messages:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return messages

@app.post("/conversations/{conv_id}/messages")
async def add_message(
    conv_id: str,
    message: Message,
    history: list[Message] = Depends(get_conversation),
    store: ConversationStore = Depends(get_store),
    llm: LLMClient = Depends(get_llm_client)
):
    store.append(conv_id, message)
    response = await llm.chat(history + [message])
    store.append(conv_id, Message(role="assistant", content=response))
    return {"response": response}
```

**Dependencies with cleanup (database sessions):**

```python
async def get_db():
    db = AsyncSession()
    try:
        yield db  # Injected into endpoint
    finally:
        await db.close()  # Always runs, even on errors
```

### 4. Request handling patterns for router endpoints

Your LLM router needs several request patterns: path parameters for conversation IDs, query parameters for options, and body parameters for messages.

**Combined parameters example:**

```python
@app.post("/v1/conversations/{conv_id}/chat")
async def chat_in_conversation(
    conv_id: str,                                    # Path parameter
    request: ChatRequest,                            # Body (Pydantic model)
    stream: bool = False,                            # Query parameter
    x_request_id: str | None = Header(default=None), # Header
    llm: LLMClient = Depends(get_llm_client)         # Dependency
):
    if stream:
        return StreamingResponse(llm.stream_chat(request))
    return await llm.chat(request)
```

**Streaming responses for LLM output:**

```python
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        async for chunk in llm.stream_response(request):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"
    
    return EventSourceResponse(generate())
```

---

## Project structure for your LLM router

Organize by domain, not by file type. Each module contains everything related to that feature.

```
smart-router/
├── app/
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Settings via Pydantic BaseSettings
│   ├── dependencies.py         # Shared dependencies
│   │
│   ├── router/                 # Core routing logic
│   │   ├── router.py           # /route endpoints
│   │   ├── schemas.py          # Request/response models
│   │   ├── service.py          # Routing algorithm logic
│   │   └── providers/          # LLM provider integrations
│   │       ├── base.py
│   │       ├── openai.py
│   │       ├── anthropic.py
│   │       └── local.py
│   │
│   ├── conversations/          # Conversation management
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── models.py           # DB models if using SQLAlchemy
│   │
│   └── health/                 # Health checks
│       └── router.py
│
├── tests/
│   ├── conftest.py             # Shared fixtures
│   ├── test_router.py
│   └── test_conversations.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

**main.py ties it together:**

```python
from fastapi import FastAPI
from app.router.router import router as routing_router
from app.conversations.router import router as conv_router
from app.health.router import router as health_router

app = FastAPI(title="Smart LLM Router", version="1.0.0")

app.include_router(routing_router, prefix="/v1/route", tags=["routing"])
app.include_router(conv_router, prefix="/v1/conversations", tags=["conversations"])
app.include_router(health_router, prefix="/health", tags=["health"])
```

**Configuration with Pydantic Settings:**

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    redis_url: str = "redis://localhost:6379"
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Testing your router with pytest

Testing FastAPI apps is straightforward. The `TestClient` handles async internally, so your test functions stay synchronous.

**Basic test setup:**

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_llm_client

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_llm_client():
    class MockLLM:
        async def chat(self, request):
            return {"response": "Mock response", "provider": "mock"}
    return MockLLM()

@pytest.fixture
def client_with_mock(mock_llm_client):
    app.dependency_overrides[get_llm_client] = lambda: mock_llm_client
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

**Testing endpoints:**

```python
# tests/test_router.py
def test_chat_endpoint(client_with_mock):
    response = client_with_mock.post(
        "/v1/route/chat",
        json={"messages": [{"role": "user", "content": "Hello"}]}
    )
    assert response.status_code == 200
    assert "response" in response.json()

def test_validation_error(client):
    response = client.post(
        "/v1/route/chat",
        json={"messages": []}  # Empty messages should fail
    )
    assert response.status_code == 422  # Validation error

def test_conversation_not_found(client):
    response = client.get("/v1/conversations/nonexistent")
    assert response.status_code == 404
```

**Testing async code with httpx:**

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/v1/route/chat",
            json={"messages": [{"role": "user", "content": "Test"}]}
        )
        assert response.status_code == 200
```

---

## Docker setup for development and deployment

**Development Dockerfile:**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**docker-compose.yml for development:**

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app  # Hot reload
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**Production Dockerfile with multi-stage build:**

```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Production stage
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY ./app /app/app

# Run as non-root user
RUN adduser --disabled-password appuser
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

## LangChain integration patterns

LangChain adds memory, chains, and agents. Integrate it with FastAPI using async methods.

**Basic LangChain integration:**

```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

class LangChainRouter:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        self.memories: dict[str, ConversationBufferMemory] = {}
    
    def get_memory(self, conv_id: str) -> ConversationBufferMemory:
        if conv_id not in self.memories:
            self.memories[conv_id] = ConversationBufferMemory()
        return self.memories[conv_id]
    
    async def chat(self, conv_id: str, message: str) -> str:
        memory = self.get_memory(conv_id)
        chain = ConversationChain(llm=self.llm, memory=memory)
        response = await chain.ainvoke({"input": message})
        return response["response"]

# Dependency
langchain_router = LangChainRouter()

def get_langchain() -> LangChainRouter:
    return langchain_router

@app.post("/langchain/chat/{conv_id}")
async def langchain_chat(
    conv_id: str,
    request: ChatRequest,
    lc: LangChainRouter = Depends(get_langchain)
):
    response = await lc.chat(conv_id, request.message)
    return {"response": response}
```

---

## Common mistakes and how to avoid them

These errors cause real production issues. Learn them upfront.

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using `requests` in async | Blocks event loop | Use `httpx.AsyncClient` |
| `time.sleep()` in async | Blocks all requests | Use `asyncio.sleep()` |
| No `response_model` | May leak internal data | Always specify response model |
| Single uvicorn worker | Uses only 1 CPU | Use `--workers 4` in production |
| Not mocking dependencies | Slow, flaky tests | Use `app.dependency_overrides` |
| Sync database calls in async | Blocks event loop | Use async drivers (asyncpg) |
| Missing CORS middleware | Frontend can't connect | Add CORSMiddleware |
| Returning Pydantic objects with matching response_model | Double serialization | Return dict or don't use response_model |

---

## Learning milestones and checkpoints

Track your progress through these concrete milestones:

**Week 1-2: Core fundamentals**
- [ ] Create endpoint that echoes input with Pydantic validation
- [ ] Implement async endpoint that calls external API with httpx
- [ ] Add path, query, and body parameters to single endpoint
- [ ] Explore `/docs` and understand auto-generated OpenAPI

**Week 3: Dependency injection and state**
- [ ] Create dependency for configuration settings
- [ ] Implement in-memory conversation store with dependency
- [ ] Add dependency that validates conversation exists
- [ ] Chain multiple dependencies together

**Week 4: Testing and error handling**
- [ ] Set up pytest with TestClient
- [ ] Mock external LLM calls with dependency overrides
- [ ] Add custom exception handlers for domain errors
- [ ] Test validation errors return 422

**Week 5: Integration and streaming**
- [ ] Integrate real LLM API (OpenAI or Anthropic)
- [ ] Implement streaming response endpoint
- [ ] Add LangChain conversation memory
- [ ] Test full conversation flow

**Week 6: Production readiness**
- [ ] Containerize with Docker and docker-compose
- [ ] Add health check endpoint
- [ ] Configure logging middleware
- [ ] Run with multiple workers and test concurrency

---

## Essential resources for deeper learning

**Official documentation** at fastapi.tiangolo.com covers everything—work through the Tutorial section chapter by chapter. It's designed as a progressive learning path and includes tested, runnable code examples.

**FastAPI Interactive** (fastapiinteractive.com) lets you write and test code in your browser with instant feedback—ideal for practicing concepts without local setup.

**GitHub repository zhanymkanov/fastapi-best-practices** (14.1k+ stars) compiles production patterns from real applications, including project structure, async patterns, and security practices.

For LLM-specific patterns, explore **wassim249/fastapi-langgraph-agent-production-ready-template** and **Coding-Crashkurse/Advanced-LangChain-with-FastAPI** for async vector stores and streaming implementations.

---

## Conclusion

Building your smart LLM router requires mastering four concepts deeply: async/await for concurrent LLM calls, Pydantic for request validation, dependency injection for clean architecture, and proper request handling patterns. Start with a working endpoint today, then add complexity incrementally. Focus on the patterns that appear repeatedly—async HTTP clients, conversation state dependencies, streaming responses—and you'll have a production-ready router within weeks. The official documentation remains your best reference; return to it whenever you need details beyond this guide.