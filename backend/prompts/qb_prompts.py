"""
Quarterback (QB) specific prompts
"""

def generate_qb_comparison_prompt(player1: str, player2: str, scoring: str = "PPR") -> str:
    """
    Generate a specialized prompt for QB comparisons with specific metrics
    """
    return f"""{player1} vs {player2} (QB, {scoring}) - who to start?

Get their 2025-26 season stats **PER GAME** for 6 metrics. **Prioritize** in this order:
1. PPG (MOST IMPORTANT)
2. Passing Yards per game (HIGH priority)
3. Passing TDs per game (HIGH priority)
4. Interceptions per game (MEDIUM priority - lower is better)
5. Completion % (MEDIUM priority)
6. Rushing Yards per game (LOW priority)

Format (ALL STATS ARE PER-GAME AVERAGES):
{player1}: PPG=X.X | Pass Yds=X.X | Pass TDs=X.X | INTs=X.X | Comp%=X.X% | Rush Yds=X.X
{player2}: PPG=X.X | Pass Yds=X.X | Pass TDs=X.X | INTs=X.X | Comp%=X.X% | Rush Yds=X.X

Advantages:
{player1}: [list metrics where better, separated by commas]
{player2}: [list metrics where better, separated by commas]

START: [name]
CONFIDENCE: High/Med/Low
REASON: [Name] wins X/6, leads in high-priority metrics

IMPORTANT: Do not include citation numbers [1][2], references, or source links in your response."""
