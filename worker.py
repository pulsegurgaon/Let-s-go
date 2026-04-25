import torch
import os
import subprocess
from diffusers import LTXVideoPipeline
from diffusers.utils import export_to_video
from gtts import gTTS
from config import OUTPUT_DIR

class VideoWorker:
    def __init__(self):
        self.device = "cuda"
        # Using Distilled for T4 speed
        self.pipe = LTXVideoPipeline.from_pretrained(
            "Lightricks/LTX-Video", 
            torch_dtype=torch.bfloat16
        ).to(self.device)
        self.pipe.enable_model_cpu_offload()

    def generate_voiceover(self, script, pillar):
        voice_path = "temp_voice.mp3"
        tts = gTTS(text=script, lang='en')
        tts.save(voice_path)
        return voice_path

    def generate_video(self, visual_prompt, pillar):
        segments = []
        last_frame = None
        
        # 8 chunks of ~5.5 seconds = ~45 seconds
        for i in range(8):
            print(f"--- Scene {i+1}/8 ---")
            
            # Continuity trick: use last frame of prev clip as start of next
            kwargs = {"image": last_frame} if last_frame is not None else {}
            
            frames = self.pipe(
                prompt=visual_prompt,
                num_frames=121, 
                num_inference_steps=12, # Distilled speed
                **kwargs
            ).frames[0]
            
            seg_path = f"seg_{i}.mp4"
            export_to_video(frames, seg_path)
            segments.append(seg_path)
            last_frame = frames[-1] # Save last frame for next chunk

        return segments

    def stitch_and_finalize(self, segments, voice_path, pillar):
        final_path = os.path.join(OUTPUT_DIR, f"{pillar}_{os.urandom(4).hex()}.mp4")
        list_file = "list.txt"
        with open(list_file, "w") as f:
            for s in segments: f.write(f"file '{os.path.abspath(s)}'\n")

        # FFmpeg: Combine clips + Add Voiceover + Loop audio if needed
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_file,
            "-i", voice_path, "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", final_path
        ]
        subprocess.run(cmd)
        
        # Cleanup
        for s in segments: os.remove(s)
        os.remove(voice_path)
        return final_path
