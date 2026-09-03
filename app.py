import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Speech & Anchor Coach", layout="centered")

st.title("🎙️ AI Broadcast & Speech Coach")
st.write("Paste your speech/news script, record your voice, and get an instant review.")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

script_text = st.text_area("1. Paste your speech script here:", height=150)
audio_data = st.audio_input("2. Record your speech")

if st.button("Analyze Speech", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not script_text.strip():
        st.error("Please enter your speech script first.")
    elif not audio_data:
        st.error("Please record your speech before submitting.")
    else:
        with st.spinner("Analyzing your delivery, pace, and diction..."):
            try:
                client = genai.Client(api_key=api_key)
                
                audio_bytes = audio_data.read()
                mime_type = audio_data.type if hasattr(audio_data, "type") else "audio/wav"

                prompt = f"""
You are an expert broadcast journalism coach evaluating a media student.

ORIGINAL SCRIPT:
\"\"\"{script_text}\"\"\"

TASK:
Listen to the audio recording and provide an evaluation:
1. Script Fidelity (words missed, added, or misread).
2. Broadcast Pacing (speed, rhythm, breathing).
3. Filler Words (um, ah, like, nervous repetitions).
4. Tone, Intonation & Expression (headline emphasis, authority).
5. 2-3 Actionable Tips for the next practice take.
"""

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
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

            except Exception as e:
                st.error(f"Error processing audio: {e}")
