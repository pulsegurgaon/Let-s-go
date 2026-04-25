import json
import os
from config import HISTORY_PATH, PILLARS

class AI_Brain:
    def __init__(self):
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, "r") as f:
                return json.load(f)
        return {k: [] for k in PILLARS.keys()}

    def save_to_history(self, pillar, idea):
        self.history[pillar].append(idea)
        with open(HISTORY_PATH, "w") as f:
            json.dump(self.history, f, indent=4)

    def get_next_idea(self, pillar, groq_client):
        past_ideas = ", ".join(self.history.get(pillar, []))
        prompt = f"Generate a unique 45-second script for a {pillar} video. Avoid: {past_ideas}. Return only the script and a short visual prompt."
        
        # Call Groq here (Standard implementation)
        # return script, visual_prompt
