import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "⚠️ No se encontró la API Key de OpenAI. Revisa el archivo .env en la raíz."
    )
    st.stop()

client = OpenAI(api_key="A)

st.set_page_config(page_title="Transcripción Whisper UTP", page_icon="🎙️")
st.title("🎙️ Procesamiento de Audio y Voz con Whisper")
st.write(
    "Sube una nota de voz con una consulta técnica para que sea transcrita y"
    " respondida automáticamente."
)

audio_file = st.file_uploader(
    "Sube un archivo de audio (mp3, wav, m4a)",
    type=["mp3", "wav", "m4a", "ogg"],
)

if audio_file is not None:
    st.audio(audio_file)

    if st.button("Procesar Audio con Whisper"):
        with st.spinner("Transcribiendo audio y generando respuesta..."):
            temp_path = "temp_audio.mp3"
            with open(temp_path, "wb") as f:
                f.write(audio_file.getbuffer())

            try:
                with open(temp_path, "rb") as audio:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", file=audio
                    )
                texto_voz = transcript.text

                if os.path.exists(temp_path):
                    os.remove(temp_path)

                st.success("¡Transcripción exitosa!")
                st.markdown(f"**Texto detectado por Whisper:**")
                st.info(texto_voz)

                # Respuesta de la IA basada en la transcripción
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Eres un asistente técnico respondiendo a una"
                                " consulta de voz."
                            ),
                        },
                        {"role": "user", "content": texto_voz},
                    ],
                )
                st.markdown("### 🤖 Respuesta del Asistente:")
                st.write(response.choices[0].message.content)

            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)