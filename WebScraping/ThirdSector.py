from funcoesTS import *



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
while n <= 1:
    url = "https://www.thirdsectorcap.org/projects/"
    print('url')
    #cria o webdriver
    driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
    print('cria o webdriver')

    #pega o conteúdo da url
    driver.get(url)
    print('pega o conteúdo da url')
    #tempo para carregar a página inteira
    time.sleep(10)
    print('carregando')


    #fecha pop-up
    tentativa(1000, "#ngo > div.ngo-popup > div.got-it", driver)
    print('tentativas')

    lista_de_projetos = acha_lista(1000, "#ngo > div.portifolio-table-nav > div", driver)
    print("lista de projetos")
    #print(lista_de_projetos)


    for l_elemento in lista_de_projetos:
        for e in l_elemento:
            #print(e.text)
            manchetes.append(e.text)
    
        
    n = n+1
    driver.close()
    
    
    
#print(manchetes)
    
    
dicionario = {}

dicionario["Manchetes"] = manchetes


resultado = pd.DataFrame(data=dicionario)

ref=pd.read_excel("TS_referencia.xlsx")

referenciais, lista_novos_links = compara(ref, resultado)

referenciais = resultado.to_excel('TS_referencia.xlsx', index = False)

