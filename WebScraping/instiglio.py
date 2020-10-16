import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import ActionChains

##----------------------------------------------
def retornaListaLinks(elementos):

    #lista de reposta para return
    resposta = []

    for elemento in elementos:

        #pega o link de cada elemento encontrado
        link = elemento.get_attribute("href")

        #adiciona o link na lista de reposta
        resposta.append(link)

    return resposta

##----------------------------------------------
def pegaListaAntigos(arquivo_excel):

    #cria lista de resposta para return
    resposta = []

    #le o arquivo excel com o backup dos links já adicionados
    df = pd.read_excel(arquivo_excel)

    #adiciona todos os links antigos na lista de resposta
    df["linksAntigos"].apply(lambda x: resposta.append(x))

    return resposta

##----------------------------------------------
def comparaListas(lista1, lista2):

    #cria lista de resposta para return
    resposta = []

    #vamos comparar cada elemento das duas lista
    for elemento in lista1:
        
        #se o elemento da lista1 não estiver na lista2...
        if elemento not in lista2:

            #adiciona o elemento novo na lista de resposta
            resposta.append(elemento)
        
        #se o elemento já estiver na outra lista, o link é antigo
        else:
            pass
    
    return resposta

##----------------------------------------------
            
#determina a url do site desejado
url = "https://www.instiglio.org/en/projects/"

#cria o webdriver
driver = webdriver.Chrome(executable_path=r'C:\Users\ferna\Documents\ChromeDriver\chromedriver.exe')

#pega o conteúdo da url
driver.get(url)

#tempo para carregar a página inteira
time.sleep(2)

#encontra a lista de elementos
elementos = driver.find_elements_by_css_selector(".wpb_wrapper [href]")

#cria lista de links encontrados
lista_links = retornaListaLinks(elementos)

#cria a lista de antigos:
lista_antigos = pegaListaAntigos("instiglio.xlsx")

#cria a lista com os links novos
lista_novos_links = comparaListas(lista_links, lista_antigos)


