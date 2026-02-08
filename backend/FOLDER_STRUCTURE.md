# Backend Folder Structure

## Overview
The backend is now organized with position-specific prompts and parsers for QB, RB, WR, and TE comparisons.

## Directory Structure

```
backend/
├── prompts/                    # Position-specific prompt generators
│   ├── __init__.py
│   ├── base_prompts.py        # Shared/system prompts
│   ├── wr_prompts.py          # Wide Receiver prompts
│   ├── qb_prompts.py          # Quarterback prompts
│   ├── rb_prompts.py          # Running Back prompts
│   └── te_prompts.py          # Tight End prompts
│
├── parsers/                    # Position-specific response parsers
│   ├── __init__.py
│   ├── base_parser.py         # Shared parsing utilities
│   ├── wr_parser.py           # WR stats parser
│   ├── qb_parser.py           # QB stats parser
│   ├── rb_parser.py           # RB stats parser
│   └── te_parser.py           # TE stats parser
│
├── main.py                     # FastAPI app with position routing
├── models.py                   # Pydantic models for all positions
├── perplexity_client.py        # API client for Perplexity
└── requirements.txt            # Python dependencies
```

## How It Works

### 1. Request Flow
```
User Request → main.py → Position Router → Prompt Generator → Perplexity API → Parser → Structured Response
```

### 2. Position-Specific Components

#### WR (Wide Receiver)
- **Metrics**: PPG, Targets/G, Rec Yards/G, Receptions/G, Target Share %, Y/TA
- **File**: `prompts/wr_prompts.py`, `parsers/wr_parser.py`
- **Model**: `WRStats`

#### QB (Quarterback)
- **Metrics**: PPG, Pass Yards/G, Pass TDs/G, INTs/G, Comp%, Rush Yards/G
- **File**: `prompts/qb_prompts.py`, `parsers/qb_parser.py`
- **Model**: `QBStats`

#### RB (Running Back)
- **Metrics**: PPG, Rush Yards/G, Receptions/G, Carries/G, YPC, Rec Yards/G
- **File**: `prompts/rb_prompts.py`, `parsers/rb_parser.py`
- **Model**: `RBStats`

#### TE (Tight End)
- **Metrics**: PPG, Targets/G, Rec Yards/G, Receptions/G, RZ Targets/G, Target Share %
- **File**: `prompts/te_prompts.py`, `parsers/te_parser.py`
- **Model**: `TEStats`

## Adding a New Position

To add support for a new position (e.g., K for Kicker):

1. **Create Prompt File**: `prompts/k_prompts.py`
   ```python
   def generate_k_comparison_prompt(player1: str, player2: str, scoring: str = "PPR") -> str:
       # Define K-specific metrics and format
       pass
   ```

2. **Create Parser File**: `parsers/k_parser.py`
   ```python
   def parse_k_recommendation(raw_text: str, player1_name: str, player2_name: str) -> dict:
       # Parse K-specific stats
       pass
   ```

3. **Add Stats Model**: Update `models.py`
   ```python
   class KStats(BaseModel):
       name: str
       ppg: float
       # ... K-specific fields
   ```

4. **Update Mappings**: In `main.py`
   ```python
   PROMPT_MAP["K"] = generate_k_comparison_prompt
   PARSER_MAP["K"] = parse_k_recommendation
   STATS_MODEL_MAP["K"] = KStats
   ```

5. **Update __init__.py files**: Add imports to `prompts/__init__.py` and `parsers/__init__.py`

## API Usage

### Request Format (All Positions)
```json
{
  "players": ["Player 1", "Player 2"],
  "position": "QB|RB|WR|TE",
  "scoring": "PPR|Half-PPR|Standard"
}
```

### Response Format
```json
{
  "decision": "Player Name",
  "confidence": "High|Med|Low",
  "reason": "Explanation",
  "player1_stats": { /* Position-specific stats */ },
  "player2_stats": { /* Position-specific stats */ },
  "player1_advantages": ["Metric 1", "Metric 2"],
  "player2_advantages": ["Metric 3"],
  "players_analyzed": ["Player 1", "Player 2"],
  "position": "WR",
  "scoring": "PPR",
  "raw_response": "Full text response"
}
```

## Benefits of This Structure

✅ **Scalable**: Easy to add new positions
✅ **Maintainable**: Position logic is isolated
✅ **Type-Safe**: Position-specific Pydantic models
✅ **Flexible**: Each position can have unique metrics
✅ **Clean**: Clear separation of concerns

## Migration Notes

### Old Files (Can be removed after testing)
- `receiver_prompts.py` → Replaced by `prompts/wr_prompts.py` and `prompts/base_prompts.py`
- `response_parser.py` → Replaced by `parsers/wr_parser.py` and `parsers/base_parser.py`

### Testing
Test each position:
```bash
# WR Test
curl -X POST http://localhost:8000/start-sit \
  -H "Content-Type: application/json" \
  -d '{"players": ["Tyreek Hill", "Justin Jefferson"], "position": "WR", "scoring": "PPR"}'

# QB Test
curl -X POST http://localhost:8000/start-sit \
  -H "Content-Type: application/json" \
  -d '{"players": ["Patrick Mahomes", "Josh Allen"], "position": "QB", "scoring": "PPR"}'

# RB Test
curl -X POST http://localhost:8000/start-sit \
  -H "Content-Type: application/json" \
  -d '{"players": ["Christian McCaffrey", "Derrick Henry"], "position": "RB", "scoring": "PPR"}'

# TE Test
curl -X POST http://localhost:8000/start-sit \
  -H "Content-Type: application/json" \
  -d '{"players": ["Travis Kelce", "George Kittle"], "position": "TE", "scoring": "PPR"}'
```
