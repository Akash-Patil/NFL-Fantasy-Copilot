# Deployment Guide - Fly.io

This guide covers deploying the Fantasy Copilot backend to Fly.io.

## Prerequisites

1. **Install Fly.io CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up / Log in:**
   ```bash
   fly auth signup  # or fly auth login
   ```

## Deployment Steps

### 1. Initialize Fly.io App (First Time Only)

```bash
cd backend
fly launch --no-deploy
```

This creates the `fly.toml` configuration. You can modify it as needed.

### 2. Set Up Redis

**Option A: Use Upstash Redis (Recommended - Free tier available)**
```bash
fly redis create
# Note the connection URL
fly secrets set REDIS_HOST=your-redis-host.upstash.io
fly secrets set REDIS_PORT=6379
fly secrets set REDIS_PASSWORD=your-password
```

**Option B: Use Fly.io Redis**
```bash
fly redis create --name fantasy-redis --region iad
fly redis attach fantasy-redis
```

### 3. Set Environment Secrets

```bash
# Required: Perplexity API Key
fly secrets set PERPLEXITY_API_KEY=your_api_key_here

# Optional: Override cache settings
fly secrets set CACHE_ENABLED=true
fly secrets set CACHE_TTL_SECONDS=3600
```

### 4. Deploy

```bash
fly deploy
```

### 5. Verify Deployment

```bash
# Check status
fly status

# View logs
fly logs

# Open in browser
fly open

# Check health endpoint
curl https://your-app.fly.dev/health

# Check metrics
curl https://your-app.fly.dev/metrics
```

## Testing the Deployed API

```bash
# Test start-sit endpoint
curl -X POST https://your-app.fly.dev/start-sit \
  -H "Content-Type: application/json" \
  -d '{
    "players": ["Tyreek Hill", "Justin Jefferson"],
    "position": "WR",
    "scoring": "PPR"
  }'
```

## Scaling

```bash
# Scale to specific VM size
fly scale vm shared-cpu-1x --memory 512

# Scale number of instances
fly scale count 2

# Auto-scale settings
fly autoscale set min=1 max=3
```

## Monitoring

```bash
# Live logs
fly logs -a fantasy-copilot-backend

# App metrics
fly dashboard

# SSH into container
fly ssh console
```

## Update Deployment

```bash
# After making code changes
fly deploy

# Restart without rebuilding
fly apps restart fantasy-copilot-backend
```

## Cost Optimization

The current configuration uses:
- **Shared CPU** (cheapest option)
- **256MB RAM** (minimal for this app)
- **Auto-stop/start** (scale to zero when idle)
- **Free tier friendly** (should stay within Fly.io free tier)

## Troubleshooting

### Build Fails
```bash
# Build locally first to test
docker build -t fantasy-backend .
docker run -p 8000:8000 fantasy-backend
```

### Redis Connection Issues
```bash
# Check Redis status
fly redis status fantasy-redis

# Verify secrets are set
fly secrets list
```

### App Crashes
```bash
# View detailed logs
fly logs --app fantasy-copilot-backend

# Check health checks
fly checks list
```

### Update Environment Variables
```bash
# Update a secret
fly secrets set CACHE_TTL_SECONDS=7200

# Unset a secret
fly secrets unset CACHE_ENABLED
```

## Production Checklist

- [ ] Set `PERPLEXITY_API_KEY` secret
- [ ] Configure Redis connection
- [ ] Test health endpoint
- [ ] Test metrics endpoint
- [ ] Test API endpoints
- [ ] Set up monitoring/alerts
- [ ] Configure custom domain (optional)
- [ ] Enable automatic deployments from GitHub (optional)

## FDE Interview Talking Points

When discussing this deployment:
1. **Containerization**: Multi-stage Docker build for optimized image size
2. **Infrastructure as Code**: fly.toml defines infrastructure declaratively
3. **Secrets Management**: API keys stored securely, not in code
4. **Health Checks**: Automatic monitoring and restart on failures
5. **Cost Optimization**: Auto-scaling to zero when idle
6. **Observability**: Built-in metrics and logging
7. **Zero-downtime deploys**: Fly.io handles rolling deployments
8. **Global CDN**: Can deploy to multiple regions easily

## Useful Commands Reference

```bash
# Deploy
fly deploy

# Status
fly status
fly logs

# Scale
fly scale count 2
fly scale vm shared-cpu-1x

# Secrets
fly secrets list
fly secrets set KEY=value

# SSH
fly ssh console

# Postgres (if needed later)
fly postgres create
fly postgres attach

# Destroy app
fly apps destroy fantasy-copilot-backend
```

## Next Steps

After backend is deployed:
1. Deploy frontend to Vercel/Netlify
2. Update frontend `.env` with backend URL
3. Set up CORS for production domain
4. Add custom domain (optional)
5. Set up CI/CD with GitHub Actions
