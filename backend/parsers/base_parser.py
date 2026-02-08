"""
Base/shared parsing utilities for all positions
"""
import re
from typing import Optional


def clean_citations(text: str) -> str:
    """Remove citation numbers like [1][2][5] from text"""
    return re.sub(r'\[\d+\]', '', text).strip()


def extract_decision(cleaned_text: str) -> str:
    """Extract START decision from response"""
    start_match = re.search(r'\*\*START:?\s*\*?\*?\s*([^\n\*]+)', cleaned_text, re.IGNORECASE)
    if not start_match:
        start_match = re.search(r'START:\s*([^\n]+)', cleaned_text, re.IGNORECASE)
    return start_match.group(1).strip().rstrip('*').strip() if start_match else "Unknown"


def extract_confidence(cleaned_text: str) -> str:
    """Extract CONFIDENCE level from response"""
    confidence_match = re.search(r'\*\*CONFIDENCE:?\s*\*?\*?\s*([^\n\*]+)', cleaned_text, re.IGNORECASE)
    if not confidence_match:
        confidence_match = re.search(r'CONFIDENCE:\s*([^\n]+)', cleaned_text, re.IGNORECASE)
    return confidence_match.group(1).strip().rstrip('*').strip() if confidence_match else "Med"


def extract_reason(cleaned_text: str) -> str:
    """Extract REASON from response"""
    reason_match = re.search(r'\*\*REASON\*?\*?:?\s*(.+?)(?:\n|$)', cleaned_text, re.IGNORECASE | re.DOTALL)
    if not reason_match:
        reason_match = re.search(r'REASON:?\s*(.+?)(?:\n|$)', cleaned_text, re.IGNORECASE)
    reason = reason_match.group(1).strip() if reason_match else ""
    return reason.rstrip('*').strip().lstrip(':').strip()


def parse_advantages(advantages_text: str, player1_name: str, player2_name: str) -> tuple[list[str], list[str]]:
    """
    Parse advantages section for both players
    """
    player1_advantages = []
    player2_advantages = []
    
    # Clean up text
    advantages_text = advantages_text.replace('**', '').strip()
    
    # Split by player names
    lines = advantages_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if player1_name in line:
            metrics_part = line.split(':', 1)
            if len(metrics_part) > 1:
                metrics_text = metrics_part[1].strip()
                if metrics_text.lower() not in ['none', '*none*', 'n/a', '']:
                    metrics = [m.strip() for m in metrics_text.split(',')]
                    player1_advantages.extend([m for m in metrics if m and m.lower() not in ['none', '*none*', 'n/a']])
        elif player2_name in line:
            metrics_part = line.split(':', 1)
            if len(metrics_part) > 1:
                metrics_text = metrics_part[1].strip()
                if metrics_text.lower() not in ['none', '*none*', 'n/a', '']:
                    metrics = [m.strip() for m in metrics_text.split(',')]
                    player2_advantages.extend([m for m in metrics if m and m.lower() not in ['none', '*none*', 'n/a']])
    
    return player1_advantages, player2_advantages


def extract_advantages_section(cleaned_text: str) -> Optional[str]:
    """Extract the advantages section from the response"""
    if 'Advantages' in cleaned_text:
        advantages_section = re.search(
            r'\*?\*?Advantages\*?\*?:?\s*(.*?)(?:\*\*START:|START:)',
            cleaned_text,
            re.DOTALL | re.IGNORECASE
        )
        if advantages_section:
            return advantages_section.group(1)
    return None
