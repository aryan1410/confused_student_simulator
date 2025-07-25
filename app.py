import streamlit as st
import tempfile
import os
import requests
import json
from PyPDF2 import PdfReader
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

load_dotenv()
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'awaiting_follow_up' not in st.session_state:
    st.session_state.awaiting_follow_up = False

st.title("Confused Student Simulation Bot")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_video(uploaded_file):
    asr = pipeline("automatic-speech-recognition", model="openai/whisper-base")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp.flush()
        result = asr(tmp.name, return_timestamps=True)
    return result["text"]


def extract_text_from_youtube(url):
    video_id = url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return " ".join([entry['text'] for entry in transcript])

def generate_confused_question(text, history):
    history_prompt = "\n".join([f"Q: {q}\nA: {a}" for q, a in history])
    prompt = f'''You are a confused student trying to understand the following content. Generate an intellectual question that expresses misunderstanding or confusion
    that would be raised by a uniquely talented student. But make sure it sounds like a student talking, no need for unnecessary complex words or phrases. It should 
    sound like a natural, casual conversation and not an AI bot speaking. Ask good questions in a simple manner. Feel free to use the following conversation history (if any), in case you want to generate a follow 
    up based on that. If the answer was not up to the standards of clarity, you can also repeat a question from the history.\nConversation history:\n{history_prompt}\nContent:\n{text}\nQ:'''
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
        headers=headers,
        data=json.dumps(payload)
    )
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

st.subheader("Step 1: Provide lecture material (any or all supported)")
text_input = st.text_area("Paste lecture content (optional):")
pdf_file = st.file_uploader("Upload a PDF (optional):", type=["pdf"])
video_file = st.file_uploader("Upload video file (optional):", type=["mp4"])
yt_link = st.text_input("YouTube video link (optional):")

text = text_input.strip()
if pdf_file:
    text += "\n" + extract_text_from_pdf(pdf_file)
if video_file:
    text += "\n" + extract_text_from_video(video_file)
if yt_link:
    try:
        text += "\n" + extract_text_from_youtube(yt_link)
    except:
        st.error("This video doesn't seem to have captions. Please try another video or upload the file manually")

if text:
    st.success("Lecture text loaded.")

    if st.session_state.turn == 0:
        if st.button("🧠 Generate initial confused question"):
            with st.spinner("Thinking..."):
                q = generate_confused_question(text, [])
                st.session_state.conversation.append((q, ""))
                st.session_state.turn += 1

    # Display chat
    for i, (q, a) in enumerate(st.session_state.conversation):
        with st.chat_message("assistant"):
            st.markdown(f"**Q{i+1}:** {q}")
        if a:
            with st.chat_message("user"):
                st.markdown(a)

    if st.session_state.conversation and st.session_state.conversation[-1][1] == "":
        user_input = st.chat_input("Your answer:")
        if user_input:
            st.session_state.conversation[-1] = (
                st.session_state.conversation[-1][0],
                user_input
            )
            st.session_state.awaiting_follow_up = True
            st.rerun()

    if st.session_state.awaiting_follow_up and st.session_state.turn < 5:
        with st.spinner("Thinking..."):
            follow_up = generate_confused_question(text, st.session_state.conversation)
            st.session_state.conversation.append((follow_up, ""))
            st.session_state.turn += 1
            st.session_state.awaiting_follow_up = False
            st.rerun()

