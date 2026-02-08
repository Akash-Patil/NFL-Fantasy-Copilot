"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import Union


# Request Models
class StartSitRequest(BaseModel):
    players: list[str] = Field(..., min_items=2, max_items=2, description="Exactly 2 player names for 1v1 comparison")
    position: str = Field(..., description="Position (QB, RB, WR, TE)")
    scoring: str = Field(default="PPR", description="Scoring format (PPR, Half-PPR, Standard)")


# Stats Models for each position
class WRStats(BaseModel):
    name: str
    ppg: float
    targets_per_game: float
    receptions_per_game: float
    yards_per_game: float
    target_share_pct: float
    yards_per_team_att: float


class QBStats(BaseModel):
    name: str
    ppg: float
    passing_yards_per_game: float
    passing_tds_per_game: float
    interceptions_per_game: float
    completion_pct: float
    rushing_yards_per_game: float


class RBStats(BaseModel):
    name: str
    ppg: float
    rushing_yards_per_game: float
    receptions_per_game: float
    carries_per_game: float
    yards_per_carry: float
    receiving_yards_per_game: float


class TEStats(BaseModel):
    name: str
    ppg: float
    targets_per_game: float
    receiving_yards_per_game: float
    receptions_per_game: float
    redzone_targets_per_game: float
    target_share_pct: float


# Union type for all player stats
PlayerStatsUnion = Union[WRStats, QBStats, RBStats, TEStats]


# Response Models
class StartSitResponse(BaseModel):
    # Main decision
    decision: str = Field(..., description="The player to start")
    confidence: str = Field(..., description="High, Med, or Low")
    reason: str = Field(..., description="Brief explanation for the decision")
    
    # Structured stats for each player (will be position-specific)
    player1_stats: dict  # Can be WRStats, QBStats, RBStats, or TEStats
    player2_stats: dict  # Can be WRStats, QBStats, RBStats, or TEStats
    
    # Which metrics each player wins
    player1_advantages: list[str] = Field(default_factory=list, description="Metrics where player 1 is better")
    player2_advantages: list[str] = Field(default_factory=list, description="Metrics where player 2 is better")
    
    # Original metadata
    players_analyzed: list[str]
    position: str
    scoring: str
    
    # Full raw response for debugging
    raw_response: str = Field(..., description="Complete unstructured response")
    
    # Cache metadata
    from_cache: bool = Field(default=False, description="Whether this response was served from cache")
