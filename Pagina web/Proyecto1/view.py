import requests
import multiprocessing
from bs4 import BeautifulSoup
from time import time
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.shortcuts import render
import json

class Game(object):
    def __init__(self, titulo, precioGaming, precioEbay, imagen, descripcion, calificacion, duracion):
        self.titulo = titulo
        self.precioGaming = precioGaming 
        self.precioEbay = precioEbay
        self.imagen = imagen 
        self.descripcion = descripcion
        self.calificacion = calificacion 
        self.duracion = duracion

def pagina(request):

    doc_externo = loader.get_template('miplantilla.html')

    games = []

    with open('C:/Users/Personal/Desktop/TEC/Semestre_2/Arquitectura de computadores/Proyecto Multicore/datos.json', 'r') as f:
        datos = json.load(f)

    for game in range(50):
        titulo = datos['titulo'][game]
        precioGaming = datos['precioGaming'][game]
        precioEbay = datos['precioEbay'][game]
        imagen = datos['imagen'][game]
        descripcion = datos['descripcion'][game]
        calificacion = datos['calificacion'][game+game]
        duracion = datos['duracion'][game]
        g1 = Game(titulo, precioGaming, precioEbay, imagen, descripcion, calificacion, duracion)
        games.append(g1)

    documento = doc_externo.render({'Games': games})

    return HttpResponse(documento)

