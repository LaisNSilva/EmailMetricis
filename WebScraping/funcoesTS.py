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


def acha_lista(numero_de_tentativas, css_code_selector, driver):
    
    #cria uma lista vazia para dar return
    elementos = None
    
    #numero da tentativa atual
    tentativa_atual = 0 
    
    #define um número limite de tentativas
    elementos=[]
    acabou = False
    l = 1
    i = 1
    while tentativa_atual < numero_de_tentativas:
        #lista = driver.find_elements_by_css_selector(css_code_selector)
        #elementos = lista.find_elements_by_class_name("project")
#            print("deu")
        
        #tenta clicar no botão
        try:
            
            while l != 0 :
                #try:
                elemento = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[1]')
                l = len(elemento)
                elementos.append(elemento)
                i=i+2
            print(i)
                     
                #except:
                    #acabou = True
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
        
    return elementos #, links  

def compara(arquivo, dados):
    #referencia = pd.read_excel(arquivo)
    referencia=arquivo
    novas_manchetes=[]
    novos_links=[]
    man_ref = referencia["Manchetes"].tolist()
    dado_man = dados['Manchetes'].tolist()
    for e in range(0, len(dados['Manchetes'])):
        if dado_man[e] not in man_ref:
            novas_manchetes.append(dados['Manchetes'][e])
            # adicionar ao referencail
            man_ref.append(dados['Manchetes'][e])
            

    dic = {}
    dic["Manchetes novas"] = novas_manchetes
    

    dic_ref = {}
    dic_ref["Manchetes"] = man_ref
    
    referencias = pd.DataFrame(data=dic_ref)

    resultado = pd.DataFrame(data=dic)

    resultado.to_excel('TS.xlsx', index = False)

    return referencias, novas_manchetes
