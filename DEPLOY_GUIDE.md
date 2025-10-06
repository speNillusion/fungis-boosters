# 🚀 Guia de Deploy - API StackSpot

Este guia mostra como fazer deploy da API em diferentes plataformas.

## 🎯 Plataformas Suportadas

- [Heroku](#heroku)
- [Railway](#railway)
- [Vercel](#vercel)
- [Render](#render)
- [DigitalOcean App Platform](#digitalocean)

---

## 🟣 Heroku

### 1. Configurar Secrets no GitHub

```
HEROKU_API_KEY=sua-api-key-do-heroku
HEROKU_APP_NAME=nome-do-seu-app
HEROKU_EMAIL=seu-email@heroku.com
```

### 2. Deploy Manual

```bash
# Instalar Heroku CLI
npm install -g heroku

# Login
heroku login

# Criar app
heroku create nome-do-seu-app

# Configurar variáveis
heroku config:set REALM=stackspot-freemium
heroku config:set CLIENT_ID=seu-client-id
heroku config:set CLIENT_SECRET=seu-client-secret
heroku config:set NODE_ENV=production

# Deploy
git push heroku main
```

---

## 🚂 Railway

### 1. Configurar Secrets no GitHub

```
RAILWAY_TOKEN=seu-token-do-railway
```

### 2. Deploy Manual

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar projeto
railway init

# Configurar variáveis
railway variables set REALM=stackspot-freemium
railway variables set CLIENT_ID=seu-client-id
railway variables set CLIENT_SECRET=seu-client-secret
railway variables set NODE_ENV=production

# Deploy
railway up
```

---

## ▲ Vercel

### 1. Configurar Secrets no GitHub

```
VERCEL_TOKEN=seu-token-do-vercel
VERCEL_ORG_ID=seu-org-id
VERCEL_PROJECT_ID=seu-project-id
```

### 2. Criar vercel.json

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

### 3. Deploy Manual

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

---

## 🎨 Render

### 1. Configuração via Dashboard

1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente:
   - `REALM=stackspot-freemium`
   - `CLIENT_ID=seu-client-id`
   - `CLIENT_SECRET=seu-client-secret`
   - `NODE_ENV=production`

### 2. Configuração de Build

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

### 1. Configuração via .do/app.yaml

```yaml
name: plastic-degradation-api
services:
- name: api
  source_dir: /
  github:
    repo: seu-usuario/seu-repositorio
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

## 🔧 Configuração Local para Desenvolvimento

### 1. Instalar dependências

```bash
npm install
```

### 2. Configurar .env

```bash
cp .env.example .env
# Editar .env com suas credenciais
```

### 3. Executar

```bash
# Desenvolvimento (com watch)
npm run dev

# Produção
npm start
```

---

## 🔍 Verificação de Deploy

### Health Check

Todas as plataformas devem responder em:

```
GET /health
```

Resposta esperada:
```json
{
  "status": "ok",
  "timestamp": "2025-01-05T21:39:00.000Z",
  "environment": "production"
}
```

### Teste da API

```bash
# Testar endpoint principal
curl https://seu-app.herokuapp.com/

# Testar com dados
curl -X POST https://seu-app.herokuapp.com/predict \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

---

## 🆘 Troubleshooting

### Erro: "Missing environment variables"

**Solução**: Verifique se todas as variáveis estão configuradas na plataforma.

### Erro: "Port already in use"

**Solução**: Use `process.env.PORT` no código (já configurado).

### Erro: "Module not found"

**Solução**: Verifique se `"type": "module"` está no package.json.

### Deploy falha no GitHub Actions

**Solução**: Verifique se todos os secrets estão configurados corretamente.

---

## 📊 Monitoramento

### Logs

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Vercel
vercel logs
```

### Métricas

- Tempo de resposta
- Taxa de erro
- Uso de memória
- Número de requisições

---

**💡 Dica**: Sempre teste localmente antes de fazer deploy!