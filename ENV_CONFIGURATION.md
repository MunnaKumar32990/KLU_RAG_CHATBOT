# 🔧 Environment Configuration Guide

## Backend Configuration (`.env`)

Located at: `c:\Users\Asus\Downloads\KL_RAG_CHATBOT\.env`

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
OLLAMA_TEMPERATURE=0.3
OLLAMA_MAX_TOKENS=512

# RAG Configuration
TOP_K_RESULTS=3

# Logging
LOG_LEVEL=INFO
```

**What these do:**
- `OLLAMA_BASE_URL`: Where Ollama service is running
- `OLLAMA_MODEL`: Which LLM model to use (llama3.2:1b for low memory)
- `OLLAMA_TEMPERATURE`: Response randomness (0.3 = more focused)
- `OLLAMA_MAX_TOKENS`: Maximum response length (512 tokens)
- `TOP_K_RESULTS`: Number of documents to retrieve (3 for small model)
- `LOG_LEVEL`: Logging verbosity

## Frontend Configuration (`frontend/.env`)

Located at: `c:\Users\Asus\Downloads\KL_RAG_CHATBOT\frontend\.env`

```env
# Frontend Environment Variables
VITE_API_BASE_URL=http://localhost:8000
```

**What this does:**
- `VITE_API_BASE_URL`: Backend API endpoint (optional, proxy handles this)

## How They Connect

### Backend → Ollama
```
Backend (port 8000) → Ollama (port 11434)
```
- Backend calls Ollama API at `http://localhost:11434/api/generate`
- Configured via `OLLAMA_BASE_URL` in `.env`

### Frontend → Backend
```
Frontend (port 3000) → Backend (port 8000)
```
- Frontend makes API calls to `/api/*`
- Vite proxy forwards to `http://localhost:8000`
- Configured in `frontend/vite.config.js`:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/api/, '')
  }
}
```

## API Endpoints

### Backend Endpoints (Port 8000)

1. **POST /chat**
   - Send questions, get AI responses
   - Request: `{question: "your question"}`
   - Response: `{answer: "...", sources: [...]}`

2. **GET /health**
   - Check system health
   - Response: `{status: "healthy", vector_db_initialized: true, ollama_available: true}`

3. **GET /stats**
   - Get document statistics
   - Response: `{total_chunks: 19, status: "ready"}`

4. **GET /**
   - API information
   - Response: `{message: "...", version: "1.0.0"}`

### Frontend API Calls

The frontend uses `/api/*` prefix which gets proxied:
- `POST /api/chat` → `POST http://localhost:8000/chat`
- `GET /api/health` → `GET http://localhost:8000/health`
- `GET /api/stats` → `GET http://localhost:8000/stats`

## Testing Endpoints

### Test Backend Directly
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Stats
Invoke-RestMethod -Uri "http://localhost:8000/stats"

# Chat
$body = @{question = "Test question"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

### Test Frontend Proxy
```powershell
# From frontend perspective (through proxy)
Invoke-RestMethod -Uri "http://localhost:3000/api/health"
Invoke-RestMethod -Uri "http://localhost:3000/api/stats"
```

## Common Issues & Solutions

### Issue: Frontend can't connect to backend
**Error:** `ECONNREFUSED ::1:8000`

**Solution:**
1. Ensure backend is running: `uvicorn backend.main:app --reload`
2. Check backend is on port 8000: `netstat -ano | findstr :8000`
3. Restart both servers if needed

### Issue: Backend can't connect to Ollama
**Error:** `Connection refused to localhost:11434`

**Solution:**
1. Start Ollama: `ollama serve`
2. Or check if running: `Get-Process ollama`
3. Verify model is downloaded: `ollama list`

### Issue: Wrong model being used
**Error:** `model requires more system memory`

**Solution:**
1. Check `.env` has `OLLAMA_MODEL=llama3.2:1b`
2. Restart backend to reload config
3. Verify with: `ollama list`

## Environment Variables Priority

1. **System environment variables** (highest)
2. **`.env` file** in project root
3. **Default values** in `backend/config.py` (lowest)

To override, set system environment variable:
```powershell
$env:OLLAMA_MODEL = "llama3.2:1b"
```

## Production Deployment

For production, set these environment variables on your server:

```bash
export OLLAMA_BASE_URL=http://your-ollama-server:11434
export OLLAMA_MODEL=llama3.2:1b
export OLLAMA_TEMPERATURE=0.3
export OLLAMA_MAX_TOKENS=512
export TOP_K_RESULTS=3
export LOG_LEVEL=WARNING
```

Frontend build:
```bash
cd frontend
npm run build
# Serve the dist/ folder
```

## Summary

✅ **Backend `.env`**: Configured correctly with llama3.2:1b
✅ **Frontend `.env`**: Created with API base URL
✅ **Vite proxy**: Configured to forward `/api/*` to backend
✅ **Endpoints**: All 4 endpoints working (/chat, /health, /stats, /)

**Your environment is properly configured! 🎉**
