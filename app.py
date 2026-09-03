import streamlit as st
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="Speech & Anchor Coach", layout="centered")

st.title("🎙️ AI Broadcast & Speech Coach")
st.write("Paste your speech/news script, record your voice, and get an instant review.")

# Apni working AIzaSy... key yahan rehne do
API_KEY = "AIzaSyBlFzZoxji486Z8_3RQu5EMx6rfqEzzIgA" 

script_text = st.text_area("1. Paste your speech script here:", height=150)
audio_data = st.audio_input("2. Record your speech")

# List of models to fallback automatically if one is overloaded (503)
MODELS_TO_TRY = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']

if st.button("Analyze Speech", type="primary"):
    if not script_text.strip():
        st.error("Please enter your speech script first.")
    elif not audio_data:
        st.error("Please record your speech before submitting.")
    else:
        with st.spinner("Analyzing your delivery, pace, and diction..."):
            client = genai.Client(api_key=API_KEY)
            audio_bytes = audio_data.read()
            mime_type = audio_data.type if hasattr(audio_data, "type") else "audio/wav"

            prompt = f"""
You are an expert broadcast journalism coach evaluating a mass communication student.

ORIGINAL SCRIPT:
\"\"\"{script_text}\"\"\"

TASK:
Listen to the audio recording and provide a clear, professional evaluation report:
1. **Script Fidelity**: Transcribe what was spoken and flag any missed sentences, added words, or mispronounced facts.
2. **Broadcast Pacing**: Evaluate speaking speed (target benchmark: 130-150 WPM), sentence rhythm, and breathing pauses.
3. **Filler Words**: Highlight crutch words like 'um', 'ah', 'like', throat clears, or nervous repetitions.
4. **Tone & Intonation**: Check if headlines and key terms had proper emphasis, authority, and vocal energy.
5. **Actionable Tips**: Give 2-3 specific points to improve on the next take.
"""

            response_success = False
            last_error = ""

            for model_name in MODELS_TO_TRY:
                for attempt in range(2):  # 2 retries per model
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=[
                                prompt,
                                types.Part.from_bytes(
                                    data=audio_bytes,
                                    mime_type=mime_type,
                                )
                            ]
                        )
                        st.success("Analysis complete!")
                        st.markdown(response.text)
                        response_success = True
                        break
                    except Exception as e:
                        last_error = str(e)
                        time.sleep(2)  # Wait 2 seconds before retrying
                if response_success:
                    break

            if not response_success:
                st.error(f"Google servers are currently overloaded. Please try clicking Analyze again in a few seconds. Details: {last_error}")
