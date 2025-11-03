# 🎙️ Summarify - AI Meeting Summarizer

An AI-powered meeting transcript summarizer that extracts key points, action items, and decisions from meeting transcripts.

## Features

✨ Upload transcript files (.txt, .srt, .vtt)
📝 Paste text directly
🤖 AI-powered summarization using Llama 3.3
📋 Automatic action item extraction
🎯 Decision tracking
💜 Beautiful, responsive UI

## Tech Stack

- **Backend:** FastAPI + Python
- **AI:** Groq API (Llama 3.3)
- **Frontend:** Vanilla HTML/CSS/JavaScript

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/summarify.git
cd summarify
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Groq API key:
   - Get a free API key from https://console.groq.com/
   - Create a `.env` file:
```
   GROQ_API_KEY=your_api_key_here
```

5. Run the application:
```bash
python main.py
```

6. Open http://localhost:8000 in your browser

## Usage

1. Choose between uploading a file or pasting text
2. Add your meeting transcript
3. Click "Summarize"
4. Get instant AI-generated summaries with action items!


## License

MIT License

## Author

[Piyush Patrikar](https://github.com/PiyushCodess)
