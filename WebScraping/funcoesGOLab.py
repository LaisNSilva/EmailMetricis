from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import ActionChains
import pandas as pd

def tentativa(numero_de_tentativas, css_code_selector,driver):
    
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

def retornaListaLinks(elementos):

    #lista de reposta para return
    resposta = []

    for elemento in elementos:

        #pega o link de cada elemento encontrado
        link = elemento.get_attribute("href")

        #adiciona o link na lista de reposta
        resposta.append(link)

    return resposta    


def acha_lista(numero_de_tentativas, css_code_selector, driver):
    
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
            links = driver.find_elements_by_class_name("search-result__link")
            print("os links são:")
            print(links)
            lista_links = retornaListaLinks(links)
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
        
    return elementos, lista_links  

def compara(arquivo, dados):
    #referencia = pd.read_excel(arquivo)
    referencia=arquivo
    novas_manchetes=[]
    novos_links=[]
    man_ref = referencia["Manchetes"].tolist()
    link_ref = referencia["Links"].tolist()
    dado_man = dados['Manchetes'].tolist()
    for e in range(0, len(dados['Manchetes'])):
        if dado_man[e] not in man_ref:
            novas_manchetes.append(dados['Manchetes'][e])
            novos_links.append(dados['Links'][e])
            # adicionar ao referencail
            man_ref.append(dados['Manchetes'][e])
            link_ref.append(dados['Links'][e])

    dic = {}
    dic["Manchetes novas"] = novas_manchetes
    dic["Links novas"] = novos_links

    dic_ref = {}
    dic_ref["Manchetes"] = man_ref
    dic_ref["Links"] = link_ref

    referencias = pd.DataFrame(data=dic_ref)

    resultado = pd.DataFrame(data=dic)

    resultado.to_excel('GOLab.xlsx', index = False)

    return referencias, novos_links
