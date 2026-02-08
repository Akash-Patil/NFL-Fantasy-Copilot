"""
Quarterback (QB) response parser
"""
import re
from typing import Optional
from .base_parser import (
    clean_citations, extract_decision, extract_confidence, 
    extract_reason, parse_advantages, extract_advantages_section
)


def parse_qb_stats(stats_line: str) -> Optional[dict]:
    """
    Parse QB stats line like:
    "Patrick Mahomes: PPG=X.X | Pass Yds=X.X | Pass TDs=X.X | INTs=X.X | Comp%=X.X% | Rush Yds=X.X"
    """
    stats_line = stats_line.replace('**', '').strip()
    
    name_match = re.match(r'^([^:]+):', stats_line)
    if not name_match:
        return None
    
    player_name = name_match.group(1).strip()
    
    # Extract QB-specific stats
    ppg_match = re.search(r'PPG=([0-9.]+)', stats_line)
    pass_yds_match = re.search(r'Pass Yds=([0-9.]+)', stats_line)
    pass_tds_match = re.search(r'Pass TDs=([0-9.]+)', stats_line)
    ints_match = re.search(r'INTs=([0-9.]+)', stats_line)
    comp_pct_match = re.search(r'Comp%=([0-9.]+)%?', stats_line)
    rush_yds_match = re.search(r'Rush Yds=([0-9.]+)', stats_line)
    
    return {
        "name": player_name,
        "ppg": float(ppg_match.group(1)) if ppg_match else 0.0,
        "passing_yards_per_game": float(pass_yds_match.group(1)) if pass_yds_match else 0.0,
        "passing_tds_per_game": float(pass_tds_match.group(1)) if pass_tds_match else 0.0,
        "interceptions_per_game": float(ints_match.group(1)) if ints_match else 0.0,
        "completion_pct": float(comp_pct_match.group(1)) if comp_pct_match else 0.0,
        "rushing_yards_per_game": float(rush_yds_match.group(1)) if rush_yds_match else 0.0
    }


def parse_qb_recommendation(raw_text: str, player1_name: str, player2_name: str) -> dict:
    """
    Parse the QB comparison response into structured data
    """
    cleaned_text = clean_citations(raw_text)
    
    decision = extract_decision(cleaned_text)
    confidence = extract_confidence(cleaned_text)
    reason = extract_reason(cleaned_text)
    
    # Parse player stats
    player1_stats = None
    player2_stats = None
    
    lines = cleaned_text.split('\n')
    for line in lines:
        if 'PPG=' in line:
            parsed = parse_qb_stats(line)
            if parsed:
                if player1_name.lower() in parsed['name'].lower():
                    player1_stats = parsed
                elif player2_name.lower() in parsed['name'].lower():
                    player2_stats = parsed
    
    # Parse advantages
    player1_advantages = []
    player2_advantages = []
    
    advantages_section = extract_advantages_section(cleaned_text)
    if advantages_section:
        player1_advantages, player2_advantages = parse_advantages(
            advantages_section,
            player1_name,
            player2_name
        )
    
    return {
        "decision": decision,
        "confidence": confidence,
        "reason": reason,
        "player1_stats": player1_stats or {
            "name": player1_name,
            "ppg": 0.0,
            "passing_yards_per_game": 0.0,
            "passing_tds_per_game": 0.0,
            "interceptions_per_game": 0.0,
            "completion_pct": 0.0,
            "rushing_yards_per_game": 0.0
        },
        "player2_stats": player2_stats or {
            "name": player2_name,
            "ppg": 0.0,
            "passing_yards_per_game": 0.0,
            "passing_tds_per_game": 0.0,
            "interceptions_per_game": 0.0,
            "completion_pct": 0.0,
            "rushing_yards_per_game": 0.0
        },
        "player1_advantages": player1_advantages,
        "player2_advantages": player2_advantages,
        "raw_response": cleaned_text
    }
