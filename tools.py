from agents import function_tool

enviar_email = None


def configurar_envio_email(funcao):
    global enviar_email
    enviar_email = funcao


@function_tool
def registrar_dados_usuario(
    email: str, nome: str = "Nome não informado", observacoes: str = "não informado"
) -> str:
    """Use esta ferramenta para registrar que um usuário quer contato e informou um e-mail."""
    enviar_email(
        "Novo contato pelo gêmeo digital",
        f"Nome: {nome}\nEmail: {email}\nObservações: {observacoes}",
    )
    return "OK"


@function_tool
def registrar_pergunta_desconhecida(pergunta: str) -> str:
    """Sempre use esta ferramenta para registrar perguntas que você não soube responder."""
    enviar_email("Pergunta sem resposta", pergunta)
    return "OK"


ferramentas = [
    registrar_dados_usuario,
    registrar_pergunta_desconhecida,
]
