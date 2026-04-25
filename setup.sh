#!/bin/bash

echo "🚀 Setting up AI Video Factory..."

# system deps
sudo apt update && sudo apt install -y git ffmpeg

# python env
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# install ollama (optional)
curl -fsSL https://ollama.com/install.sh | sh

echo "✅ Setup complete!"
