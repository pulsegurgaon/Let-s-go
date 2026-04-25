#!/bin/bash

# Exit on any error
set -e

echo "--- Starting OVH GPU Setup ---"

# 1. Update system and install Python essentials
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git

# 2. Create and activate a Virtual Environment
# This prevents conflicts with system packages
python3 -m venv venv
source venv/bin/activate

# 3. Install requirements
# This will look for your requirements.txt in the same folder
echo "--- Installing Python Libraries (This may take a few minutes) ---"
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create necessary folders
mkdir -p outputs

echo "--- SETUP COMPLETE ---"
echo "Follow these steps to start your studio:"
echo "1. Start Backend: source venv/bin/activate && uvicorn app:app --host 0.0.0.0 --port 8000"
echo "2. Open a new terminal tab."
echo "3. Start Frontend: source venv/bin/activate && streamlit run frontend.py --server.port 8501"
echo "------------------------------------------------"
