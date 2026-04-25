import os
import json
import subprocess
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from brain import AI_Brain
from worker import VideoWorker
from dotenv import load_dotenv

# Load environment variables (for local testing, though key comes from UI)
load_dotenv()

app = FastAPI(title="AI Video Production Pipeline")

# Initialize Worker once to keep model in VRAM
# Initialize Brain (logic for Groq)
brain = AI_Brain()
worker = VideoWorker()

# --- Data Models ---
class GenerationRequest(BaseModel):
    pillar: str
    seed_idea: str
    user_key: str  # Received from the Streamlit Frontend

# --- Helper Functions ---

def ensure_history_exists():
    """Checks if history.json exists, creates it if not."""
    if not os.path.exists("history.json"):
        with open("history.json", "w") as f:
            json.dump({}, f)
        print("--- 📝 Created new history.json ---")

def upload_to_drive(file_path):
    """
    Uses Rclone to push the finished video to Google Drive.
    Assumes you have configured a remote named 'mydrive' via 'rclone config'.
    """
    try:
        # Pushes to a folder named 'AI_Videos' on your Google Drive
        print(f"--- ☁️ Uploading {file_path} to Google Drive... ---")
        subprocess.run(["rclone", "copy", file_path, "mydrive:AI_Videos"], check=True)
        print(f"--- ✅ Successfully uploaded to Drive ---")
    except Exception as e:
        print(f"--- ❌ Rclone Upload Failed: {e} ---")

def process_video_task(pillar: str, seed_idea: str, user_key: str):
    """
    The background sequence: 
    1. Expand Prompt -> 2. Generate Video -> 3. Upload to Drive
    """
    print(f"\n--- 🚀 Starting Task for Pillar: {pillar} ---")
    
    try:
        # 1. Expand the idea into a 500+ word master prompt using the user's key
        detailed_prompt = brain.generate_detailed_prompt(pillar, seed_idea, user_key)
        
        if "Error" in detailed_prompt:
            print(f"--- ❌ Brain Error: {detailed_prompt} ---")
            return

        # 2. Feed the detailed prompt into the GPU Worker (LTX-Video/SkyReels)
        video_path = worker.generate(detailed_prompt, pillar)
        
        # 3. If video is successful, push to Google Drive
        if video_path and os.path.exists(video_path):
            upload_to_drive(video_path)
            print(f"--- 🏁 Full Pipeline Complete for {video_path} ---")
        else:
            print("--- ❌ GPU worker failed to produce a file. ---")

    except Exception as e:
        print(f"--- ❌ Pipeline Crash: {e} ---")

# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    ensure_history_exists()

@app.get("/")
def health_check():
    return {"status": "Online", "mode": "OVH GPU Trial", "storage": "Rclone/GoogleDrive"}

@app.post("/generate")
async def generate_video(request: GenerationRequest, background_tasks: BackgroundTasks):
    # Verify Pillar exists in config
    from config import PILLAR_CONFIG
    if request.pillar not in PILLAR_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid Pillar Name")

    # Add task to background queue so the API returns instantly
    background_tasks.add_task(
        process_video_task, 
        request.pillar, 
        request.seed_idea, 
        request.user_key
    )
    
    return {
        "message": "Job Queued",
        "pillar": request.pillar,
        "status": "Check OVH Terminal for logs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
