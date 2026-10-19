import os
import json
import re
from google import genai
from google.genai import types

# Configuração do cliente Gemini
client = genai.Client()

def limpar_comentario(texto):
    """
    Função para remover padrões visuais de metadados do Instagram 
    (ex: '79 sem2 curtidasResponder', '1 semResponder', etc.)
    """
    # Remove o padrão de tempo, curtidas e botão responder no final do texto
    texto_limpo = re.sub(r'\d+\s*sem(?:\d+\s*curtidas)?Responder', '', texto)
    # Remove quebras de linha e espaços duplos
    texto_limpo = texto_limpo.strip()
    return texto_limpo

def analisar_comentarios_instagram(comentarios):
    # Aplica a limpeza em cada comentário e remove linhas vazias
    comentarios_limpos = [
        limpar_comentario(c) for c in comentarios if limpar_comentario(c)
    ]

    prompt = f"""
    Você é um Analista de Comportamento e Estrategista de Comunidades com foco em projetos filosóficos e sociais.
    Analise a lista de comentários abaixo extraídos do Instagram da Pequena Tribo.
    Retorne estritamente um JSON contendo:
    1. 'distribuicao_intencao' (percentual ou estimativa entre: 'Elogio Passivo', 'Conexão Filosófica' e 'Intenção Ativa')
    2. 'tons_predominantes' (lista com os tons emocionais/filosóficos mais fortes encontrados, ex: Devocional/Gratidão, Acolhimento, Inspiração)
    3. 'nivel_profundidade' (análise se os comentários foram majoritariamente superficiais/emojis ou elaborados/reflexivos)
    4. 'insights_para_equipe' (uma frase estratégica avaliando o termômetro e orientando a equipe)
    
    Comentários: {json.dumps(comentarios_limpos, ensure_ascii=False)}
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    return response.text

# Dados brutos copiados do Instagram
comentarios_brutos = [
    "Um projeto do coração. ❤️79 sem2 curtidasResponder",
    "Que Isvara continue abençoando este belíssimo projeto🙌que as crianças bem direcionadas no hoje, sejam adultos inteiros e fraternos no amanhã 🙌❤️79 sem2 curtidasResponder",
    "Muito lindo esse projeto, dando uma educação saudável para essas crianças 🙌🙌❤️79 sem2 curtidasResponder",
    "Que lindeza! 🙏🏻🌷🧘🏻‍♀️79 sem2 curtidasResponder",
    "Um trabalho lindo de ver.🙏🏽79 sem2 curtidasResponder",
    "Projeto maravilhoso, que continue crescendo e ajudando muitas crianças ❤️79 sem2 curtidasResponder",
    "Esse projeto é uma linda manifestação de amor e dedicação!💖79 sem2 curtidasResponder",
    "Um projeto que olha as crianças de um jeito diferente. O respeito é a base para estas crianças irem para o mundo.79 sem2 curtidasResponder"
]

if __name__ == "__main__":
    print("Analisando intenções, tons e profundidade da comunidade...")
    resultado = analisar_comentarios_instagram(comentarios_brutos)
    print("\n--- Relatório Estratégico da Comunidade ---")
    print(resultado)

    # Salva o relatório formatado em um arquivo local
    with open("Relatorio_Pequena_Tribo.md", "w", encoding="utf-8") as f:
        f.write(resultado)
    print("\nArquivo 'Relatorio_Pequena_Tribo.md' gerado com sucesso!")