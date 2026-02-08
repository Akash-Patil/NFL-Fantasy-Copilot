# Fantasy Copilot Frontend

A React frontend for comparing fantasy football players and getting AI-powered recommendations.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Your FastAPI backend running

### Local Development

1. **Install dependencies:**
```bash
npm install
```

2. **Configure backend URL:**
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and set your backend URL
VITE_API_URL=http://localhost:8000
```

3. **Run development server:**
```bash
npm run dev
```

4. **Open in browser:**
```
http://localhost:3000
```

## 📦 Deploy to Vercel

### Method 1: GitHub (Recommended)

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fantasy-frontend.git
git push -u origin main
```

2. **Deploy on Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Add environment variable: `VITE_API_URL` = your backend URL
   - Click "Deploy"

### Method 2: Vercel CLI

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Deploy:**
```bash
vercel
```

3. **Add environment variable on Vercel dashboard:**
   - `VITE_API_URL` = your production backend URL

## 🔧 Configuration

### Environment Variables

- `VITE_API_URL`: Your FastAPI backend URL
  - Local: `http://localhost:8000`
  - Production: `https://your-backend.onrender.com`

## 🏗️ Build for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` folder.

## 📝 API Integration

The app expects your backend to have an endpoint:

```
POST /compare
{
  "player1": "Tyreek Hill",
  "player2": "Justin Jefferson",
  "position": "WR",
  "scoring": "PPR"
}
```

Response format:
```json
{
  "recommendation": "**Player Name: PPG=X | Tgt=Y...",
  "players_analyzed": ["Player 1", "Player 2"],
  "position": "WR",
  "scoring": "PPR"
}
```

## 🎨 Features

- ✅ Clean, modern UI with gradient design
- ✅ Real-time player comparison
- ✅ Highlights recommended player
- ✅ Shows confidence level
- ✅ Detailed stats breakdown
- ✅ Fully responsive (mobile-friendly)
- ✅ Error handling

## 🐛 Troubleshooting

### CORS Issues
If you get CORS errors, make sure your FastAPI backend has CORS enabled:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend Connection Failed
- Check that `VITE_API_URL` in `.env` matches your backend URL
- Verify your backend is running
- Check browser console for detailed error messages

## 📱 Screenshots

The app displays:
- Input form for two players
- Comparison results with stats
- Winner highlighted with star
- Confidence badge
- Reasoning explanation

## 🔗 Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling with gradients

## 📄 License

MIT
