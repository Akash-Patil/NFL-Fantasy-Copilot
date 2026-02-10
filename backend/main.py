from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from perplexity_client import PerplexityClient
from models import StartSitRequest, StartSitResponse, WRStats, QBStats, RBStats, TEStats
from cache import cache
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import prompts
from prompts import (
    generate_wr_comparison_prompt,
    generate_qb_comparison_prompt,
    generate_rb_comparison_prompt,
    generate_te_comparison_prompt,
    get_system_prompt
)

# Import parsers
from parsers import (
    parse_wr_recommendation,
    parse_qb_recommendation,
    parse_rb_recommendation,
    parse_te_recommendation
)

app = FastAPI(
    title="NFL Fantasy Copilot API",
    description="NFL Fantasy Football AI Assistant with position-specific analysis and Redis caching",
    version="2.1.0"
)

# CORS middleware
# Development: Allow all origins
# Production: Replace "*" with your actual frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"  # Development - allows all origins
        # Production - uncomment and update with your Vercel URL:
        # "http://localhost:3000",
        # "http://localhost:5173",
        # "https://your-app.vercel.app",
        # "https://*.vercel.app"  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Perplexity client
perplexity = PerplexityClient()


# Position-specific prompt mapping
PROMPT_MAP = {
    "WR": generate_wr_comparison_prompt,
    "QB": generate_qb_comparison_prompt,
    "RB": generate_rb_comparison_prompt,
    "TE": generate_te_comparison_prompt
}

# Position-specific parser mapping
PARSER_MAP = {
    "WR": parse_wr_recommendation,
    "QB": parse_qb_recommendation,
    "RB": parse_rb_recommendation,
    "TE": parse_te_recommendation
}

# Position-specific stats model mapping
STATS_MODEL_MAP = {
    "WR": WRStats,
    "QB": QBStats,
    "RB": RBStats,
    "TE": TEStats
}


@app.get("/")
async def root():
    return {
        "message": "NFL Fantasy Copilot API v2.1",
        "description": "Position-specific player analysis with caching for QB, RB, WR, TE",
        "endpoints": {
            "/start-sit": "POST - Compare two players (cached)",
            "/metrics": "GET - Cache performance metrics",
            "/health": "GET - Health check with cache status",
            "/docs": "API documentation"
        },
        "supported_positions": ["QB", "RB", "WR", "TE"],
        "cache_enabled": settings.CACHE_ENABLED
    }


@app.post("/start-sit", response_model=StartSitResponse)
async def start_sit(request: StartSitRequest):
    """
    Compare two players and get start/sit recommendations with position-specific analysis.
    
    Responses are cached for performance and cost optimization.
    
    Supported positions: QB, RB, WR, TE
    """
    try:
        position = request.position.upper()
        scoring = request.scoring.upper()
        
        # Validate position
        if position not in PROMPT_MAP:
            raise HTTPException(
                status_code=400, 
                detail=f"Position '{position}' not supported. Use: QB, RB, WR, or TE"
            )
        
        # 1. Check cache first
        cached_response = cache.get(request.players, position, scoring)
        if cached_response:
            logger.info(f"Cache HIT for {request.players[0]} vs {request.players[1]} ({position})")
            cached_response["from_cache"] = True
            return StartSitResponse(**cached_response)
        
        logger.info(f"Cache MISS for {request.players[0]} vs {request.players[1]} ({position}) - calling Perplexity API")
        
        # 2. Cache miss - call Perplexity API
        prompt_generator = PROMPT_MAP[position]
        prompt = prompt_generator(
            request.players[0],
            request.players[1],
            request.scoring
        )
        
        raw_recommendation = await perplexity.ask(prompt, system_prompt=None)
        
        # 3. Parse the response
        parser = PARSER_MAP[position]
        parsed_data = parser(
            raw_recommendation,
            request.players[0],
            request.players[1]
        )
        
        # 4. Validate with position-specific stats model
        stats_model = STATS_MODEL_MAP[position]
        
        # 5. Build response data
        response_data = {
            "decision": parsed_data["decision"],
            "confidence": parsed_data["confidence"],
            "reason": parsed_data["reason"],
            "player1_stats": stats_model(**parsed_data["player1_stats"]).model_dump(),
            "player2_stats": stats_model(**parsed_data["player2_stats"]).model_dump(),
            "player1_advantages": parsed_data["player1_advantages"],
            "player2_advantages": parsed_data["player2_advantages"],
            "players_analyzed": request.players,
            "position": position,
            "scoring": scoring,
            "raw_response": parsed_data["raw_response"],
            "from_cache": False
        }
        
        # 6. Store in cache for future requests
        cache.set(request.players, position, scoring, response_data)
        
        return StartSitResponse(**response_data)
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint with cache status"""
    return {
        "status": "healthy",
        "version": "2.1.0",
        "positions_supported": list(PROMPT_MAP.keys()),
        "cache_enabled": settings.CACHE_ENABLED,
        "cache_healthy": cache.is_healthy()
    }


@app.get("/metrics")
async def get_metrics():
    """
    Cache performance metrics endpoint.
    
    FDE Interview Talking Point:
    - Observability is critical for customer trust and debugging
    - These metrics help demonstrate concrete value (cost savings, performance)
    - Customers can integrate this into their monitoring dashboards
    """
    return {
        "cache": cache.get_metrics(),
        "api_version": "2.1.0"
    }
