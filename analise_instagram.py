import os
import json
import re
from google import genai
from google.genai import types

# Configuração do cliente Gemini
client = genai.Client()

def limpar_comentarios_instagram(texto_bruto):
    """
    Pipeline de Regex para higienizar dados brutos ou exportações web,
    removendo ruídos de interface e metadados do Instagram.
    """
    padroes_ruido = r"(Responder|Ver respostas.*|há \d+ [dhsm]|Curtir|\d+ curtidas)"
    
    linhas = texto_bruto.strip().split("\n")
    comentarios_limpos = []
    
    for linha in linhas:
        linha_limpa = re.sub(padroes_ruido, "", linha).strip()
        if len(linha_limpa) > 3:  
            comentarios_limpos.append(linha_limpa)
            
    return comentarios_limpos

def analisar_post_com_link(url_post, comentarios_limpos):
    """
    Envia o link do post e a lista tratada para o modelo Gemini estruturar 
    o relatório gerencial em JSON, preservando a origem da URL.
    """
    prompt = f"""
    Você é um Analista de Comportamento e Estrategista de Comunidades com foco em projetos sociais e filosóficos (Seva / Vedanta).
    Analise a lista de comentários abaixo extraídos da postagem da Pequena Tribo através do link: {url_post}
    
    Retorne estritamente um JSON contendo:
    1. 'url_analisada' (o link do post fornecido)
    2. 'distribuicao_intencao' (percentual ou estimativa entre: 'Elogio Passivo', 'Conexão Filosófica' e 'Intenção Ativa')
    3. 'tons_predominantes' (lista com os tons emocionais/filosóficos mais fortes encontrados)
    4. 'nivel_profundidade' (análise se os comentários foram majoritariamente superficiais ou reflexivos)
    5. 'insights_para_equipe' (uma frase estratégica avaliando o termômetro e orientando a equipe)
    
    Comentários do post: {json.dumps(comentarios_limpos, ensure_ascii=False)}
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    return response.text

def salvar_relatorio_markdown(resultado_json, nome_arquivo="Relatorio_Pequena_Tribo.md"):
    """
    Salva o resultado da IA automaticamente em um arquivo Markdown (.md) estruturado.
    """
    conteudo_md = f"# Relatório Executivo - Pequena Tribo (Seva)\n\n```json\n{resultado_json}\n```"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_md)
    print(f"\nArquivo '{nome_arquivo}' gerado e salvo com sucesso!")

if __name__ == "__main__":
    # URL do post que serve como referência e rastreabilidade para a análise
    url_alvo = "https://www.instagram.com/p/exemplo_pequena_tribo/"
    
    # Bloco bruto de comentários coletados do post correspondente à URL
    bloco_brutos = """
    Um projeto do coração. ❤️79 sem2 curtidasResponder
    Que Isvara continue abençoando este belíssimo projeto🙌que as crianças bem direcionadas no hoje, sejam adultos inteiros e fraternos no amanhã 🙌❤️79 sem2 curtidasResponder
    """
    
    print(f"1. Processando link da postagem: {url_alvo}")
    comentarios_tratados = limpar_comentarios_instagram(bloco_brutos)
    
    print("2. Executando pipeline de limpeza e análise com Gemini (2.5-flash)...")
    resultado = analisar_post_com_link(url_alvo, comentarios_tratados)
    
    print("\n--- Relatório Estratégico Vinculado ao Link ---")
    print(resultado)
    
    print("3. Persistindo relatório em Markdown...")
    salvar_relatorio_markdown(resultado)