# 🚀 Quick Deployment Guide

## Deploy to Vercel in 5 Minutes

### Step 1: Prepare Your Code
```bash
# Make sure you're in the fantasy-frontend directory
cd fantasy-frontend

# Install dependencies (if not done already)
npm install
```

### Step 2: Create GitHub Repository

1. Go to GitHub and create a new repository (e.g., `fantasy-copilot-frontend`)
2. Initialize and push:

```bash
git init
git add .
git commit -m "Initial commit - Fantasy Copilot Frontend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fantasy-copilot-frontend.git
git push -u origin main
```

### Step 3: Deploy on Vercel

1. **Go to [vercel.com](https://vercel.com)**
2. **Sign in with GitHub**
3. **Click "New Project"**
4. **Import your repository** (`fantasy-copilot-frontend`)
5. **Configure:**
   - Framework Preset: `Vite`
   - Root Directory: `./`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. **Add Environment Variable:**
   - Name: `VITE_API_URL`
   - Value: Your backend URL (e.g., `https://your-backend.onrender.com`)
7. **Click "Deploy"**

### Step 4: Done! 🎉

Your app will be live at: `https://your-project-name.vercel.app`

---

## Alternative: Deploy Without GitHub

If you don't want to use GitHub:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? fantasy-copilot-frontend
# - Directory? ./
# - Override settings? No

# Add environment variable
vercel env add VITE_API_URL
# Enter your backend URL when prompted

# Production deployment
vercel --prod
```

---

## Update Your Deployment

When you make changes:

### With GitHub:
```bash
git add .
git commit -m "Update: description of changes"
git push
# Vercel auto-deploys on push
```

### With Vercel CLI:
```bash
vercel --prod
```

---

## Connect Your Custom Domain

1. Go to Vercel Dashboard → Your Project → Settings → Domains
2. Add your domain
3. Update DNS records as instructed
4. Done!

---

## Important: Update Backend CORS

Make sure your FastAPI backend allows requests from your Vercel domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-project-name.vercel.app",  # Your Vercel domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

### Deployment fails?
- Check build logs in Vercel dashboard
- Ensure `package.json` has correct scripts
- Verify all files are committed to git

### Can't connect to backend?
- Check `VITE_API_URL` environment variable in Vercel
- Verify backend CORS settings
- Test backend directly with curl/Postman

### Changes not showing?
- Hard refresh: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
- Clear browser cache
- Check Vercel deployment logs

---

## Cost

**Vercel Free Tier includes:**
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Perfect for personal projects!

No credit card required for hobby projects! 🎉
