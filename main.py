from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI(title="Summarify")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

class TranscriptText(BaseModel):
    text: str

def summarize_meeting(transcript: str):
    """Generate summary and action items using Groq's Llama model"""
    
    prompt = f"""Analyze this meeting transcript and provide:

1. **Brief Summary** (2-3 sentences)
2. **Key Discussion Points** (bullet points)
3. **Action Items** (who needs to do what, with deadlines if mentioned)
4. **Decisions Made** (if any)

Transcript:
{transcript}

Format your response clearly with headers."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=[
                {"role": "system", "content": "You are an expert meeting analyst who creates concise, actionable summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML"""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/summarize/file")
async def summarize_from_file(file: UploadFile = File(...)):
    """Upload a transcript file and get summary"""

    if not file.filename.endswith(('.txt', '.srt', '.vtt')):
        raise HTTPException(status_code=400, detail="Only .txt, .srt, or .vtt files are supported")
    
    content = await file.read()
    transcript = content.decode('utf-8')
    
    if len(transcript.strip()) < 50:
        raise HTTPException(status_code=400, detail="Transcript too short (minimum 50 characters)")

    summary = summarize_meeting(transcript)
    
    return {
        "filename": file.filename,
        "transcript_length": len(transcript),
        "summary": summary
    }

@app.post("/summarize/text")
async def summarize_from_text(data: TranscriptText):
    """Paste transcript text and get summary"""
    
    if len(data.text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Transcript too short (minimum 50 characters)")
    
    summary = summarize_meeting(data.text)
    
    return {
        "transcript_length": len(data.text),
        "summary": summary
    }

@app.get("/health")
async def health_check():
    """Check if API is working"""
    return {"status": "healthy", "model": "llama-3.1-70b-versatile"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)