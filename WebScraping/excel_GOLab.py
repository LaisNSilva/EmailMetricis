# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:59:35 2020

@author: Lais Nascimento
"""

from tkinter import *

from tkinter.ttk import *
import re
from textblob import TextBlob
from tqdm.auto import tqdm
from tkinter import Label
import time

from funcoes import *



# Importar a função que classifica as manchetes
#from funcao.ipynb import classificar
  
# importing askopenfile function 
# from class filedialog 

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import ActionChains

#determina a url do site desejado
n = 1
manchetes = []
links = []
while n <= 10:
    url = "https://golab.bsg.ox.ac.uk/knowledge-bank/indigo-data-and-visualisation/impact-bond-dataset-v2/?page="+str(n)

    #cria o webdriver
    driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

    #pega o conteúdo da url
    driver.get(url)

    #tempo para carregar a página inteira
    time.sleep(10)


    #fecha pop-up
    tentativa(1000, "#ngo > div.ngo-popup > div.got-it", driver)

    lista_de_projetos, lista_de_links = acha_lista(1000, "#ngo > div.search-results > div", driver)


    for elemento in lista_de_projetos:
        manchetes.append(elemento.text)
    
    for l in lista_de_links:
        links.append(l.text)
        
    n = n+1
    driver.close()
    
print(manchetes)
print(links)

dicionario = {}

dicionario["Manchetes"] = manchetes
dicionario["Links"] = links

resultado = pd.DataFrame(data=dicionario)

resultado.to_excel('GOLab_referencia.xlsx', index = False)
    







    



