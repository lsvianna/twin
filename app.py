import asyncio
import os

import streamlit as st
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI

from context import PROMPT_SISTEMA_GEMEO
from tools import ferramentas

load_dotenv(override=True)
set_tracing_disabled(disabled=True)

URL_BASE_GEMINI = os.getenv("GEMINI_BASE_URL")
CHAVE_API_GEMINI = os.getenv("GEMINI_API_KEY")
NOME_MODELO = "gemini-3.5-flash"


async def conversar(mensagem, historico):
    if not URL_BASE_GEMINI or not CHAVE_API_GEMINI:
        return "Configure GEMINI_BASE_URL e GEMINI_API_KEY para conversar comigo."

    cliente_gemini = AsyncOpenAI(base_url=URL_BASE_GEMINI, api_key=CHAVE_API_GEMINI)
    modelo_gemini = OpenAIChatCompletionsModel(
        model=NOME_MODELO,
        openai_client=cliente_gemini,
    )
    agente = Agent(
        name="Gêmeo Digital",
        instructions=PROMPT_SISTEMA_GEMEO,
        model=modelo_gemini,
        tools=ferramentas,
    )
    entrada = historico + [{"role": "user", "content": mensagem}]
    resultado = await Runner.run(agente, entrada)
    return resultado.final_output


st.set_page_config(page_title="Gêmeo Digital", page_icon=":speech_balloon:")
st.title("Gêmeo Digital")
st.caption("Converse com meu gêmeo de IA sobre minha carreira")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for item in st.session_state.mensagens:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

mensagem_usuario = st.chat_input("Digite sua mensagem")
if mensagem_usuario:
    historico = st.session_state.mensagens.copy()
    st.session_state.mensagens.append({"role": "user", "content": mensagem_usuario})

    with st.chat_message("user"):
        st.markdown(mensagem_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = asyncio.run(conversar(mensagem_usuario, historico))
        st.markdown(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
