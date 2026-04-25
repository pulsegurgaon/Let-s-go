import time
import random
import requests
from groq import Groq
from config import PILLAR_CONFIG

# --- CONFIGURATION ---
BACKEND_URL = "http://localhost:8000/generate"
# PASTE YOUR KEY HERE FOR THE AUTOMATED LOOP
GROQ_KEY = "gsk_xxxx..." 
# 30 seconds of video takes time to render. 
# Set delay to 15-20 mins (900-1200 seconds) so the queue doesn't overflow.
DELAY_BETWEEN_VIDEOS = 1800

def get_automated_idea(pillar):
    client = Groq(api_key=GROQ_KEY)
    prompt = f"""
    Create a viral, high-intensity 30-second video concept for the '{pillar}' category.
    The idea should have a clear beginning, middle, and shocking end.
    Output ONLY the one-sentence seed idea.
    """
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return completion.choices[0].message.content

def run_factory():
    pillars = list(PILLAR_CONFIG.keys())
    print("--- 🏭 AUTOMATED 30s VIDEO FACTORY ONLINE ---")
    
    while True:
        pillar = random.choice(pillars)
        print(f"\n[Director] 🎯 Target Pillar: {pillar}")
        
        try:
            # 1. Dream up the idea
            seed_idea = get_automated_idea(pillar)
            print(f"[Director] 💡 New Idea: {seed_idea}")
            
            # 2. Send to Backend
            payload = {
                "pillar": pillar,
                "seed_idea": seed_idea,
                "user_key": GROQ_KEY
            }
            response = requests.post(BACKEND_URL, json=payload)
            
            if response.status_code == 200:
                print(f"[Director] ✅ Task queued. Next video in {DELAY_BETWEEN_VIDEOS/60} mins.")
            else:
                print(f"[Director] ⚠️ Backend Busy: {response.text}")
                
        except Exception as e:
            print(f"[Director] ❌ Loop Error: {e}")
        
        # 3. Wait for GPU to finish the 30s render
        time.sleep(DELAY_BETWEEN_VIDEOS)

if __name__ == "__main__":
    run_factory()
