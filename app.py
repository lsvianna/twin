import asyncio
import streamlit as st
from agent import conversar

# Configuração da página
st.set_page_config(page_title='Leonardo Vianna', page_icon=':speech_balloon:')
st.title('Leonardo Vianna')
st.caption('Converse com meu gêmeo digital sobre minha carreira')

# Inicializa o histórico de mensagens se não existir
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []

# Exibe o histórico de mensagens
for item in st.session_state.mensagens:
    # Exibe cada mensagem no chat
    with st.chat_message(item['role']):
        st.markdown(item['content'])

# Entrada do usuário
mensagem_usuario = st.chat_input('Digite sua mensagem')
# Se o usuário enviar uma mensagem, processa a entrada
if mensagem_usuario:
    # Copia o histórico de mensagens antes de adicionar a nova mensagem do usuário
    historico = st.session_state.mensagens.copy()
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.mensagens.append({'role': 'user', 'content': mensagem_usuario})

    # Exibe a mensagem do usuário no chat
    with st.chat_message('user'):
        st.markdown(mensagem_usuario)

    # Processa a resposta do agente e exibe no chat
    with st.chat_message('assistant'):
        # Mostra um spinner enquanto o agente está "pensando"
        with st.spinner('Pensando...'):
            # Chama a função conversar para obter a resposta do agente
            resposta = asyncio.run(conversar(mensagem_usuario, historico))
        # Exibe a resposta do agente no chat
        st.markdown(resposta)

    # Adiciona a resposta do agente ao histórico de mensagens
    st.session_state.mensagens.append({'role': 'assistant', 'content': resposta})
