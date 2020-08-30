# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:59:35 2020

@author: Lais Nascimento
"""



from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import ActionChains

#determina a url do site desejado
url = "https://golab.bsg.ox.ac.uk/knowledge-bank/indigo-data-and-visualisation/impact-bond-dataset-v2/"

#cria o webdriver
driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')

#pega o conteúdo da url
driver.get(url)

#tempo para carregar a página inteira
time.sleep(10)

def tentativa(numero_de_tentativas, css_code_selector):
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    while tentativa_atual <= numero_de_tentativas:
        
        #tenta clicar no botão
        try:
            driver.find_element_by_css_selector(css_code_selector).click()
            break
        
        #caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1
    
    #caso o número de tentativas seja igual ao número limite, não foi possível concluir 
    #a ação
    if tentativa_atual == numero_de_tentativas:
        print("Número de tentativas excedidas")
        
    #caso contrário, informa que passou no teste
    else:
        print("Pass!")
    
    return

def acha_lista(numero_de_tentativas, css_code_selector):
    
    #cria uma lista vazia para dar return
    elementos = None
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    while tentativa_atual < numero_de_tentativas:
        #lista = driver.find_elements_by_css_selector(css_code_selector)
        #elementos = lista.find_elements_by_class_name("project")
#            print("deu")
        
        #tenta clicar no botão
        try:
            #lista = driver.find_elements_by_css_selector(css_code_selector)
            elementos = driver.find_elements_by_class_name("search-result__title")
            break
        
        #caso não funcione, aumenta a tentativa
        except:
            tentativa_atual += 1
            
    #caso o número de tentativas seja igual ao número limite, não foi possível concluir 
    #a ação
    if tentativa_atual == numero_de_tentativas:
        print("Número de tentativas excedidas")
    
    #caso contrário, informa que passou no teste
    else:
        print("Pass!")
        
    return elementos

#fecha pop-up
tentativa(1000, "#ngo > div.ngo-popup > div.got-it")

lista_de_projetos = acha_lista(1000, "#ngo > div.search-results > div")



for elemento in lista_de_projetos:
    print(elemento.text + " ------------------------------ " + str(type(elemento)))

