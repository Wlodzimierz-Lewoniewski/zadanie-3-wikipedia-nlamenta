import re
from urllib.parse import quote
import requests

# Funkcja do pobrania i przetworzenia artykułów z danej kategorii
def wyciagnij(kategoria):
    kategoria = kategoria.replace(" ", "_")
    kategoria_encoded = quote(kategoria)
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{kategoria_encoded}"
    response = requests.get(url).text

    # Wyszukiwanie pierwszych dwóch artykułów w kategorii
    main_content = response[re.search(re.compile(r'mw-category-generated'), response).start():]
    artykuly = re.findall(r'<a href="(/wiki/[^":#]*?)".*?>(.*?)</a>', main_content)[:2]

    if not artykuly:
        print("Nie znaleziono artykułów w tej kategorii.")
        return

    for artykul in artykuly:
        tytul = artykul[1]
        artykul_url = f"https://pl.wikipedia.org{artykul[0]}"
        response_artykul = requests.get(artykul_url).text

        # Znajdowanie linków wewnętrznych
        start = re.search(re.compile(r'id="mw-content-text"'), response_artykul).start()
        text_content = response_artykul[start:]
        linki = re.findall(re.compile(r'href="[^:]+?".+?title="(.*?)"'), text_content)[:5]

        # Znajdowanie obrazków
        image_text = re.search(re.compile(r'mw-content-text(.+?)<noscript>', re.DOTALL), text_content).group()
        images = re.findall(re.compile(r'<img.+?src="(.+?)"'), image_text)
        images = images[:3]  # Pierwsze 3 obrazy
        images = [img for img in images]  # Bez dodawania "https:"

        # Znajdowanie źródeł zewnętrznych
        sources_text = re.search(re.compile(r'id="Przypisy"(.+)', re.DOTALL), text_content)
        if sources_text:
            sources_text = re.search(re.compile(r'class="references"(.+?)</ol>', re.DOTALL), sources_text.group()).group()
            linki2 = re.findall(re.compile(r'"(http.+?)"'), sources_text)[:3]
        else:
            linki2 = []

        # Znajdowanie przypisanych kategorii
        categories_text = re.search(re.compile('mw-normal-catlinks(.+?)</div>'), text_content).group()
        kategorie = re.findall(re.compile(r'<li.+?>(.+?)</a></li>'), categories_text)[:3]

        # Wyświetlanie w odpowiednim formacie
        print(f" | ".join(linki))
        print(" | ".join(images))
        print(" | ".join(linki2))
        print(" | ".join(kategorie))

# input
kategoria_input = input("Podaj nazwę kategorii na Wikipedii: ").strip()
wyciagnij(kategoria_input)
