import os
import json
from groq import Groq
from dotenv import load_dotenv
from config import PILLAR_CONFIG

load_dotenv()

class AI_Brain:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.history_file = "history.json"

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def _save_history(self, idea):
        history = self._load_history()
        history.append(idea)
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=4)

    def generate_detailed_prompt(self, pillar_key, seed_idea):
        pillar = PILLAR_CONFIG.get(pillar_key)
        history = self._load_history()
        
        # The System Instruction: This forces the 500-word technical depth
        system_msg = f"""
        You are a Technical Cinematographer and Senior AI Prompt Engineer for LTX-Video.
        Your goal is to generate an EXTREMELY DETAILED (minimum 500 words) video generation prompt.
        
        STRICT FORMATTING RULES:
        1. CHARACTER DNA: Describe the subject using: {pillar['character']}
        2. CAMERA: Use specific lens kits and movements: {pillar['camera']}
        3. LIGHTING: Describe ray-tracing, global illumination, rim lights, and light temperatures.
        4. TEXTURES: Describe PBR materials, subsurface scattering, and micro-details.
        5. STORY LOGIC: Follow the {pillar['logic']} structure.
        
        REFERENCE EXAMPLES FOR STYLE:
        {json.dumps(pillar['prompt_examples'], indent=2)}

        Avoid repeating these previous themes: {history[-10:]}
        
        The output must be one continuous, highly descriptive paragraph designed for a video diffusion model. 
        Focus on the physical reality of the scene.
        """

        user_msg = f"Generate a master-level video prompt based on this seed idea: {seed_idea}"

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            
            full_prompt = chat_completion.choices[0].message.content
            self._save_history(seed_idea)
            return full_prompt

        except Exception as e:
            return f"Error connecting to Groq: {e}"

# Test usage
if __name__ == "__main__":
    brain = AI_Brain()
    # Example: Desert survival story
    result = brain.generate_detailed_prompt("survival", "What if you had to survive 24 hours on only Redbull")
    print(result)
