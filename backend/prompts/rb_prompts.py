"""
Running Back (RB) specific prompts
"""

def generate_rb_comparison_prompt(player1: str, player2: str, scoring: str = "PPR") -> str:
    """
    Generate a specialized prompt for RB comparisons with specific metrics
    """
    return f"""{player1} vs {player2} (RB, {scoring}) - who to start?

Get their 2025-26 season stats **PER GAME** for 6 metrics. **Prioritize** in this order:
1. PPG (MOST IMPORTANT)
2. Rush Yards per game (HIGH priority)
3. Receptions per game (HIGH priority in PPR)
4. Rush Attempts per game (MEDIUM priority)
5. Yards per Carry (MEDIUM priority)
6. Rec Yards per game (LOW priority)

Format (ALL STATS ARE PER-GAME AVERAGES):
{player1}: PPG=X.X | Rush Yds=X.X | Rec=X.X | Carries=X.X | YPC=X.X | Rec Yds=X.X
{player2}: PPG=X.X | Rush Yds=X.X | Rec=X.X | Carries=X.X | YPC=X.X | Rec Yds=X.X

Advantages:
{player1}: [list metrics where better, separated by commas]
{player2}: [list metrics where better, separated by commas]

START: [name]
CONFIDENCE: High/Med/Low
REASON: [Name] wins X/6, leads in high-priority metrics

IMPORTANT: Do not include citation numbers [1][2], references, or source links in your response."""
