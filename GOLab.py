# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 11:59:35 2020

@author: Lais Nascimento
"""

from tkinter import *
import pandas as pd 
from tkinter.ttk import *
import re
from textblob import TextBlob
from tqdm.auto import tqdm
from tkinter import Label
import time



# Importar a função que classifica as manchetes
#from funcao.ipynb import classificar
  
# importing askopenfile function 
# from class filedialog 
from tkinter.filedialog import askopenfile
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import f1_score, recall_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score


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

def cleanup(text):
    import string
    punctuation = '[\/!-.:?;]' # Note que os sinais [] são delimitadores de um conjunto.
    pattern = re.compile(punctuation)
    text_subbed = re.sub(pattern, ' ', text)
    return text_subbed

def classifica_dataset(dataset, model, count_vect):
    X = dataset.loc[:,"Manchete"]
    pred = count_vect.transform(X).toarray()
    predict = model.predict(pred)

    dataset["Relevância"] = pd.Series(predict)

    return dataset

def classificar (treino, arquivo):
    global relevantes
    
    
    
    X_para_treinar = treino.loc[:, "Manchete"]
    Y_para_treinar = treino.loc[:, "Relevância"]
    ##y = arquivo.loc[:, "Relevância"]

    # Vetorizando
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_para_treinar).toarray()


    # Sepando em teste e treino
    # Porém vou colocar tudo para treino
    X_train, X_test, y_train, y_test = train_test_split(X_train_counts, Y_para_treinar, test_size=0.001, random_state=42)
    #Aplicando o modelo SVM (Support Vector Machine)

    kernels = ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']

    model = svm.SVC(kernel = 'linear') #Kernel

    #Dando fit no modelo SVM usando o dataset de treino
    model.fit(X_train, y_train)
    
    planilha_classificada = classifica_dataset(arquivo, model, count_vect)
    
    if planilha_classificada["Relevância"].max() == 0:
        print("NENHUMA MANCHETE RELEVANTE ENCONTRADA!")
    else:
        planilha_final = planilha_classificada.loc[planilha_classificada["Relevância"] == 1][["Link", "Manchete", "Relevância"]]
        planilha_final.columns = ["Manchete","Link", "Relevância"]
        
        planilha_final = pd.DataFrame(planilha_final)
        planilha_final.drop_duplicates() 
        try:
            
            planilha = planilha_final.to_excel('ManchetesRelevantes_GOLab.xlsx', index = False)
            
        except:  
            print('The file already exists!')
    
base_para_treinar = pd.read_excel("base_pronta.xlsx")    

manchetes = []
for elemento in lista_de_projetos:
    manchetes.append(cleanup(elemento.text))
print(manchetes)



# POR ENQUATO
links = []
relevancia=[]
n=0
for e in manchetes:
    n+=1
    links.append(n)
    relevancia.append(1)
    
dicionario = {}

dicionario['Manchete'] = manchetes
#dicionario['Indice'] = email
dicionario['Link'] = links
dicionario['Relevancia'] = relevancia

resultado = pd.DataFrame(data=dicionario)

classificar(base_para_treinar, resultado)



    



