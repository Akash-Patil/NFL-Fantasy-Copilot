"""
Redis Cache Client with Metrics Tracking

FDE Interview Talking Points:
1. Cache key design: Sort player names so "A vs B" = "B vs A" (reduces storage by ~50%)
2. TTL-based expiration: Configurable freshness vs. performance trade-off
3. Metrics: Track hit/miss rates for customer observability
4. Cost savings: Each cache hit saves ~$0.005 in API costs
"""
import json
import time
import logging
from typing import Optional
from dataclasses import dataclass, field
from config import settings
import redis

logger = logging.getLogger(__name__)


@dataclass
class CacheMetrics:
    """
    Track cache performance metrics.
    
    FDE Interview Talking Point:
    - Observability is critical for customer trust
    - These metrics help customers understand cost savings
    """
    hits: int = 0
    misses: int = 0
    total_requests: int = 0
    total_latency_ms: float = 0.0
    errors: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate as percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100
    
    @property
    def avg_latency_ms(self) -> float:
        """Calculate average cache lookup latency"""
        if self.total_requests == 0:
            return 0.0
        return self.total_latency_ms / self.total_requests
    
    @property
    def estimated_cost_savings(self) -> float:
        """
        Estimate cost savings from cache hits.
        Assumes ~$0.005 per Perplexity API call.
        """
        cost_per_call = 0.005
        return self.hits * cost_per_call


class CacheClient:
    """
    Redis-based cache client with metrics tracking.
    
    Key Design Decisions:
    1. Player names are normalized and sorted for consistent cache keys
    2. TTL is configurable via environment variable
    3. Graceful degradation: if Redis fails, we just call the API
    """
    
    def __init__(self):
        self.metrics = CacheMetrics()
        self.redis = None
        self._connect()
    
    def _connect(self):
        """Connect to Redis with error handling"""
        if not settings.CACHE_ENABLED:
            logger.info("Cache is disabled via configuration")
            return
            
        try:
            import redis
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis.ping()
            logger.info(f"Connected to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Cache will be disabled.")
            self.redis = None
    
    def _generate_key(self, players: list[str], position: str, scoring: str) -> str:
        """
        Generate a consistent cache key.
        
        FDE Interview Talking Point:
        - Sorting player names ensures "A vs B" and "B vs A" hit the same cache entry
        - This effectively doubles our cache hit rate for duplicate queries
        """
        # Normalize: lowercase, replace spaces with underscores
        normalized = sorted([p.lower().strip().replace(" ", "_") for p in players])
        return f"fantasy:start-sit:{position.upper()}:{scoring.upper()}:{normalized[0]}:{normalized[1]}"
    
    def get(self, players: list[str], position: str, scoring: str) -> Optional[dict]:
        """
        Retrieve cached response if available.
        
        Returns:
            Cached response dict or None if cache miss
        """
        if not self.redis or not settings.CACHE_ENABLED:
            self.metrics.total_requests += 1
            self.metrics.misses += 1
            return None
        
        key = self._generate_key(players, position, scoring)
        start_time = time.time()
        
        try:
            cached = self.redis.get(key)
            latency_ms = (time.time() - start_time) * 1000
            
            self.metrics.total_requests += 1
            self.metrics.total_latency_ms += latency_ms
            
            if cached:
                self.metrics.hits += 1
                logger.debug(f"Cache HIT for {key} (latency: {latency_ms:.2f}ms)")
                return json.loads(cached)
            else:
                self.metrics.misses += 1
                logger.debug(f"Cache MISS for {key}")
                return None
                
        except Exception as e:
            self.metrics.errors += 1
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, players: list[str], position: str, scoring: str, data: dict, ttl: int = None) -> bool:
        """
        Store response in cache with TTL.
        
        Args:
            players: List of player names
            position: Position (QB, RB, WR, TE)
            scoring: Scoring format (PPR, Half-PPR, Standard)
            data: Response data to cache
            ttl: Time-to-live in seconds (uses default if not specified)
            
        Returns:
            True if cached successfully, False otherwise
        """
        if not self.redis or not settings.CACHE_ENABLED:
            return False
        
        key = self._generate_key(players, position, scoring)
        ttl = ttl or settings.CACHE_TTL_SECONDS
        
        try:
            self.redis.setex(key, ttl, json.dumps(data))
            logger.debug(f"Cached {key} with TTL={ttl}s")
            return True
        except Exception as e:
            self.metrics.errors += 1
            logger.error(f"Cache set error: {e}")
            return False
    
    def get_metrics(self) -> dict:
        """
        Get cache performance metrics.
        
        FDE Interview Talking Point:
        - Expose metrics via API endpoint for customer dashboards
        - Show concrete value: hit rate, cost savings
        """
        return {
            "hits": self.metrics.hits,
            "misses": self.metrics.misses,
            "total_requests": self.metrics.total_requests,
            "hit_rate_pct": round(self.metrics.hit_rate, 2),
            "avg_latency_ms": round(self.metrics.avg_latency_ms, 2),
            "errors": self.metrics.errors,
            "estimated_cost_savings_usd": round(self.metrics.estimated_cost_savings, 4),
            "cache_enabled": settings.CACHE_ENABLED,
            "ttl_seconds": settings.CACHE_TTL_SECONDS
        }
    
    def is_healthy(self) -> bool:
        """Check if Redis connection is healthy"""
        if not self.redis:
            return False
        try:
            self.redis.ping()
            return True
        except:
            return False


# Singleton instance
cache = CacheClient()
