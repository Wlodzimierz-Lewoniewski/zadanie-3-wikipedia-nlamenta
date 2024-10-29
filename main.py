import re
from urllib.request import urlopen
from urllib.parse import quote
import sys
import io

# Ustawienie odpowiedniego kodowania dla konsoli
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# funkcja do pobrania i przetworzenia artykułów z danej kategorii
def wyciagnij(kategoria):
    # Przygotowanie URL do kategorii z kodowaniem
    kategoria_encoded = quote(kategoria)
    url = "https://pl.wikipedia.org/wiki/Kategoria:" + kategoria_encoded
    odp = urlopen(url)
    html = odp.read().decode("utf-8")

    # wyszukiwanie pierwszych dwóch artykułów w kategorii
    artykuly = re.findall(r'<a href="(/wiki/[^":#]*?)".*?>(.*?)</a>', html)
    artykuly = artykuly[:2]  # ograniczenie do pierwszych dwóch artykułów

    for artykul in artykuly:
        tytul = artykul[1]  # Tytuł artykułu
        artykul_url = f"https://pl.wikipedia.org{artykul[0]}"

        odp_artykul = urlopen(artykul_url)
        artykul_zawartosc = odp_artykul.read().decode('utf-8')

        # Znajdowanie linków wewnętrznych
        linki = re.findall(r'<a href="(/wiki/[^":#]*?)".*?>(.*?)</a>', artykul_zawartosc)
        linki = [(link[1], f"https://pl.wikipedia.org{link[0]}") for link in linki[:5]]

        # Znajdowanie obrazków
        zdj_linki = re.findall(r'<img.*?src="(//upload.wikimedia.org.*?)".*?>', artykul_zawartosc)
        zdj_linki = zdj_linki[:3]  # Pierwsze 3 obrazy
        zdj_linki = [f"https:{link}" for link in zdj_linki]  # Dodajemy protokół

        # Znajdowanie źródeł zewnętrznych
        linki2 = re.findall(r'<a href="(https?://[^"]+)"', artykul_zawartosc)
        linki2 = linki2[:3]  # Pierwsze 3 źródła

        # Znajdowanie przypisanych kategorii
        kategorie = re.findall(r'<div class="catlinks">.*?<ul>(.*?)</ul>', artykul_zawartosc, re.DOTALL)
        kategorie = re.findall(r'<li><a href="[^"]*?">([^<]*?)</a>', kategorie[0]) if kategorie else []
        kategorie = kategorie[:3]  # Pierwsze 3 kategorie

        # Wyświetlanie w odpowiednim formacie
        print(f"{tytul} | ", end="")
        print(" | ".join([link[0] for link in linki]), end=" | ")
        print(" | ".join(zdj_linki), end=" | ")
        print(" | ".join(linki2), end=" | ")
        print(" | ".join(kategorie))
        print("\n" + "-" * 50 + "\n")

# input
kategoria_input = input("Podaj nazwę kategorii na Wikipedii: ").strip()
wyciagnij(kategoria_input)
