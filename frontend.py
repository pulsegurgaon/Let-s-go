import streamlit as st
import requests
import os
import time

# --- Page Config ---
st.set_page_config(page_title="AI Video Production Studio", layout="wide")

# --- Sidebar: Security & Setup ---
st.sidebar.title("🔐 Access Control")
groq_key = st.sidebar.text_input("Enter Groq API Key", type="password")
backend_url = st.sidebar.text_input("Backend URL", value="http://localhost:8000")

if not groq_key:
    st.warning("Please enter your Groq API Key in the sidebar to continue.")
    st.stop()

# Save the key to a temporary environment variable for the backend to read
os.environ["GROQ_API_KEY"] = groq_key

# --- Main UI ---
st.title("🎥 AI Video Production Engine")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("🚀 Generate New Content")
    
    pillar = st.selectbox("Select Content Pillar", [
        "survival", "dog_talk", "dog_rescue", "satisfying", "restoration", "what_if", "house"
    ])
    
    seed_idea = st.text_area("Enter Seed Idea", placeholder="e.g., Survive 24 hours in a desert with only Redbull")
    
    if st.button("Generate Video"):
        if seed_idea:
            with st.spinner("Brain is thinking and GPU is rendering..."):
                payload = {"pillar": pillar, "seed_idea": seed_idea}
                try:
                    response = requests.post(f"{backend_url}/generate", json=payload)
                    if response.status_code == 200:
                        st.success("Task queued! Check the gallery in a few minutes.")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to Backend: {e}")
        else:
            st.warning("Please enter a seed idea.")

with col2:
    st.header("📦 Video Gallery")
    output_path = "./outputs"
    
    if os.path.exists(output_path):
        video_files = [f for f in os.listdir(output_path) if f.endswith('.mp4')]
        video_files.sort(reverse=True) # Show newest first
        
        if video_files:
            selected_video = st.selectbox("Select a video to preview", video_files)
            video_file = open(os.path.join(output_path, selected_video), 'rb')
            st.video(video_file)
        else:
            st.info("No videos generated yet.")
    else:
        st.info("Output directory not found. Start generating!")

# --- Auto-Refresh Logic ---
st.sidebar.markdown("---")
if st.sidebar.button("Refresh Gallery"):
    st.rerun()
