import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config_manager import config
from core.audio_engine import AudioEngine
from core.llm_engine import LLMEngine

if 'audio_engine' not in st.session_state:
    st.session_state.audio_engine = AudioEngine()
if 'llm_engine' not in st.session_state:
    st.session_state.llm_engine = LLMEngine()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="NLP Практикум", layout="wide")

with st.sidebar:
    st.header("Налаштування бота")

    config.input_mode = st.radio("Режим вводу", ["Text", "Voice"])
    config.output_mode = st.radio("Режим виводу", ["Text", "Voice"])

    st.subheader("Налаштування TTS")
    config.volume = st.slider("Гучність", 0.0, 1.0, 1.0)
    config.rate = st.slider("Швидкість мовлення", 50, 300, 150)

    voices = st.session_state.audio_engine.get_voices()
    voice_options = {voice.name: voice.id for voice in voices}
    selected_voice_name = st.selectbox("Голос", list(voice_options.keys()))
    config.voice_id = voice_options[selected_voice_name]

st.title("Діалогові програми (Echo & LLM)")

tab1, tab2, tab3 = st.tabs(["Echo-бот", "Вільний LLM Чат", "Q&A за контекстом"])

with tab1:
    st.header("Echo-бот")
    user_text = st.text_input("Введіть текст для Echo:")

    if st.button("Сказати голосом (Voice Input)", key="echo_mic") and config.input_mode == "Voice":
        user_text = st.session_state.audio_engine.listen()
        st.info(f"Розпізнано: {user_text}")

    if st.button("Надіслати", key="echo_send") and user_text:
        response = f"Ви сказали: {user_text}"
        st.success(response)
        if config.output_mode == "Voice":
            st.session_state.audio_engine.speak(response)

with tab2:
    st.header("Чат з LLM (Gemini)")
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    chat_input = st.chat_input("Напишіть повідомлення...")

    if chat_input:
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        st.chat_message("user").write(chat_input)

        response = st.session_state.llm_engine.generate_chat_response(chat_input)

        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

        if config.output_mode == "Voice":
            st.session_state.audio_engine.speak(response)

with tab3:
    st.header("Відповіді на питання за текстом (RAG)")

    context_text = st.text_area("Вставте текст (контекст):", height=200)
    qa_input = st.text_input("Ваше запитання до тексту:")

    if st.button("Запитати") and qa_input and context_text:
        with st.spinner("Модель аналізує текст..."):
            qa_response = st.session_state.llm_engine.generate_qa_response(qa_input, context_text)
            st.write(qa_response)
            if config.output_mode == "Voice":
                st.session_state.audio_engine.speak(qa_response)
