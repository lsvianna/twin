import asyncio
import os
import smtplib
from email.message import EmailMessage

import streamlit as st

from tools import configurar_envio_email


def enviar_email(assunto, conteudo):
    mensagem = EmailMessage()
    mensagem["From"] = os.getenv("GMAIL_EMAIL")
    mensagem["To"] = os.getenv("GMAIL_EMAIL", os.getenv("GMAIL_EMAIL"))
    mensagem["Subject"] = assunto
    mensagem.set_content(conteudo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(os.getenv("GMAIL_EMAIL"), os.getenv("GMAIL_SENHA"))
        servidor.send_message(mensagem)


configurar_envio_email(enviar_email)

from agentes import conversar


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
