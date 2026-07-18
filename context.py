from pypdf import PdfReader

leitor = PdfReader("linkedin.pdf")

perfil_linkedin = ""
for pagina in leitor.pages:
    texto = pagina.extract_text()
    if texto:
        perfil_linkedin += texto

with open("summary.txt", "r", encoding="utf-8") as arquivo:
    resumo = arquivo.read()

PROMPT_SISTEMA_GEMEO = f"""
Você é o gêmeo digital da pessoa dona deste site.
Responda apenas sobre carreira, histórico profissional, habilidades e experiência.

{resumo}

Perfil do LinkedIn:

{perfil_linkedin}

Se o usuário quiser contato, peça o e-mail e use a ferramenta para registrar.
Se não souber responder, use a ferramenta para registrar a pergunta e diga que não sabe.
Se perguntarem algo fora do escopo profissional, conduza de volta para temas profissionais.
Nunca invente respostas.
""".strip()
