import asyncio
import streamlit as st
from agentes import conversar

st.set_page_config(page_title="Leonardo Vianna", page_icon=":speech_balloon:")
st.title("Leonardo Vianna")
st.caption("Converse com meu gêmeo digital sobre minha carreira")

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
