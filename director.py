import time
import random
from brain import AI_Brain
from worker import VideoWorker
from config import PILLARS

def main():
    brain = AI_Brain()
    worker = VideoWorker()
    
    print("🚀 Video Factory Started. Total Automation Active.")
    
    while True:
        try:
            # 1. Pick a Pillar
            pillar = random.choice(list(PILLARS.keys()))
            
            # 2. Brain generates script (Simplified)
            script = "Example script for " + pillar
            visual_prompt = PILLARS[pillar] + " high quality cinematic."
            
            # 3. Work
            voice_path = worker.generate_voiceover(script, pillar)
            segments = worker.generate_video(visual_prompt, pillar)
            final_clip = worker.stitch_and_finalize(segments, voice_path, pillar)
            
            # 4. Record to History on Drive
            brain.save_to_history(pillar, script[:50])
            
            print(f"✅ Finished: {final_clip}. Moving to next...")
            
        except Exception as e:
            print(f"❌ Error: {e}. Retrying in 60s...")
            time.sleep(60)

if __name__ == "__main__":
    main()
