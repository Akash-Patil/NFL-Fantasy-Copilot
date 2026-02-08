"""
Running Back (RB) response parser
"""
import re
from typing import Optional
from .base_parser import (
    clean_citations, extract_decision, extract_confidence, 
    extract_reason, parse_advantages, extract_advantages_section
)


def parse_rb_stats(stats_line: str) -> Optional[dict]:
    """
    Parse RB stats line like:
    "Derrick Henry: PPG=X.X | Rush Yds=X.X | Rec=X.X | Carries=X.X | YPC=X.X | Rec Yds=X.X"
    """
    stats_line = stats_line.replace('**', '').strip()
    
    name_match = re.match(r'^([^:]+):', stats_line)
    if not name_match:
        return None
    
    player_name = name_match.group(1).strip()
    
    # Extract RB-specific stats
    ppg_match = re.search(r'PPG=([0-9.]+)', stats_line)
    rush_yds_match = re.search(r'Rush Yds=([0-9.]+)', stats_line)
    rec_match = re.search(r'Rec=([0-9.]+)', stats_line)
    carries_match = re.search(r'Carries=([0-9.]+)', stats_line)
    ypc_match = re.search(r'YPC=([0-9.]+)', stats_line)
    rec_yds_match = re.search(r'Rec Yds=([0-9.]+)', stats_line)
    
    return {
        "name": player_name,
        "ppg": float(ppg_match.group(1)) if ppg_match else 0.0,
        "rushing_yards_per_game": float(rush_yds_match.group(1)) if rush_yds_match else 0.0,
        "receptions_per_game": float(rec_match.group(1)) if rec_match else 0.0,
        "carries_per_game": float(carries_match.group(1)) if carries_match else 0.0,
        "yards_per_carry": float(ypc_match.group(1)) if ypc_match else 0.0,
        "receiving_yards_per_game": float(rec_yds_match.group(1)) if rec_yds_match else 0.0
    }


def parse_rb_recommendation(raw_text: str, player1_name: str, player2_name: str) -> dict:
    """
    Parse the RB comparison response into structured data
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
            parsed = parse_rb_stats(line)
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
            "rushing_yards_per_game": 0.0,
            "receptions_per_game": 0.0,
            "carries_per_game": 0.0,
            "yards_per_carry": 0.0,
            "receiving_yards_per_game": 0.0
        },
        "player2_stats": player2_stats or {
            "name": player2_name,
            "ppg": 0.0,
            "rushing_yards_per_game": 0.0,
            "receptions_per_game": 0.0,
            "carries_per_game": 0.0,
            "yards_per_carry": 0.0,
            "receiving_yards_per_game": 0.0
        },
        "player1_advantages": player1_advantages,
        "player2_advantages": player2_advantages,
        "raw_response": cleaned_text
    }
