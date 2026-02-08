# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fantasy Copilot is a full-stack AI-powered NFL fantasy football player comparison tool. It uses the Perplexity API for analysis and Redis for optional response caching.

## Tech Stack

- **Frontend**: React 18 + Vite + Axios (port 3000)
- **Backend**: FastAPI + Python 3.13+ (port 8000)
- **AI**: Perplexity API (sonar model)
- **Cache**: Redis (optional, gracefully degrades)

## Development Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev      # Dev server at localhost:3000
npm run build    # Production build to dist/
```

### Redis (optional)
```bash
docker-compose up -d redis
```

## Environment Variables

### Backend (.env)
- `PERPLEXITY_API_KEY` - Required
- `REDIS_HOST`, `REDIS_PORT` - Redis connection (optional)
- `CACHE_ENABLED`, `CACHE_TTL_SECONDS` - Cache settings

### Frontend (.env)
- `VITE_API_URL` - Backend URL (default: http://localhost:8000)

## Architecture

### Request Flow
```
Frontend Form → POST /start-sit → Check Cache → Generate Position Prompt → Perplexity API → Parse Response → Store Cache → Return
```

### Position-Based Routing
The backend routes requests by position (WR, QB, RB, TE). Each position has:
- **Prompt generator**: `backend/prompts/{position}_prompts.py`
- **Response parser**: `backend/parsers/{position}_parser.py`
- **Stats model**: Pydantic model in `backend/models.py`

Position mappings are in `backend/main.py`: `PROMPT_MAP`, `PARSER_MAP`, `STATS_MODEL_MAP`

### Adding a New Position
1. Create `prompts/{pos}_prompts.py` with `generate_{pos}_comparison_prompt()`
2. Create `parsers/{pos}_parser.py` with `parse_{pos}_recommendation()`
3. Add stats model to `models.py`
4. Update mappings in `main.py`
5. Add imports to `prompts/__init__.py` and `parsers/__init__.py`

## API Endpoints

- `POST /start-sit` - Main comparison endpoint (players, position, scoring)
- `GET /health` - Health check with cache status
- `GET /metrics` - Cache performance metrics

## Testing

```bash
# Test backend API
curl -X POST http://localhost:8000/start-sit \
  -H "Content-Type: application/json" \
  -d '{"players": ["Tyreek Hill", "Justin Jefferson"], "position": "WR", "scoring": "PPR"}'
```
