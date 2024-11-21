import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import urllib3

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def fetch_url_content(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL: {e}")
        return None


def extract_course_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Extrair todas as tags h3, h4, h5, p e li
    relevant_tags = soup.find_all(["h3", "h4", "h5", "p", "li"])
    content = "\n".join([tag.get_text(strip=True) for tag in relevant_tags])

    return content


def summarize_content_with_openai(content):
    prompt = f"""
    Baseado no seguinte conteúdo extraído de uma página de curso, crie um resumo detalhado e informativo, excluindo qualquer menção ao nome da instituição ou outros detalhes irrelevantes ao propósito de descrever o curso. Siga as instruções abaixo cuidadosamente:

    {content[:6000]}

    Por favor, forneça um resumo completo em um único parágrafo contendo as seguintes informações:
    - Nome completo do curso
    - Tipo do curso (Bacharelado, Tecnólogo ou Licenciatura)
    - Duração do curso em (semestres, trimestres ou horas/aula)
    - Nome completo do coordenador do curso (se disponível)
    - Descrição do curso, que deve incluir:
      - Os Objetivos principais do curso
      - As Habilidades que os alunos desenvolverão
      - As áreas de atuação dos formados

    Importante:
    - Não inclua o nome da instituição, a menos que seja diretamente relevante à descrição.
    - Não mencione informações sobre contexto, regulamentos ou sistemas de ensino, a menos que sejam essenciais para entender o curso.
    - Evite repetir informações desnecessárias. Foque apenas nos dados solicitados.
    - Caso falte alguma informação (como o nome do coordenador), omita essa parte do resumo sem mencionar sua ausência.
    - Escreva o resumo em um único parágrafo com tom formal e informativo, mantendo a objetividade e clareza.
    - Use pontuação adequada para garantir a legibilidade do texto.
    
    Exemplo do formato esperado:
    O curso de {{NOME_CURSO}} é um curso de {{TIPO_CURSO}} com duração de {{DURACAO_CURSO}}, focado em {{OBJETIVOS_CURSO}}. Durante o curso, os alunos irão desenvolver {{HABILIDADES}} que irão prepará-los para atuar em {{AREAS_ATUACAO}}.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente especializado em resumir informações sobre cursos universitários de forma precisa, detalhada e concisa.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            top_p=0.9,
            max_tokens=500,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao processar a solicitação ao OpenAI: {e}")
        return None

def salvar_resposta(resposta, file_path):
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{resposta}\n")
    except Exception as e:
        print(f"Erro ao salvar em arquivo: {e}")


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("A chave da API do OpenAI não foi fornecida.")
        return

    directories = [
        "https://www.iesb.br/cursos/analise-e-desenvolvimento-de-sistemas/",
        "https://www.iesb.br/cursos/direito/",
        "https://www.iesb.br/cursos/ciencia-da-computacao/",
    ]

    for page_url in directories:
        print(f"Acessando {page_url}...")
        html_content = fetch_url_content(page_url)
        if html_content:
            course_content = extract_course_info(html_content)
            summary = summarize_content_with_openai(course_content)
            if summary:
                print("\nResposta da IA: Bem sucedida.")
                salvar_resposta(summary, "resumos_cursos_detalhados.txt")


if __name__ == "__main__":
    main()
