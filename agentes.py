import os

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI

from context import PROMPT_SISTEMA_GEMEO
from tools import ferramentas

load_dotenv(override=True)
set_tracing_disabled(disabled=True)

URL_BASE_GEMINI = "https://generativelanguage.googleapis.com/v1beta/openai/"
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
