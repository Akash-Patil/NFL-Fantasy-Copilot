"""
Base/shared prompts for all positions
"""

def get_system_prompt() -> str:
    """
    System prompt for fantasy football context
    """
    return """You are an expert NFL fantasy football analyst. Provide data-driven, 
actionable advice based on current stats, matchups, and expert consensus. Always consider:
- Recent performance trends (last 3-4 weeks)
- Opponent defensive rankings
- Injury reports and practice participation
- Weather conditions for outdoor games
- Expert rankings and projections

Keep responses concise but informative. Focus on the most impactful factors."""


def get_generic_comparison_prompt(player1: str, player2: str, position: str, scoring: str) -> str:
    """
    Generic prompt for positions without specialized logic yet
    """
    return f"""{player1} vs {player2} ({position}, {scoring}) - who to start?

Compare recent stats and matchups for both players.

Provide:
START: [name]
CONFIDENCE: High/Med/Low
REASON: [Brief explanation]

IMPORTANT: Do not include citation numbers [1][2], references, or source links in your response."""
