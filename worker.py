import torch
import os
import subprocess
import time
from diffusers import SkyreelsVideoPipeline
from diffusers.utils import export_to_video
from datetime import datetime

class VideoWorker:
    def __init__(self, model_id="Skywork/SkyReels-V1-7B"):
        print(f"--- 🛠️ Initializing SkyReels Continuity Engine ---")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.output_dir = "./outputs"
        self.temp_dir = "./temp_segments"
        
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)
        if not os.path.exists(self.temp_dir): os.makedirs(self.temp_dir)

        # Load SkyReels Pipeline
        self.pipe = SkyreelsVideoPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.bfloat16
        )
        self.pipe.to(self.device)
        # Offloading helps manage VRAM during the long 45s loop
        self.pipe.enable_model_cpu_offload() 

    def _stitch_videos(self, segments, final_path):
        list_path = os.path.join(self.temp_dir, "list.txt")
        with open(list_path, "w") as f:
            for seg in segments:
                f.write(f"file '{os.path.abspath(seg)}'\n")
        
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
            "-i", list_path, "-c", "copy", final_path
        ]
        subprocess.run(cmd, check=True)
        for seg in segments: os.remove(seg)
        return final_path

    def generate(self, prompt, pillar_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{pillar_name}_{timestamp}_FULL.mp4"
        final_path = os.path.join(self.output_dir, final_filename)
        
        segments = []
        num_segments = 5 # 5 segments @ 8-9 seconds = ~45 seconds
        last_frame = None 
        
        print(f"--- 🎬 SkyReels: Generating 45s Narrative for {pillar_name} ---")

        try:
            for i in range(num_segments):
                print(f"--- Rendering Segment {i+1}/{num_segments} ---")
                
                # If we have a last_frame, we use it as the 'init_image' 
                # to keep the character and background consistent.
                kwargs = {}
                if last_frame is not None:
                    kwargs["image"] = last_frame # Continuity hook

                output = self.pipe(
                    prompt=prompt,
                    negative_prompt="low quality, flickering, jumping, distorted, text",
                    num_frames=121,      
                    height=960,          # Vertical Short Format
                    width=544,           
                    num_inference_steps=30, 
                    guidance_scale=4.5,
                    **kwargs
                ).frames[0] # frames[0] is a list of PIL images

                # Update last_frame with the absolute last image of this segment
                last_frame = output[-1] 

                seg_path = os.path.join(self.temp_dir, f"seg_{i}.mp4")
                export_to_video(output, seg_path, fps=24)
                segments.append(seg_path)

            print("--- 🧵 Joining SkyReels Segments ---")
            self._stitch_videos(segments, final_path)
            return final_path

        except Exception as e:
            print(f"--- ❌ SkyReels Worker Error: {e} ---")
            return None
