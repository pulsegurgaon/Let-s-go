import torch
import os
import time
from diffusers import LTXVideoPipeline
from diffusers.utils import export_to_video
from datetime import datetime

class VideoWorker:
    def __init__(self, model_id="Lightricks/LTX-Video"):
        print(f"--- Initializing GPU Worker with {model_id} ---")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "./outputs"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Load the pipeline into GPU memory
        # Using bfloat16 to save VRAM while keeping high cinematic quality
        self.pipe = LTXVideoPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.bfloat16
        )
        self.pipe.to(self.device)
        
        # Enable memory optimizations
        self.pipe.enable_model_cpu_offload() 
        print("--- Worker Ready for Tasks ---")

    def generate(self, prompt, pillar_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{pillar_name}_{timestamp}.mp4"
        filepath = os.path.join(self.output_dir, filename)

        print(f"--- Starting Render for Pillar: {pillar_name} ---")
        print(f"Prompt Length: {len(prompt)} characters")

        try:
            # LTX-Video Generation Logic
            output = self.pipe(
                prompt=prompt,
                negative_prompt="low quality, blurry, distorted, messy textures, static, flickering",
                num_frames=161,      # Approx 5-7 seconds depending on FPS
                height=768,          # Vertical Height
                width=448,           # Vertical Width (9:16)
                num_inference_steps=50, 
                guidance_scale=3.5,
            ).frames[0]

            # Export to high-quality MP4
            export_to_video(output, filepath, fps=24)
            print(f"--- Render Complete: {filepath} ---")
            return filepath

        except Exception as e:
            print(f"--- GPU Error: {e} ---")
            return None

# Simple manual test loop
if __name__ == "__main__":
    worker = VideoWorker()
    # Test with a placeholder prompt
    test_prompt = "A cinematic shot of a sunset over digital dunes, 8k, highly detailed."
    worker.generate(test_prompt, "test_run")
