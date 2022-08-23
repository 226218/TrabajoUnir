# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:31:04 2022

@author: Amir
"""
from bs4 import BeautifulSoup
import requests

cookies
sesion
analizar las funciones

website = "http://procesos.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml"
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')
print(soup.prettify())