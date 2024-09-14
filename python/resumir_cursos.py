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

def extract_text_from_html(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        headers = soup.find_all(["h3", "h4", "h5"])
        header_text = "\n".join([tag.get_text() for tag in headers])
        return f"{header_text}\n{soup.get_text()}"
    except Exception as e:
        print(f"Erro ao processar o HTML: {e}")
        return None

def summarize_content_with_openai(content, question):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"Resumo do conteúdo: {content[:5000]}\nBaseado nesse resumo, responda a seguinte pergunta: {question}",
                }
            ],
            temperature=0.1,
            max_tokens=2000,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Erro ao processar a solicitação ao OpenAI: {e}")
        return None

def salvar_resposta(resposta, file_path):
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"{resposta}\n\n")
    except Exception as e:
        print(f"Erro ao salvar em arquivo: {e}")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("A chave da API do OpenAI não foi fornecida.")
        return

    directories = [
        "https://www.iesb.br/cursos/analise-e-desenvolvimento-de-sistemas/",
        "https://www.iesb.br/cursos/direito/",
    ]

    for page_url in directories:
        print(f"Acessando {page_url}...")
        html_content = fetch_url_content(page_url)
        if html_content:
            text_content = extract_text_from_html(html_content)
            if text_content:
                question = "Fale sobre o nome do curso, qual o tipo de curso, qual a duração do curso em semestres e qual o nome do coordenador do curso. Fale também de forma resumida um pouco sobre o curso. Não responda com urls e não utilize aspas."
                summary = summarize_content_with_openai(text_content, question)
                if summary:
                    print("\nResposta da IA:")
                    print(summary)
                    salvar_resposta(summary, "resumos.txt")

if __name__ == "__main__":
    main()