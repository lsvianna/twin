from tool import send_email

import os
from pypdf import PdfReader
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled, trace
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)
set_tracing_disabled(True)

@function_tool
def envia_email(email: str, nome: str, notas: str) -> str:
    """
    Registre que um usuário tem interesse em manter contato e forneceu um endereço de e-mail.

    Argumentos:
        email: O endereço de e-mail informado pelo usuário
        nome: O nome do usuário
        notas: Informações adicionais sobre o contato
    """
    assunto = "Novo contato pelo gêmeo digital"
    texto = f'Nome: {nome}\nEmail: {email}\nNotas: {notas}'
    send_email(assunto, texto)
    return 'Email enviado com sucesso!'


perfil_linkedin = ''
for pagina in PdfReader('linkedin.pdf').pages:
    texto = pagina.extract_text()
    if texto:
        perfil_linkedin += texto

perfil_lattes = ''
for pagina in PdfReader('lattes.pdf').pages:
    texto = pagina.extract_text()
    if texto:
        perfil_lattes += texto

PROMPT_SISTEMA_GEMEO = f"""
Você é o gêmeo digital da pessoa dona deste site.
Responda apenas sobre carreira, histórico profissional, habilidades e experiência.

Perfil do LinkedIn:

{perfil_linkedin}

Perfil do Lattes:

{perfil_lattes}

Se o usuário quiser contato, peça o e-mail e use a ferramenta para registrar.
Se não souber responder, use a ferramenta para registrar a pergunta e diga que não sabe.
Se perguntarem algo fora do escopo profissional, conduza de volta para temas profissionais.
Nunca invente respostas. Seja direto, objetivo e educado. Se não souber, diga que não sabe.
Não forneça informações pessoais, como endereço ou telefone. Não produza respostas longas.
"""

URL_BASE_GEMINI = 'https://generativelanguage.googleapis.com/v1beta/openai/'
CHAVE_API_GEMINI = os.getenv('GEMINI_API_KEY')
NOME_MODELO = 'gemini-3.5-flash'

cliente_gemini = AsyncOpenAI(base_url=URL_BASE_GEMINI, api_key=CHAVE_API_GEMINI)
modelo_gemini = OpenAIChatCompletionsModel(
    model=NOME_MODELO,
    openai_client=cliente_gemini,
)
agente = Agent(
    name="gemeo_digital",
    instructions=PROMPT_SISTEMA_GEMEO,
    model=modelo_gemini,
    tools=[envia_email]
)


async def conversar(mensagem, historico):
    entrada = historico + [{'role': 'user', 'content': mensagem}]
    resultado = await Runner.run(agente, entrada)
    return resultado.final_output
