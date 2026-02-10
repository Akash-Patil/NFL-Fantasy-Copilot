# Quick Deployment Guide

Deploy your Fantasy Copilot app in ~15 minutes.

## 🎯 Quick Overview

```
1. Redis (Upstash)     → 5 min
2. Backend (Fly.io)    → 5 min
3. Frontend (Vercel)   → 5 min
Total: ~15 minutes
```

---

## ✅ Pre-Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] Perplexity API key ready
- [ ] Fly.io account created
- [ ] Vercel account created  
- [ ] Upstash account created

---

## 🚀 Deployment Steps

### 1️⃣ Redis (5 minutes)

1. Go to https://upstash.com → Create Database
2. Name: `fantasy-copilot-redis`
3. Region: `us-east-1` (or closest to you)
4. Save these values:
   ```
   REDIS_HOST: __________.upstash.io
   REDIS_PASSWORD: __________
   ```

### 2️⃣ Backend (5 minutes)

```bash
cd backend

# Login & create app
fly auth login
fly launch --no-deploy

# Set secrets
fly secrets set PERPLEXITY_API_KEY=your_key
fly secrets set REDIS_HOST=your-db.upstash.io
fly secrets set REDIS_PASSWORD=your_password

# Deploy
fly deploy

# Save URL: https://__________.fly.dev
```

### 3️⃣ Frontend (5 minutes)

**Via Vercel Dashboard:**

1. Go to https://vercel.com → New Project
2. Import from GitHub
3. Settings:
   - Root Directory: `frontend`
   - Framework: Vite
   - Environment Variable:
     - `VITE_API_URL` = `https://your-backend.fly.dev`
4. Deploy

**Save URL:** `https://__________.vercel.app`

### 4️⃣ Connect Them

```bash
cd backend

# Update main.py CORS with your Vercel URL
# Then redeploy
fly deploy
```

---

## 🧪 Test Your Deployment

1. **Frontend:** Open `https://your-app.vercel.app`
2. **Backend Health:** `https://your-backend.fly.dev/health`
3. **API Docs:** `https://your-backend.fly.dev/docs`
4. **Test comparison:** Compare two players
5. **Check cache:** `https://your-backend.fly.dev/metrics`

---

## 📝 Save Your URLs

```
Frontend:  https://_________________.vercel.app
Backend:   https://_________________.fly.dev
Redis:     _________________.upstash.io
```

---

## 🐛 Common Issues

### "CORS error"
→ Update backend `main.py` CORS with your Vercel URL, then `fly deploy`

### "Can't connect to backend"
→ Check `VITE_API_URL` in Vercel environment variables

### "Redis connection failed"
→ Verify `REDIS_HOST` and `REDIS_PASSWORD` secrets in Fly.io

---

## 📚 Full Guide

For detailed instructions, see `FULL_DEPLOYMENT.md`

---

## 🎤 Demo Commands

```bash
# Check backend status
fly status

# View backend logs
fly logs

# Check cache metrics
curl https://your-backend.fly.dev/metrics

# Test API
curl https://your-backend.fly.dev/health
```

---

## ✨ You're Live!

Your app is now running in production! 🎉

Share your demo: `https://your-app.vercel.app`
