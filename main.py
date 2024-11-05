from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os
import json
import secrets
from typing import Dict
from datetime import datetime
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions
)
from openai import OpenAI

load_dotenv()

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class TranscriptionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.transcripts: Dict[str, list] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.connections[client_id] = websocket
        self.transcripts[client_id] = []
        
    def disconnect(self, client_id: str):
        self.connections.pop(client_id, None)
        return self.transcripts.pop(client_id, [])
        
    def add_transcript(self, client_id: str, text: str):
        if client_id in self.transcripts:
            self.transcripts[client_id].append(text)
            
    async def send_transcript(self, client_id: str, text: str):
        if client_id in self.connections:
            await self.connections[client_id].send_json({
                "type": "transcript",
                "text": text
            })

manager = TranscriptionManager()

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    with open("static/index.html") as f:
        return f.read()

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    client_id = secrets.token_urlsafe(16)
    await manager.connect(websocket, client_id)
    print("connection open")
    
    try:
        # Initialize Deepgram
        deepgram = DeepgramClient(
            os.getenv("DG_API_KEY"),
            DeepgramClientOptions(options={"keepalive": "true"})
        )
        
        connection = deepgram.listen.asynclive.v("1")
        
        # Set up message handler
        async def handle_message(self, result, **kwargs):
            if result.is_final:
                transcript = result.channel.alternatives[0].transcript
                if transcript.strip():
                    manager.add_transcript(client_id, transcript)
                    await manager.send_transcript(client_id, transcript)
        
        connection.on(LiveTranscriptionEvents.Transcript, handle_message)
        
        # Configure live transcription
        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            smart_format=True
        )
        
        await connection.start(options)
        
        # Process incoming audio
        try:
            while True:
                audio_data = await websocket.receive_bytes()
                await connection.send(audio_data)
        except Exception as e:
            print(f"Error processing audio: {e}")
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Clean up
        transcript = manager.disconnect(client_id)
        print("connection closed")

@app.post("/generate-mom")
async def generate_mom(request: Request):
    try:
        data = await request.json()
        transcript = data.get("transcript", "")
        
        if not transcript:
            raise HTTPException(status_code=400, detail="No transcript provided")
            
        client = OpenAI(api_key=os.getenv("OPEN_AI_TOKEN"))
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        prompt = f"""
        Generate minutes of meeting from the following transcript. Only include information that is 
        explicitly mentioned in the transcript. Do not make assumptions about deadlines, statuses, 
        or tasks unless they are clearly stated in the conversation.
        
        Generate detailed minutes of meeting from this transcript and format it with clear spacing and structure.
        Format the output with these sections (only include sections that have content from the transcript)
        Use the following format:

        # Minutes of Meeting

        ## Meeting Date
        {current_date}

        ## Participants
        - [Name] ([Role])
        - [Name] ([Role])

        ## Discussion Points
        1. [Point 1]
        2. [Point 2]


        ## Action Items (table format)
        | Assignee | Task | Status | Deadline |
        |----------|------|--------|----------|
        | [Name] | [Task Description] | [Status] | [Date] |
        
        ## Decisions Made
        - [Decision 1]
        - [Decision 2]

        ## Next Steps
        - [Step 1]
        - [Step 2]
        
        ## Meeting Conclusion: 
        Brief summary of what was actually discussed
        ... 
        
        If no clear tasks, deadlines, or next steps were mentioned, simply summarize the discussion 
        without including those sections.
        
        If there is mention about project status and deadlines please generate the table of Action Items.
        
        Make sure to format all tables properly with markdown table syntax and include proper headers and sections.
        
        Transcript: {transcript}
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        
        mom = response.choices[0].message.content
        return JSONResponse(content={"mom": mom})
        
    except Exception as e:
        print(f"Error generating MoM: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)