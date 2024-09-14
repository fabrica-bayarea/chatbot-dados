from playwright.sync_api import sync_playwright
import time

def extract_links(page):
    return page.evaluate("""
        () => Array.from(document.querySelectorAll('.bt.mais')).map(link => link.href)
    """)

def click_load_more(page):
    while True:
        load_more_button = page.query_selector('a.bt.red:has-text("Carregar mais")')
        if not load_more_button:
            break
        load_more_button.click()
        time.sleep(5)

url = "https://www.iesb.br/modalidades/graduacao-presencial/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    time.sleep(5)

    click_load_more(page)
    time.sleep(5)

    all_links = extract_links(page)

    with open("links.txt", "a") as file:
        for link in all_links:
            file.write(link + "\n")

    browser.close()

print("Script concluído.")