"""
Tight End (TE) specific prompts
"""

def generate_te_comparison_prompt(player1: str, player2: str, scoring: str = "PPR") -> str:
    """
    Generate a specialized prompt for TE comparisons with specific metrics
    """
    return f"""{player1} vs {player2} (TE, {scoring}) - who to start?

Get their 2025-26 season stats **PER GAME** for 6 metrics. **Prioritize** in this order:
1. PPG (MOST IMPORTANT)
2. Targets per game (HIGH priority)
3. Rec Yards per game (HIGH priority)
4. Receptions per game (MEDIUM priority)
5. Red Zone Targets per game (MEDIUM priority)
6. Target Share % (LOW priority)

Format (ALL STATS ARE PER-GAME AVERAGES):
{player1}: PPG=X.X | Tgt=X.X | Rec Yds=X.X | Rec=X.X | RZ Tgt=X.X | TgtSh=X%
{player2}: PPG=X.X | Tgt=X.X | Rec Yds=X.X | Rec=X.X | RZ Tgt=X.X | TgtSh=X%

Advantages:
{player1}: [list metrics where better, separated by commas]
{player2}: [list metrics where better, separated by commas]

START: [name]
CONFIDENCE: High/Med/Low
REASON: [Name] wins X/6, leads in high-priority metrics

IMPORTANT: Do not include citation numbers [1][2], references, or source links in your response."""
