# Confused Student Simulation Bot

This project implements a conversational agent that mimics a **confused yet intelligent student** reacting to lecture material. It accepts **text, PDFs, uploaded videos, or YouTube links** and generates naive or follow-up questions using **LLMs** via the **Gemini API**. The goal is to simulate conceptual misunderstandings and identify gaps in lecture clarity using **transformer-based language models**.

---

## Project Overview

This tool is designed to assist **instructors, TAs, and learners** by simulating how a student might misinterpret or struggle with a concept. It uses **large language models (LLMs)** and **automatic speech recognition (ASR)** to process diverse input formats (text, PDFs, audio from video), and engages in a five-turn back-and-forth question-answer loop with the user.

The agent builds context with each response and generates follow-up questions based on prior conversation history.

---

## Supported Input Types

* Pasted lecture **text**
* Uploaded **PDFs**
* Uploaded **video files (.mp4)**
* **YouTube video links** (auto-captions)

The app converts any of the above into plain text for LLM consumption.

---

## Core Technologies

* **Gemini API** (via `generateContent` endpoint): Generates confused student questions using Google's LLM
* **Hugging Face `transformers`**: Handles automatic speech recognition for uploaded videos using Whisper
* **Whisper (ASR)**: Transcribes audio to text using the open-source `openai/whisper-base` model
* **YouTube Transcript API**: Fetches captions for public videos with English subtitles
* **Streamlit**: Provides a conversational chat-like user interface

---

## App Behavior

* Parses and aggregates all uploaded or linked input into clean text
* Sends the text to Gemini API to generate a **"confused student question"**
* Displays conversation using **`st.chat_message()`** blocks (user/assistant roles)
* Accepts user answers and generates **up to 5 rounds of follow-up questions**

---

## File Structure

* `app.py`: Main Streamlit app
* `README.md`: This file
* `requirements.txt`: Dependencies for environment setup
* `ffmpeg/` (optional): Folder containing `ffmpeg` binaries (if manually included)

---

## How to Run

1. Install required packages:

```bash
pip install streamlit transformers torchaudio PyPDF2 youtube-transcript-api
```

2. Run the app:

```bash
streamlit run app.py
```

3. Provide your **Gemini API key** in the code or via Streamlit secrets.

---

## FFmpeg Installation (Required for ASR)

Video uploads require `ffmpeg` to convert and process audio for transcription.

### Windows:

1. Download the latest Windows build from:
   [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

2. Extract it to a location like:

   ```
   C:\ffmpeg
   ```

3. Add the `bin` folder to your system PATH:

   ```
   C:\ffmpeg\bin
   ```

4. Restart your terminal and confirm with:

   ```bash
   ffmpeg -version
   ```

### Linux:

```bash
sudo apt install ffmpeg
```

### macOS:

```bash
brew install ffmpeg
```

---

## Example Use Cases

| Scenario                              | What Happens                            |
| ------------------------------------- | --------------------------------------- |
| Upload lecture slides (PDF)           | Bot asks naive clarifying questions     |
| Paste complex text (e.g., ML intro)   | Bot misinterprets and asks follow-ups   |
| Upload recorded lecture (MP4)         | Bot transcribes and engages in dialogue |
| Link to a YouTube video with captions | Bot extracts captions and begins Q\&A   |

---

## Model Summary

| Task                | Model                                     |
| ------------------- | ----------------------------------------- |
| Language generation | `gemini-2.0-flash` via Gemini API         |
| ASR transcription   | `openai/whisper-base` from Hugging Face   |
| Chat interface      | Streamlit's `chat_input` + `chat_message` |

---

## Applications
* Lecture Testing: Identify confusing parts of lecture material before presenting.
* Tutoring Support: Generate common student questions for TA prep or FAQs.
* Self-Study Tool: Help students reflect on their understanding by simulating confusion.
* Educational QA: Screen textbooks, slides, or videos for potential misunderstandings.
* Research on LLM Dialogue: Study how models simulate learning gaps and follow-up questioning.
* Content Creation Aid: Improve clarity in MOOCs, YouTube videos, or blogs by previewing confusion.

## Potential Enhancements

* Adjustable confusion level: "mild", "medium", "deep"
* Visual transcript editor before starting the Q\&A
* Export conversations to `.json` or `.txt`
* LangChain agent memory for long conversations

