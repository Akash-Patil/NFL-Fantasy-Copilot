"""
Wide Receiver (WR) specific prompts
"""

def generate_wr_comparison_prompt(player1: str, player2: str, scoring: str = "PPR") -> str:
    """
    Generate a specialized prompt for WR comparisons with specific metrics
    """
    return f"""{player1} vs {player2} (WR, {scoring}) - who to start?

Get their 2025-26 season stats **PER GAME** for 6 metrics. **Prioritize** in this order:
1. PPG (MOST IMPORTANT)
2. Targets per game (HIGH priority)
3. Rec Yards per game (HIGH priority)
4. Receptions per game (MEDIUM priority)
5. Target Share % (LOW priority)
6. Yards per Team Pass Attempt (LOW priority)

Format (ALL STATS ARE PER-GAME AVERAGES):
{player1}: PPG=X.X | Tgt=X.X | Rec=X.X | Yds=X.X | TgtSh=X% | Y/TA=X.X
{player2}: PPG=X.X | Tgt=X.X | Rec=X.X | Yds=X.X | TgtSh=X% | Y/TA=X.X

Advantages:
{player1}: [list metrics where better, separated by commas]
{player2}: [list metrics where better, separated by commas]

START: [name]
CONFIDENCE: High/Med/Low
REASON: [Name] wins X/6, leads in high-priority metrics

IMPORTANT: Do not include citation numbers [1][2], references, or source links in your response."""
