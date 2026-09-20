import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Cargar la API key desde la raíz del proyecto (subiendo un nivel)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "⚠️ No se encontró la API Key de OpenAI. Revisa el archivo .env en la raíz."
    )
    st.stop()

client = OpenAI(api_key="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")

st.set_page_config(
    page_title="Asistente Ingeniería de Sistemas UTP", page_icon="💻"
)
st.title("💻 Chatbot Académico - Ingeniería de Sistemas UTP")
st.write(
    "Asistente virtual de texto para orientación en cursos, créditos y malla curricular."
)

if "messages_sistemas" not in st.session_state:
    st.session_state.messages_sistemas = [
        {
            "role": "system",
            "content": (
                "Eres un asistente académico experto en la carrera de Ingeniería"
                " de Sistemas e Informática de la UTP. Ayudas a los alumnos"
                " con dudas sobre su malla, programación y proyectos."
            ),
        }
    ]

for message in st.session_state.messages_sistemas:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input(
    "Pregunta sobre cursos, ciclos o metodologías (ej. ¿Qué cursos hay en el ciclo 5?)..."
):
    st.session_state.messages_sistemas.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando información académica..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages_sistemas,
                )
                respuesta = response.choices[0].message.content
                st.markdown(respuesta)
                st.session_state.messages_sistemas.append(
                    {"role": "assistant", "content": respuesta}
                )
            except Exception as e:
                st.error(f"Error: {e}")