import time
import random
import requests
from config import PILLAR_CONFIG

# --- SETTINGS ---
BACKEND_URL = "http://localhost:8000/generate"
GROQ_KEY = "your_key_here" # Or pass it as an argument
DELAY_BETWEEN_VIDEOS = 600 # 10 minutes (Wait for GPU to finish)

PILLARS = list(PILLAR_CONFIG.keys())

def get_automated_idea(pillar, key):
    """
    Ask Groq to come up with a viral, creative seed idea 
    for a specific pillar so you don't have to.
    """
    from groq import Groq
    client = Groq(api_key=key)
    
    prompt = f"Come up with one unique, viral, and high-concept video idea for the '{pillar}' category. Give me only the idea, one sentence maximum."
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )
    return completion.choices[0].message.content

def run_factory():
    print("--- 🏭 AI VIDEO FACTORY STARTED ---")
    
    while True:
        # 1. Pick a random pillar
        pillar = random.choice(PILLARS)
        print(f"\n[Director] Selected Pillar: {pillar}")
        
        # 2. Generate a new seed idea automatically
        idea = get_automated_idea(pillar, GROQ_KEY)
        print(f"[Director] Generated Idea: {idea}")
        
        # 3. Send to your Backend API
        payload = {
            "pillar": pillar,
            "seed_idea": idea,
            "user_key": GROQ_KEY
        }
        
        try:
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                print(f"[Director] Job sent to GPU. Sleeping for {DELAY_BETWEEN_VIDEOS}s...")
            else:
                print(f"[Director] Error: {response.text}")
        except Exception as e:
            print(f"[Director] Connection failed: {e}")
        
        # 4. Wait for the video to finish before starting the next one
        time.sleep(DELAY_BETWEEN_VIDEOS)

if __name__ == "__main__":
    run_factory()
