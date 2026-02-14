# Quick Start Guide - Ollama PATH Fix

## Issue
Ollama is installed but not recognized in new terminal sessions.

## Solution

### Option 1: Use Full Path (Works Immediately)
Instead of `ollama`, use the full path:

**PowerShell:**
```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull llama3
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve
```

**Command Prompt (cmd):**
```cmd
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" pull llama3
"%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve
```

### Option 2: Restart Terminal (Permanent Fix)
Close and reopen your terminal. The PATH will be updated automatically.

### Option 3: Refresh PATH in Current Session (PowerShell Only)
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
ollama --version
```

## Current Status
✅ Ollama v0.16.1 installed
🔄 LLaMA 3 model downloading (4.7 GB) - this may take 5-15 minutes depending on your internet speed

## Next Steps After Download Completes
1. Start Ollama server: `ollama serve` (or use full path)
2. Install Python dependencies: `pip install -r requirements.txt`
3. Index documents: `python scripts/index_data.py`
4. Start API server: `uvicorn backend.main:app --reload`
