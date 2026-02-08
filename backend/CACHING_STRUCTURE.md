# Future Caching Implementation Structure

## Recommended Folder Structure

When you're ready to add caching, organize your project like this:

```
backend/
├── main.py                      # Main FastAPI app (routes only)
├── perplexity_client.py         # Perplexity API integration
├── prompts.py                   # Prompt templates
├── requirements.txt
├── .env
│
├── models/                      # Pydantic models
│   ├── __init__.py
│   ├── requests.py              # Request models (StartSitRequest, etc.)
│   └── responses.py             # Response models (StartSitResponse, etc.)
│
├── services/                    # Business logic layer
│   ├── __init__.py
│   ├── fantasy_service.py       # Fantasy analysis logic
│   └── perplexity_service.py    # Wrapper around perplexity_client
│
├── cache/                       # Caching layer (ADD LATER)
│   ├── __init__.py
│   ├── database.py              # SQLAlchemy models & setup
│   ├── cache_manager.py         # Caching logic
│   └── cache_config.py          # Cache settings (TTL, expiration rules)
│
├── utils/                       # Helper functions
│   ├── __init__.py
│   ├── nfl_utils.py             # NFL week calculation, team schedules
│   └── hash_utils.py            # Query hashing for cache keys
│
└── config/                      # Configuration
    ├── __init__.py
    └── settings.py              # Environment variables, app config
```

## Step-by-Step Integration Plan

### Phase 1: Current (No Cache)
```
backend/
├── main.py
├── perplexity_client.py
├── prompts.py
├── requirements.txt
└── .env
```

### Phase 2: Add Caching
1. **Create `cache/` folder** with:
   - `database.py` - SQLite + SQLAlchemy setup
   - `cache_manager.py` - Get/set cache logic
   - `cache_config.py` - Expiration rules

2. **Update `main.py`**:
   ```python
   from cache.cache_manager import CacheManager
   from database import get_db
   
   @app.post("/start-sit")
   async def start_sit(request: StartSitRequest, db: Session = Depends(get_db)):
       # Check cache
       cached = CacheManager.get_cached_response(db, hash)
       if cached:
           return cached
       
       # Call Perplexity
       result = await perplexity.ask(...)
       
       # Save to cache
       CacheManager.save_to_cache(db, hash, result)
       return result
   ```

3. **Add to `requirements.txt`**:
   ```
   sqlalchemy==2.0.25
   ```

### Phase 3: Refactor for Scale (Optional)
- Move models to `models/`
- Move business logic to `services/`
- Keep `main.py` clean with just routes

## Quick Integration Checklist

When you're ready to add caching:

- [ ] Create `cache/` directory
- [ ] Add `cache/database.py` (from earlier code)
- [ ] Add `cache/cache_manager.py` (from earlier code)
- [ ] Add `sqlalchemy` to requirements.txt
- [ ] Update imports in `main.py`
- [ ] Add `db: Session = Depends(get_db)` to endpoints
- [ ] Wrap Perplexity calls with cache checks
- [ ] Test with duplicate queries

## Benefits of This Structure

✅ **Modular** - Easy to add/remove caching  
✅ **Clean separation** - Each folder has one purpose  
✅ **Testable** - Can mock cache layer independently  
✅ **Scalable** - Easy to swap SQLite → PostgreSQL later  
✅ **Maintainable** - Clear where each piece of code lives  

## Current Simple Structure (Good for MVP!)

Your current flat structure is perfect for a 2-day build:
- Fast to develop
- Easy to understand
- No over-engineering
- Add complexity only when needed ✨



