# Complete Deployment Guide - Fantasy Copilot

Deploy your entire full-stack app (Backend + Frontend + Redis) to production.

## 🏗️ Architecture Overview

```
User Browser
    ↓
Vercel (Frontend - React)
    ↓ API calls
Fly.io (Backend - FastAPI)
    ↓ Cache
Upstash Redis (Managed Redis)
```

---

## 📋 Prerequisites

1. **Accounts (all free tier available):**
   - GitHub account
   - Fly.io account (https://fly.io/signup)
   - Vercel account (https://vercel.com/signup)
   - Upstash account (https://upstash.com)

2. **Tools:**
   ```bash
   # Install Fly CLI
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Install Vercel CLI (optional)
   npm install -g vercel
   ```

---

## 🚀 STEP 1: Deploy Redis (Upstash)

### Why Upstash?
- ✅ Free tier: 10,000 commands/day
- ✅ Managed, no server maintenance
- ✅ Global low-latency
- ✅ Perfect for serverless deployments

### Setup:

1. **Create Upstash Redis database:**
   - Go to https://upstash.com
   - Sign up / Log in
   - Click "Create Database"
   - Choose a name: `fantasy-copilot-redis`
   - Select region closest to Fly.io region (e.g., `us-east-1`)
   - Click "Create"

2. **Get connection details:**
   - Copy the following from your dashboard:
     - `UPSTASH_REDIS_REST_URL`
     - `UPSTASH_REDIS_REST_TOKEN`
   - Or use standard Redis connection:
     - Host: `your-db.upstash.io`
     - Port: `6379`
     - Password: `your-password`

---

## 🚀 STEP 2: Deploy Backend (Fly.io)

### 2.1 Initialize Fly.io

```bash
cd backend

# Login to Fly.io
fly auth login

# Launch app (creates fly.toml if needed)
fly launch --no-deploy
```

**During `fly launch`, answer:**
- App name: `fantasy-copilot-backend` (or your choice)
- Region: `iad` (US East) or closest to you
- PostgreSQL: **No**
- Redis: **No** (we're using Upstash)
- Deploy now: **No**

### 2.2 Set Secrets

```bash
# Required: Perplexity API Key
fly secrets set PERPLEXITY_API_KEY=your_perplexity_api_key

# Redis connection (from Upstash)
fly secrets set REDIS_HOST=your-db.upstash.io
fly secrets set REDIS_PORT=6379
fly secrets set REDIS_PASSWORD=your_upstash_password

# Cache settings (optional)
fly secrets set CACHE_ENABLED=true
fly secrets set CACHE_TTL_SECONDS=3600
```

### 2.3 Update CORS for Production

Before deploying, update `backend/main.py` CORS settings:

```python
# In backend/main.py, update CORS middleware:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local dev
        "https://your-app.vercel.app",  # Production frontend (update after Step 3)
        "https://*.vercel.app"  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2.4 Deploy

```bash
fly deploy
```

### 2.5 Verify Backend

```bash
# Check status
fly status

# View logs
fly logs

# Test health endpoint
fly apps open
# Then navigate to /health

# Or test with curl
curl https://your-app.fly.dev/health
curl https://your-app.fly.dev/metrics
```

**Save your backend URL:** `https://your-app.fly.dev`

---

## 🚀 STEP 3: Deploy Frontend (Vercel)

### 3.1 Prepare Frontend

1. **Update environment variables:**

```bash
cd ../frontend

# Edit .env file
VITE_API_URL=https://your-app.fly.dev
```

2. **Update API URL in code** (if hardcoded anywhere)

3. **Test build locally:**

```bash
npm run build
npm run preview
```

### 3.2 Push to GitHub

```bash
# From project root
cd ..
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 3.3 Deploy to Vercel

**Option A: Via Vercel Dashboard (Easiest)**

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Environment Variables:**
     - `VITE_API_URL` = `https://your-app.fly.dev`
5. Click "Deploy"

**Option B: Via Vercel CLI**

```bash
cd frontend

# Login
vercel login

# Deploy
vercel --prod

# Set environment variable
vercel env add VITE_API_URL
# Enter: https://your-app.fly.dev
# Select: Production
```

### 3.4 Get Frontend URL

After deployment completes, Vercel will give you a URL:
- `https://your-app.vercel.app`

---

## 🚀 STEP 4: Connect Frontend & Backend

### 4.1 Update Backend CORS

```bash
cd backend

# Update main.py with your Vercel URL
# Then redeploy
fly deploy
```

### 4.2 Test End-to-End

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Try comparing two players
3. Check cache is working:
   - First request: slower (calls API)
   - Second request: instant (from cache)
4. Check backend metrics: `https://your-app.fly.dev/metrics`

---

## ✅ Verification Checklist

- [ ] **Redis:** Connected and accessible from backend
- [ ] **Backend:** Deployed and healthy (`/health` returns 200)
- [ ] **Backend:** Cache working (`/metrics` shows hits/misses)
- [ ] **Frontend:** Deployed and accessible
- [ ] **Frontend:** Can reach backend API
- [ ] **CORS:** No CORS errors in browser console
- [ ] **End-to-end:** Can compare players successfully

---

## 📊 Production URLs

After deployment, you'll have:

```
Frontend:  https://your-app.vercel.app
Backend:   https://your-app.fly.dev
API Docs:  https://your-app.fly.dev/docs
Health:    https://your-app.fly.dev/health
Metrics:   https://your-app.fly.dev/metrics
Redis:     your-db.upstash.io:6379 (managed)
```

---

## 🔧 Ongoing Maintenance

### Update Backend

```bash
cd backend
# Make changes
fly deploy
```

### Update Frontend

```bash
cd frontend
# Make changes
git add .
git commit -m "Update frontend"
git push
# Vercel auto-deploys on push!
```

### Monitor Performance

```bash
# Backend logs
fly logs -a fantasy-copilot-backend

# Metrics
curl https://your-app.fly.dev/metrics

# Upstash dashboard
# View Redis metrics at upstash.com
```

---

## 💰 Cost Estimate

**Free Tier Limits:**

| Service | Free Tier | Your Usage | Cost |
|---------|-----------|------------|------|
| Fly.io | 3 VMs, 160GB bandwidth | 1 VM (256MB) | **$0** |
| Vercel | 100GB bandwidth, unlimited sites | 1 site | **$0** |
| Upstash | 10,000 commands/day | ~100-500/day | **$0** |

**Total: $0/month** (within free tiers)

---

## 🎯 Custom Domain (Optional)

### Add Custom Domain to Vercel

1. Go to Project Settings → Domains
2. Add your domain (e.g., `fantasycop ilot.com`)
3. Configure DNS (Vercel provides instructions)

### Add Custom Domain to Fly.io

```bash
fly certs add api.your-domain.com
```

Update frontend `.env`:
```
VITE_API_URL=https://api.your-domain.com
```

---

## 🐛 Troubleshooting

### Backend Issues

**Can't connect to Redis:**
```bash
# Check secrets are set
fly secrets list

# Test Redis connection
fly ssh console
> redis-cli -h your-db.upstash.io -p 6379 -a your-password ping
```

**App crashes:**
```bash
# View detailed logs
fly logs --app fantasy-copilot-backend

# Check status
fly status

# Restart
fly apps restart
```

### Frontend Issues

**Can't reach backend:**
- Check CORS settings in backend
- Verify `VITE_API_URL` is correct
- Check browser console for errors

**Build fails:**
```bash
# Test locally
npm run build

# Check Vercel build logs
# Dashboard → Project → Deployments → Click deployment → Logs
```

### CORS Errors

If you see CORS errors in browser:

1. **Add frontend URL to backend CORS:**
   ```python
   allow_origins=["https://your-actual-vercel-url.vercel.app"]
   ```

2. **Redeploy backend:**
   ```bash
   fly deploy
   ```

---

## 🚀 Quick Deploy Script

Save as `deploy.sh` in project root:

```bash
#!/bin/bash

echo "🚀 Deploying Fantasy Copilot..."

# Backend
echo "📦 Deploying backend to Fly.io..."
cd backend
fly deploy
cd ..

# Frontend
echo "🎨 Deploying frontend..."
cd frontend
git add .
git commit -m "Deploy frontend"
git push
cd ..

echo "✅ Deployment complete!"
echo "Frontend: Check Vercel dashboard"
echo "Backend: $(fly apps list | grep fantasy-copilot)"
```

---

## 📚 Additional Resources

- [Fly.io Docs](https://fly.io/docs/)
- [Vercel Docs](https://vercel.com/docs)
- [Upstash Docs](https://docs.upstash.com)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎤 Demo for Interviews

When showing this to interviewers:

1. **Show live app:** `https://your-app.vercel.app`
2. **Show API docs:** `https://your-app.fly.dev/docs`
3. **Show cache metrics:** `https://your-app.fly.dev/metrics`
4. **Explain architecture:** Frontend → Backend → Redis
5. **Discuss cost optimization:** Free tier, auto-scaling
6. **Highlight observability:** Health checks, metrics, logs
7. **Show code quality:** Docker, type safety, testing

Good luck! 🚀
