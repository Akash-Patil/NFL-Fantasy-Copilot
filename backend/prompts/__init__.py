"""
Prompts package for different NFL positions
"""
from .wr_prompts import generate_wr_comparison_prompt
from .qb_prompts import generate_qb_comparison_prompt
from .rb_prompts import generate_rb_comparison_prompt
from .te_prompts import generate_te_comparison_prompt
from .base_prompts import get_system_prompt

__all__ = [
    'generate_wr_comparison_prompt',
    'generate_qb_comparison_prompt',
    'generate_rb_comparison_prompt',
    'generate_te_comparison_prompt',
    'get_system_prompt'
]
