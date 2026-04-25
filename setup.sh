#!/bin/bash
set -e

echo "--- 🚀 Starting High-Speed OVH GPU Setup ---"

# 1. System Updates
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git rclone

# 2. Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Requirements
pip install --upgrade pip
pip install -r requirements.txt

# 4. Pre-download LTX-Video Weights (Saves time later)
# This uses huggingface-cli to grab the model before you start
pip install huggingface_hub
python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Lightricks/LTX-Video')"

# 5. Create Folders
mkdir -p outputs

echo "--- ✅ SETUP COMPLETE ---"
echo "To link Google Drive, run: rclone config"
echo "Then start the apps as instructed before."
