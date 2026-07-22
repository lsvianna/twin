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

api_server = {
    'gemini': {
        'base_url': 'https://generativelanguage.googleapis.com/v1beta/openai/',
        'api_key': os.getenv('GEMINI_API_KEY'),
        'modelo': 'gemini-3.5-flash'
    },
    'openai': {
        'base_url': 'https://api.openai.com/v1/',
        'api_key': os.getenv('OPENAI_API_KEY'),
        'modelo': 'gpt-5.4-mini'
    },
    'mooshoot': {
        'base_url': 'https://api.mooshoot.com/v1/',
        'api_key': os.getenv('MOOSHOT_API_KEY'),
        'modelo': 'mooshoot-1.0.0'
    }
}

api_service = os.getenv('API_SERVICE', 'gemini')
config = api_server.get(api_service)

cliente = AsyncOpenAI(base_url=config['base_url'], api_key=config['api_key'])
modelo = OpenAIChatCompletionsModel(
    model=config['modelo'],
    openai_client=cliente,
)

agente = Agent(
    name="gemeo_digital",
    instructions=PROMPT_SISTEMA_GEMEO,
    model=modelo,
    tools=[envia_email]
)


async def conversar(mensagem, historico):
    entrada = historico + [{'role': 'user', 'content': mensagem}]
    resultado = await Runner.run(agente, entrada)
    return resultado.final_output
