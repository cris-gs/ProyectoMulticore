import requests
import multiprocessing
from time import time
import json

user_agent = {'User-agent':'Mozilla/5.0'}
page = requests.get("https://www.metacritic.com/browse/games/score/metascore/all/ps4/filtered?view=detailed", headers= user_agent)
url_Instant_Gaming = "https://www.instant-gaming.com/es/busquedas/?q="
url_Ebay = "https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw="
url_How_Long_to_Beat = "https://howlongtobeat.com/game?id="

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')

games = {'titulo': [], 'precioGaming': [], 'precioEbay':[], 'imagen': [], 'descripcion': [], 'calificacion': [], 'duracion': []}

for titulo in soup.find_all('a', {'class':'title'}, limit=50):
    games['titulo'].append(titulo.text)
for descripcion in soup.find_all('div', {'class':'summary'}, limit=50):
    games['descripcion'].append(descripcion.text)
for calificacion in soup.find_all('div', {'class':'metascore_w large game positive'}, limit=100):
    games['calificacion'].append(calificacion.text)

linkDuracion = [27100, 4064, 66630, 20221, 38050, 41753, 15221, 5918, 20077, 4867, 21262, 30385, 10270, 39525, 12654, 52731, 40171, 42818, 21694, 38029, 57479, 3608, 20605, 31590, 19512, 12655, 3435, 52493, 22804, 10270, 57415, 61569, 52493, 40535, 38000, 26803, 57523, 12654, 869, 64753, 78213, 66595, 11627, 38001, 26784, 6064, 45392, 9782, 38029, 59820]

def parte1(duracion):
    direccionDuracion = url_How_Long_to_Beat + str(duracion)
    pageDuracion = requests.get(direccionDuracion, headers= user_agent)
    soupDuracion = BeautifulSoup(pageDuracion.content, 'html.parser')
    duracionGame = soupDuracion.find("div", {"class":"game_times"})
    return duracionGame.text.replace("\n"," ")

def parte2(titulo):
    tituloGaming = titulo.replace(" ", "+").lower()
    direccionGaming = url_Instant_Gaming + tituloGaming.replace(":", "V%3A")
    pageGaming = requests.get(direccionGaming, headers= user_agent)
    soupGaming = BeautifulSoup(pageGaming.content, 'html.parser')
    precioGaming = soupGaming.find('div', {'class': 'price'})
    return precioGaming.text


def parte3(titulo):
    try:
        titulo1 = titulo.replace("-", "").lower()
        tituloEbay = titulo1.replace(" ", "-")
        direccionEbay = url_Ebay + tituloEbay.replace(":", "%3A")
        pageEbay = requests.get(direccionEbay, headers= user_agent)
        soupEbay = BeautifulSoup(pageEbay.content, 'html.parser')
        precioEbay = soupEbay.find('span', {'class': 'ITALIC'})
        precio = precioEbay.text

    except Exception as a:
        precio = "N/A"
        pass
    return precio

if __name__ == '__main__':
    start_time = time()

    pool = multiprocessing.Pool(processes=4)
    duracion = pool.map(parte1, linkDuracion)
    games['duracion'] = duracion
    precioG = pool.map(parte2, games['titulo'])
    games['precioGaming'] = precioG
    precioE = pool.map(parte3, games['titulo'])
    games['precioEbay'] = precioE

    elapsed_time = time() - start_time

    for game in range(50):
        print(game + 1, "Título: ", games['titulo'][game])
        print("\n")
        print("Precio de Instant Gaming: ", games['precioGaming'][game])
        print("\n")
        print("Precio de Ebay: ", games['precioEbay'][game])
        print("\n")
        imagen = soup.find('img', {'alt': games['titulo'][game]})
        games['imagen'].append(imagen["src"])
        print("Imagen", imagen["src"])
        print("\n")
        print("Descripción:", games['descripcion'][game])
        print("\n")
        print("Calificación", games['calificacion'][game+game])
        print("\n")
        print("Duración:", games['duracion'][game])
        print("---------------------------------------------------------")

    print("Elapsed time: %0.10f seconds." % elapsed_time)

    with open('datos.json', 'w') as f:
        json.dump(games, f)