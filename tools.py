import os
import requests
from agents import function_tool


def enviar_notificacao(texto):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": texto,
        },
    )


@function_tool
def registrar_dados_usuario(
    email: str, nome: str = "Nome não informado", observacoes: str = "não informado"
) -> str:
    """Use esta ferramenta para registrar que um usuário quer contato e informou um e-mail."""
    enviar_notificacao(
        f"Registrando interesse de {nome} com email {email} e observações {observacoes}"
    )
    return "OK"


@function_tool
def registrar_pergunta_desconhecida(pergunta: str) -> str:
    """Sempre use esta ferramenta para registrar perguntas que você não soube responder."""
    enviar_notificacao(f"Registrando pergunta sem resposta: {pergunta}")
    return "OK"


ferramentas = [
    registrar_dados_usuario,
    registrar_pergunta_desconhecida,
]
