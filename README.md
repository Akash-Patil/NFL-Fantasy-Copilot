# Fantasy Copilot 🏈

AI-powered NFL fantasy football player comparison tool with intelligent caching and position-specific analysis.

[![Deploy Status](https://img.shields.io/badge/deploy-ready-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

## 🎯 Features

- **AI-Powered Analysis:** Uses Perplexity API for intelligent player comparisons
- **Position-Specific Prompts:** Tailored analysis for QB, RB, WR, TE
- **Smart Caching:** Redis-based caching for cost optimization and speed
- **Real-time Stats:** Current 2024-25 season statistics
- **Multiple Scoring Formats:** PPR, Half-PPR support
- **Beautiful UI:** Modern React interface with dark mode
- **Production Ready:** Deployed on Fly.io + Vercel

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  ← Vercel
│   (Vite + Axios)│
└────────┬────────┘
         │ HTTPS
         ↓
┌─────────────────┐
│  FastAPI Backend│  ← Fly.io
│   (Python 3.13) │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌──────────┐
│ Redis  │ │Perplexity│
│ Cache  │ │   API    │
└────────┘ └──────────┘
```

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Redis (Docker):**
```bash
docker-compose up -d redis
```

### Deploy to Production

See `QUICK_START.md` for 15-minute deployment guide.

## 📦 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Perplexity API** - AI-powered player analysis
- **Redis** - Response caching
- **Pydantic** - Data validation
- **Python 3.13** - Latest Python features

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **Tailwind CSS** - Styling (if applicable)

### Infrastructure
- **Fly.io** - Backend hosting
- **Vercel** - Frontend hosting
- **Upstash** - Managed Redis
- **Docker** - Containerization

## 📊 API Endpoints

```
GET  /                  # API info
GET  /health            # Health check
GET  /metrics           # Cache performance
POST /start-sit         # Player comparison
GET  /docs              # Interactive API docs
```

## 🎮 Usage Example

```bash
curl -X POST https://your-api.fly.dev/start-sit \
  -H "Content-Type: application/json" \
  -d '{
    "players": ["Tyreek Hill", "Justin Jefferson"],
    "position": "WR",
    "scoring": "PPR"
  }'
```

Response:
```json
{
  "decision": "Tyreek Hill",
  "confidence": "High",
  "reason": "Leads in PPG (most important metric)",
  "player1_stats": {
    "name": "Tyreek Hill",
    "ppg": 15.2,
    "targets_per_game": 8.5,
    ...
  },
  "from_cache": false
}
```

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
PERPLEXITY_API_KEY=your_key
REDIS_HOST=localhost
REDIS_PORT=6379
CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600
```

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000
```

## 📈 Performance

- **Cache Hit Rate:** 50%+ typical
- **Response Time:** 
  - Cache Hit: ~5ms
  - Cache Miss: ~2-5s (Perplexity API call)
- **Cost Savings:** ~$0.005 per cached request

## 🔒 Security

- ✅ API keys stored as secrets (not in code)
- ✅ CORS configured for production domains
- ✅ Environment-based configuration
- ✅ No sensitive data in logs
- ✅ Health checks and monitoring

## 📚 Documentation

- **[FULL_DEPLOYMENT.md](./FULL_DEPLOYMENT.md)** - Complete deployment guide
- **[QUICK_START.md](./QUICK_START.md)** - 15-minute quick deploy
- **[backend/DEPLOYMENT.md](./backend/DEPLOYMENT.md)** - Backend-specific deployment
- **[backend/CACHING_STRUCTURE.md](./backend/CACHING_STRUCTURE.md)** - Cache architecture

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Test Docker build
docker build -t fantasy-backend .

# Test API locally
python backend/test_api.py
```

## 🎤 Interview Talking Points

This project demonstrates:

1. **Full-Stack Development:** React + FastAPI
2. **AI Integration:** Perplexity API for intelligent analysis
3. **Performance Optimization:** Redis caching, reduces costs by 50%+
4. **Production Deployment:** Dockerized, deployed to cloud
5. **Observability:** Health checks, metrics endpoints, logging
6. **Cost Optimization:** Auto-scaling, caching, free-tier friendly
7. **Modern Best Practices:** Type safety, environment config, CI/CD ready

## 📊 Project Structure

```
fantasy-copilot/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── cache.py             # Redis client
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   ├── perplexity_client.py # AI client
│   ├── prompts/             # Position-specific prompts
│   ├── parsers/             # Response parsers
│   ├── Dockerfile           # Production container
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   └── App.jsx          # Main app
│   ├── package.json         # Node dependencies
│   └── vercel.json          # Vercel config
├── docker-compose.yml       # Local Redis
└── README.md               # You are here!
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - feel free to use for personal or commercial projects.

## 🙏 Acknowledgments

- **Perplexity AI** - For the amazing API
- **FastAPI** - For the excellent framework
- **Fly.io** - For simple, affordable hosting
- **Vercel** - For effortless frontend deployment

## 📧 Contact

Built for SDE/FDE interview demonstration.

---

⭐ Star this repo if you find it helpful!

**Live Demo:** [Your Vercel URL]  
**API Docs:** [Your Fly.io URL]/docs
