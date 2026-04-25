import os
import json
from groq import Groq
from config import PILLAR_CONFIG

class AI_Brain:
    def __init__(self):
        # We initialize without a key; it will be set per-request from the UI
        self.client = None
        self.history_file = "history.json"

    def _load_history(self):
        """Loads the history of seed ideas to prevent repetition."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_history(self, pillar_key, idea):
        """Saves the latest idea to the specific pillar in history.json."""
        history = self._load_history()
        if pillar_key not in history:
            history[pillar_key] = []
        
        history[pillar_key].append(idea)
        
        # Keep only the last 20 ideas to save space
        history[pillar_key] = history[pillar_key][-20:]
        
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=4)

    def generate_detailed_prompt(self, pillar_key, seed_idea, user_key):
        """
        Connects to Groq using the key provided from the Frontend
        and expands the seed idea into a 500+ word technical prompt.
        """
        # 1. Setup the Groq Client with the temporary key
        try:
            self.client = Groq(api_key=user_key)
        except Exception as e:
            return f"Error: Invalid Groq Key provided. {str(e)}"

        # 2. Get Pillar Data from Config
        pillar = PILLAR_CONFIG.get(pillar_key)
        if not pillar:
            return "Error: Pillar not found in config."

        # 3. Get History for this pillar to avoid repeats
        full_history = self._load_history()
        pillar_history = full_history.get(pillar_key, [])

        # 4. Construct the Master System Instruction
        system_msg = f"""
        You are a Senior AI Cinematographer and Prompt Engineer for LTX-Video.
        Your task is to write an EXTREMELY DETAILED technical video prompt (Minimum 500 words).
        
        CHARACTER DNA: {pillar['character']}
        CAMERA SYSTEM: {pillar['camera']}
        STORY LOGIC: {pillar['logic']}
        
        TECHNICAL REQUIREMENTS:
        - Use cinematic language (e.g., Fresnel reflections, subsurface scattering, focal length).
        - Describe the environment, lighting temperatures (in Kelvin), and texture maps.
        - The prompt must cover a 24-hour arc (Start, Struggle, Resolution).
        - Do NOT include any introductory text like 'Here is your prompt'. 
        - Provide ONLY the descriptive prompt block.

        REFERENCE EXAMPLES:
        {json.dumps(pillar['prompt_examples'], indent=2)}

        PREVIOUS IDEAS (DO NOT REPEAT): {pillar_history}
        """

        user_msg = f"Seed Idea for {pillar_key}: {seed_idea}"

        try:
            # 5. Call Groq
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.75, # Slight randomness for creativity
                max_tokens=2048   # Enough room for 500+ words
            )
            
            final_prompt = chat_completion.choices[0].message.content
            
            # 6. Save this success to history
            self._save_history(pillar_key, seed_idea)
            
            return final_prompt

        except Exception as e:
            return f"Error: Groq API failed. Details: {str(e)}"

# Self-test block (only runs if you run this file directly)
if __name__ == "__main__":
    print("AI Brain initialized. Waiting for requests from App.py...")
