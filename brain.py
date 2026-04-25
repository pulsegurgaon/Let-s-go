import os
import json

class AI_Brain:
    def __init__(self):
        # Point this to your Rclone/Google Drive mount point
        # This way, history.json is SAVED on Google Drive, not the temporary GPU
        self.history_file = "/content/mydrive/AI_Videos/history.json" 

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return {}
    
    def _save_history(self, pillar_key, idea):
        # Same logic as before, but it writes directly to the Drive
        # Even if the GPU machine explodes, your history stays in the cloud.
