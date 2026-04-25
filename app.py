import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from brain import AI_Brain
from worker import VideoWorker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Video Production Pipeline")

# Initialize our components
# Note: In a production trial, the Worker stays in VRAM
brain = AI_Brain()
worker = VideoWorker()

class GenerationRequest(BaseModel):
    pillar: str
    seed_idea: str

@app.get("/")
def read_root():
    return {"status": "Online", "engine": "LTX-Video", "logic": "Groq-Llama-3.3"}

def process_video_task(pillar: str, seed_idea: str):
    """
    The background task that runs the full pipeline
    """
    print(f"--- Processing Task: {seed_idea} for {pillar} ---")
    
    # 1. Ask Groq to expand the idea into a 500+ word master prompt
    detailed_prompt = brain.generate_detailed_prompt(pillar, seed_idea)
    
    if "Error" in detailed_prompt:
        print(f"Brain Error: {detailed_prompt}")
        return

    # 2. Feed the detailed prompt into the GPU Worker
    video_path = worker.generate(detailed_prompt, pillar)
    
    if video_path:
        print(f"SUCCESS: Video saved at {video_path}")
    else:
        print("FAILURE: GPU worker failed to generate video.")

@app.post("/generate")
async def generate_video(request: GenerationRequest, background_tasks: BackgroundTasks):
    # Validate if pillar exists in our config
    from config import PILLAR_CONFIG
    if request.pillar not in PILLAR_CONFIG:
        raise HTTPException(status_code=400, detail=f"Pillar {request.pillar} not found in config.")

    # Add the task to the background so the API doesn't time out
    background_tasks.add_task(process_video_task, request.pillar, request.seed_idea)
    
    return {
        "message": "Task queued successfully",
        "pillar": request.pillar,
        "idea": request.seed_idea,
        "status": "Check console for GPU progress"
    }

if __name__ == "__main__":
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
