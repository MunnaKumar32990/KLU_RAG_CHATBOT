# College RAG Chatbot 🎓🤖

A production-ready Retrieval Augmented Generation (RAG) chatbot system for college-related queries using **LLaMA 3**, **FastAPI**, **ChromaDB**, and **HuggingFace Embeddings**.

## 🌟 Features

- ✅ **Local LLM**: Runs LLaMA 3 locally via Ollama (privacy-focused, no API costs)
- ✅ **RAG Pipeline**: Retrieves relevant documents before generating answers
- ✅ **Vector Database**: Persistent ChromaDB storage with HuggingFace embeddings
- ✅ **Document Sources**: Automatically cites source documents in responses
- ✅ **Production-Ready**: Clean architecture, comprehensive error handling, logging
- ✅ **REST API**: FastAPI with automatic OpenAPI documentation
- ✅ **Flexible**: Supports TXT, PDF, MD, DOCX file formats
- ✅ **Modular**: Clean separation of concerns for easy maintenance

## 📁 Project Structure

```
college-chatbot/
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Configuration variables
│   ├── rag_pipeline.py         # Retrieval + LLM logic
│   ├── document_loader.py      # Load & chunk documents
│   ├── vector_store.py         # ChromaDB setup & indexing
│   ├── schemas.py              # Pydantic request/response models
│   └── prompts/
│       └── system_prompt.txt   # LLM system prompt
│
├── data/                       # College documents (YOU add files here)
│   ├── admissions/
│   ├── fees/
│   ├── placements/
│   ├── academics/
│   ├── faculty/
│   └── hostel/
│
├── vector_db/                  # Persistent ChromaDB storage (auto-created)
│
├── scripts/
│   └── index_data.py           # Script to index documents
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.9+** installed
- **Ollama** installed ([download here](https://ollama.ai))

### 2. Install Ollama & LLaMA 3

#### Windows/Mac/Linux:

1. Download and install Ollama from: https://ollama.ai
2. Open a terminal and pull LLaMA 3:

```bash
ollama pull llama3
```

3. Start Ollama server (it usually auto-starts, but if not):

```bash
ollama serve
```

4. Verify it's running:

```bash
ollama list
```

You should see `llama3` in the list.

### 3. Setup Python Environment

```bash
# Navigate to project directory
cd KL_RAG_CHATBOT

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment

The `.env` file is already created with default values. Modify if needed:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
OLLAMA_TEMPERATURE=0.7
OLLAMA_MAX_TOKENS=2000
TOP_K_RESULTS=5
LOG_LEVEL=INFO
```

### 5. Add Your College Documents

Place your college documents in the `data/` directory under appropriate folders:

```
data/
├── admissions/      # Admission process, eligibility, etc.
├── fees/            # Fee structure documents
├── placements/      # Placement statistics, recruiters
├── academics/       # Courses, syllabus, grading
├── faculty/         # Faculty information
└── hostel/          # Hostel rules, facilities
```

**Supported formats**: `.txt`, `.pdf`, `.md`, `.docx`

**Sample documents are already included** to get you started!

### 6. Index Documents into Vector Database

This step loads all documents, chunks them, creates embeddings, and stores in ChromaDB:

```bash
python scripts/index_data.py
```

**Expected output**:
```
[Step 1/3] Loading and chunking documents from data/ directory...
[Step 2/3] Indexing XXX chunks into ChromaDB...
[Step 3/3] Verifying indexing...
✓ INDEXING COMPLETED SUCCESSFULLY!
```

### 7. Start the FastAPI Server

```bash
# Method 1: Direct Python
python -m backend.main

# Method 2: Using uvicorn (recommended for development)
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Server will start at**: `http://localhost:8000`

### 8. Test the API

#### Option A: Interactive API Documentation (Swagger UI)

Open your browser and go to: **http://localhost:8000/docs**

Try the `/chat` endpoint:
- Click on `POST /chat`
- Click "Try it out"
- Enter your question in the request body:
```json
{
  "question": "What are the admission requirements for B.Tech?",
  "conversation_id": null
}
```
- Click "Execute"

#### Option B: Using cURL

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are the placement statistics?\"}"
```

#### Option C: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"question": "What are the hostel fees?"}
)

result = response.json()
print("Answer:", result["answer"])
print("\nSources:")
for source in result["sources"]:
    print(f"- {source['source']} (score: {source['relevance_score']:.2f})")
```

## 📚 API Endpoints

### 1. **POST /chat** - Ask Questions

**Request**:
```json
{
  "question": "What is the B.Tech CSE fee?",
  "conversation_id": "optional-id"
}
```

**Response**:
```json
{
  "answer": "The B.Tech Computer Science & Engineering annual fee is ₹193,000...",
  "sources": [
    {
      "content": "Computer Science & Engineering - Tuition Fee: ₹150,000...",
      "source": "data/fees/btech_fees.txt",
      "relevance_score": 0.92
    }
  ],
  "conversation_id": null
}
```

### 2. **GET /health** - Health Check

**Response**:
```json
{
  "status": "healthy",
  "vector_db_initialized": true,
  "ollama_available": true
}
```

### 3. **GET /stats** - Document Statistics

**Response**:
```json
{
  "vector_db_initialized": true,
  "total_chunks": 245,
  "status": "ready"
}
```

### 4. **GET /** - Root Endpoint

Returns API information and available endpoints.

## 🔧 Configuration Options

### Vector Store Configuration (`backend/config.py`)

- `EMBEDDING_MODEL_NAME`: Default is `sentence-transformers/all-MiniLM-L6-v2`
- `CHUNK_SIZE`: Characters per chunk (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_RESULTS`: Number of documents to retrieve (default: 5)

### LLM Configuration (`.env`)

- `OLLAMA_MODEL`: LLM model name (default: `llama3`)
- `OLLAMA_TEMPERATURE`: Generation creativity 0-1 (default: 0.7)
- `OLLAMA_MAX_TOKENS`: Max response length (default: 2000)

## 🛠️ Development Workflow

### Adding New Documents

1. Add documents to appropriate `data/` subfolder
2. Re-run indexing:
```bash
python scripts/index_data.py
```
3. Restart the FastAPI server (if running)

### Updating System Prompt

Edit `backend/prompts/system_prompt.txt` to customize how the AI responds. Changes take effect on next server restart.

### Changing Embedding Model

Edit `EMBEDDING_MODEL_NAME` in `backend/config.py`. Popular alternatives:
- `sentence-transformers/all-mpnet-base-v2` (better quality, slower)
- `sentence-transformers/paraphrase-MiniLM-L6-v2` (faster, lower quality)

**Note**: Re-index after changing embedding model!

### Using a Different Ollama Model

```bash
# Pull different model
ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral

# Restart server
```

## 📊 Example Queries

Try asking:

- "What are the admission requirements for B.Tech?"
- "How much is the hostel fee?"
- "Tell me about placement statistics for CSE"
- "Who is the HOD of Computer Science department?"
- "What is the refund policy for fees?"
- "What are the hostel timings?"
- "List the top recruiters"

## 🐛 Troubleshooting

### Issue: "Could not connect to Ollama"

**Solution**: 
```bash
# Start Ollama server
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Issue: "Vector database not initialized"

**Solution**:
```bash
# Run the indexing script
python scripts/index_data.py
```

### Issue: Import errors

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: "Model 'llama3' not found"

**Solution**:
```bash
# Pull the model
ollama pull llama3
```

### Issue: Slow responses

**Causes**:
- Large document corpus → Reduce `TOP_K_RESULTS`
- CPU-only inference → Ollama uses CPU by default (GPU support available)
- Large context → Reduce `OLLAMA_MAX_TOKENS`

## 🚀 Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

Update `.env` with production values:
- Set specific CORS origins in `backend/main.py`
- Use environment-specific `LOG_LEVEL`
- Consider using a reverse proxy (nginx)

## 🔒 Security Considerations

- **CORS**: Update `allow_origins` in `backend/main.py` for production
- **Rate Limiting**: Add rate limiting middleware for public APIs
- **Authentication**: Add API key or OAuth for restricted access
- **Input Validation**: Already handled by Pydantic schemas
- **Data Privacy**: All processing happens locally (no data sent to external APIs)

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Feel free to customize and extend this project for your specific needs!

## 📧 Support

For issues or questions, create an issue in the repository or contact the development team.

---

**Built with ❤️ using LLaMA 3, FastAPI, and ChromaDB**
