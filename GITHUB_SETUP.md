# 🔧 Configuração do GitHub para API StackSpot

Este guia explica como configurar as variáveis de ambiente no GitHub para que a API funcione corretamente.

## 📋 Pré-requisitos

- Conta no StackSpot
- Repositório no GitHub
- Credenciais da API StackSpot (CLIENT_ID e CLIENT_SECRET)

## 🔐 Configurando Secrets no GitHub

### 1. Acessar as Configurações do Repositório

1. Vá para o seu repositório no GitHub
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Secrets and variables** > **Actions**

### 2. Adicionar Repository Secrets

Clique em **New repository secret** e adicione as seguintes variáveis:

#### ✅ REALM
- **Name**: `REALM`
- **Secret**: `stackspot-freemium` (ou seu realm específico)

#### ✅ CLIENT_ID
- **Name**: `CLIENT_ID`
- **Secret**: Seu Client ID do StackSpot (ex: `06c995f0-372e-4051-b69b-546360861554`)

#### ✅ CLIENT_SECRET
- **Name**: `CLIENT_SECRET`
- **Secret**: Seu Client Secret do StackSpot (ex: `w0Pz29804igZUXijCzuhamhzVS69hD29joUX8U3IW21xr6aPr3bZk3GKIMC925dA`)

### 3. Variáveis Opcionais

Você também pode adicionar:

#### PORT (opcional)
- **Name**: `PORT`
- **Secret**: `5000` (ou a porta desejada)

#### NODE_ENV (opcional)
- **Name**: `NODE_ENV`
- **Secret**: `production`

## 🚀 Deploy Automático com GitHub Actions

### Arquivo de Workflow

O arquivo `.github/workflows/deploy.yml` será criado automaticamente para fazer o deploy da API.

### Configuração do Ambiente

As variáveis serão automaticamente injetadas no ambiente durante o deploy:

```yaml
env:
  REALM: ${{ secrets.REALM }}
  CLIENT_ID: ${{ secrets.CLIENT_ID }}
  CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
  PORT: ${{ secrets.PORT }}
  NODE_ENV: ${{ secrets.NODE_ENV }}
```

## 🔍 Verificação

### 1. Logs da Aplicação

Quando a API iniciar, você verá:

```
✅ Environment variables loaded successfully
🚀 Server listening on port 5000
```

### 2. Em Caso de Erro

Se alguma variável estiver faltando, você verá:

```
❌ Missing required environment variables:
  - CLIENT_ID
  - CLIENT_SECRET
📝 Please set these variables in your environment or .env file
```

## 🛠️ Desenvolvimento Local

### 1. Criar arquivo .env

```bash
cp .env.example .env
```

### 2. Editar .env com suas credenciais

```env
REALM=stackspot-freemium
CLIENT_ID=seu-client-id-aqui
CLIENT_SECRET=seu-client-secret-aqui
PORT=5000
NODE_ENV=development
```

### 3. Executar localmente

```bash
npm install
npm start
```

## 📚 Referências

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [StackSpot API Documentation](https://docs.stackspot.com/)
- [Node.js Environment Variables](https://nodejs.org/en/learn/command-line/how-to-read-environment-variables-from-nodejs)

## 🆘 Troubleshooting

### Problema: "Missing required environment variables"

**Solução**: Verifique se todas as variáveis estão configuradas corretamente no GitHub Secrets.

### Problema: "Authentication failed"

**Solução**: Verifique se CLIENT_ID e CLIENT_SECRET estão corretos e válidos.

### Problema: API não responde

**Solução**: Verifique se a porta está disponível e se o NODE_ENV está configurado corretamente.

---

**💡 Dica**: Mantenha suas credenciais sempre seguras e nunca as commite no código!