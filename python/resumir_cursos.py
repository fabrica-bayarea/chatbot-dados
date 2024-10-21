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

    # Extrair todas as tags h1, h2, h3, h4, h5, p e li
    relevant_tags = soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li"])
    content = "\n".join([tag.get_text(strip=True) for tag in relevant_tags])

    return content


def summarize_content_with_openai(content):
    prompt = f"""
    Baseado no seguinte conteúdo extraído de uma página de curso, crie um resumo detalhado e informativo:

    {content[:6000]}

    Por favor, forneça um resumo completo em um único parágrafo contendo as seguintes informações:
    - Nome completo do curso
    - Tipo do curso (Bacharel, Tecnólogo ou Licenciatura)
    - Duração do curso em semestres
    - Nome completo do coordenador do curso (se disponível)
    - Uma descrição detalhada do curso, incluindo:
      - Objetivos principais do curso
      - Habilidades que os alunos desenvolverão
      - Áreas de atuação dos formados

    Importante:
    - Inclua todas as informações relevantes encontradas no conteúdo fornecido
    - Use um tom formal e informativo
    - Mantenha o resumo em um único parágrafo, mas seja o mais completo possível
    - Se alguma informação estiver faltando, não a mencione no resumo
    - Caso o Coordenador não seja mencionado, omita essa informação
    - Use pontuação adequada para separar as informações e manter a legibilidade
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
        "https://www.iesb.br/cursos/pos-ead-em-alfabetizacao-e-letramento-e-a-psicopedagogia-institucional/",
        "https://www.iesb.br/cursos/pos-ead-em-direito-de-familia-e-sucessoes/",
        "https://www.iesb.br/cursos/pos-ead-em-direito-e-processo-penal/",
        "https://www.iesb.br/cursos/pos-ead-em-direito-tributario/",
        "https://www.iesb.br/cursos/pos-ead-em-direito-processual-civil/",
        "https://www.iesb.br/cursos/pos-ead-em-direito-empresarial/",
        "https://www.iesb.br/cursos/pos-ead-em-direito-administrativo/",
        "https://www.iesb.br/cursos/pos-sempresencial-em-psicomotricidade/",
        "https://www.iesb.br/cursos/pos-ao-vivo-em-analise-e-desenvolvimento-de-sistemas/",
        "https://www.iesb.br/cursos/pos-ao-vivo-em-business-intelligence/",
        "https://www.iesb.br/cursos/pos-ao-vivo-em-banco-de-dados/",
        "https://www.iesb.br/cursos/transformacao-digital/",
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
