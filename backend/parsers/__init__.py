"""
Response parsers for different NFL positions
"""
from .wr_parser import parse_wr_recommendation
from .qb_parser import parse_qb_recommendation
from .rb_parser import parse_rb_recommendation
from .te_parser import parse_te_recommendation

__all__ = [
    'parse_wr_recommendation',
    'parse_qb_recommendation',
    'parse_rb_recommendation',
    'parse_te_recommendation'
]
