# 🚀 Deploy Guide - StackSpot API

This guide shows how to deploy the API on different platforms.

## 🎯 Supported Platforms

- [Heroku](#heroku)
- [Railway](#railway)
- [Vercel](#vercel)
- [Render](#render)
- [DigitalOcean App Platform](#digitalocean)

---

## 🟣 Heroku

### 1. Configure Secrets in GitHub

```
HEROKU_API_KEY=your-heroku-api-key
HEROKU_APP_NAME=your-app-name
HEROKU_EMAIL=your-email@heroku.com
```

### 2. Manual Deploy

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Configure variables
heroku config:set REALM=stackspot-freemium
heroku config:set CLIENT_ID=your-client-id
heroku config:set CLIENT_SECRET=your-client-secret
heroku config:set NODE_ENV=production

# Deploy
git push heroku main
```

---

## 🚂 Railway

### 1. Configure Secrets in GitHub

```
RAILWAY_TOKEN=your-railway-token
```

### 2. Manual Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Configure variables
railway variables set REALM=stackspot-freemium
railway variables set CLIENT_ID=your-client-id
railway variables set CLIENT_SECRET=your-client-secret
railway variables set NODE_ENV=production

# Deploy
railway up
```

---

## ▲ Vercel

### 1. Configure Secrets in GitHub

```
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-org-id
VERCEL_PROJECT_ID=your-project-id
```

### 2. Create vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api.mjs",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api.mjs"
    }
  ],
  "env": {
    "REALM": "@realm",
    "CLIENT_ID": "@client_id",
    "CLIENT_SECRET": "@client_secret",
    "NODE_ENV": "production"
  }
}
```

### 3. Manual Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

---

## 🎨 Render

### 1. Configuration via Dashboard

1. Connect your GitHub repository
2. Configure environment variables:
   - `REALM=stackspot-freemium`
   - `CLIENT_ID=your-client-id`
   - `CLIENT_SECRET=your-client-secret`
   - `NODE_ENV=production`

### 2. Build Configuration

```yaml
# render.yaml
services:
  - type: web
    name: plastic-degradation-api
    env: node
    buildCommand: npm install
    startCommand: npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: REALM
        fromSecret: REALM
      - key: CLIENT_ID
        fromSecret: CLIENT_ID
      - key: CLIENT_SECRET
        fromSecret: CLIENT_SECRET
```

---

## 🌊 DigitalOcean App Platform

### 1. Configuration via .do/app.yaml

```yaml
name: plastic-degradation-api
services:
- name: api
  source_dir: /
  github:
    repo: your-username/your-repository
    branch: main
  run_command: npm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: NODE_ENV
    value: production
  - key: REALM
    value: stackspot-freemium
  - key: CLIENT_ID
    type: SECRET
  - key: CLIENT_SECRET
    type: SECRET
```

---

## 🔧 Local Configuration for Development

### 1. Install dependencies

```bash
npm install
```

### 2. Configure .env

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 3. Run

```bash
# Development (with watch)
npm run dev

# Production
npm start
```

---

## 🔍 Deploy Verification

### Health Check

All platforms should respond at:

```
GET /health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2025-01-05T21:39:00.000Z",
  "environment": "production"
}
```

### API Test

```bash
# Test main endpoint
curl https://your-app.herokuapp.com/

# Test with data
curl -X POST https://your-app.herokuapp.com/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

---

## 🆘 Troubleshooting

### Error: "Missing environment variables"

**Solution**: Check that all variables are configured on the platform.

### Error: "Port already in use"

**Solution**: Use `process.env.PORT` in code (already configured).

### Error: "Module not found"

**Solution**: Check that `"type": "module"` is in package.json.

### Deploy fails in GitHub Actions

**Solution**: Check that all secrets are configured correctly.

---

## 📊 Monitoring

### Logs

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Vercel
vercel logs
```

### Metrics

- Response time
- Error rate
- Memory usage
- Number of requests

---

**💡 Tip**: Always test locally before deploying!