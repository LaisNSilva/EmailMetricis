# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:33:40 2020

@author: Fernando
"""
from tkinter import *
import pandas as pd 
from tkinter.ttk import *
import re
from textblob import TextBlob
from tqdm.auto import tqdm

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

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

root = Tk() 
root.geometry('200x100') 

  
# This function will be used to open 
# file in read mode and only Python files 
# will be opened

relevantes = pd.read_excel("ManchetesRelevantes.xlsx")

def cleanup(text):
    import string
    punctuation = '[\/!-.:?;]' # Note que os sinais [] são delimitadores de um conjunto.
    pattern = re.compile(punctuation)
    text_subbed = re.sub(pattern, ' ', text)
    return text_subbed

def prepara_novo_data_set(dataset):
    data = dataset
    global relevantes    
    
    #------------------------------------------------------------------
    manchetes = {}
    contador = 0
    email=[]
    lista_manchetes=[]
    numero_atual = 0
    loop = tqdm(total = data.shape[0], position = 0, leave = False)
    for i in data.HTML.index:
        loop.set_description("Extraindo manchetes...".format(numero_atual))
        loop.update(1)
        numero_atual += 1
        texto = str(data.HTML[i])

        for indice in range(len(texto)):

            if texto[indice:indice+7] == "message":

                manchete_incial = texto[indice+11:indice+150]
                achou = False
                manchete = " "
                indice_letra = 0
                email.append(i+2)

                while indice_letra < len(manchete_incial):

                    if manchete_incial[indice_letra] == "}":

                        manchete = manchete_incial[0:indice_letra-6]
                        achou = True
                        manchetes[contador] = manchete

                        manchete_limpa = cleanup(manchete)
                        manchete_min = manchete_limpa.lower()

                        try:
                            hi_blob = TextBlob(manchete_min)
                            manchete_pronta = hi_blob.translate(to='en')
                        except:
                            manchete_pronta = manchete_min

                        lista_manchetes.append(str(manchete_pronta))
                        contador += 1
                        break

                    else:

                        indice_letra += 1
    loop.close()
    #------------------------------------------------------------------
    lista_links = []
    for linha in data.HTML.index:   #Percorre cada linha do dataset
        texto = data.HTML[linha]

        contador_de_titulos = 0
        for indice in range(len(texto)-7):
            if texto[indice:indice+7] == "message":
                contador_de_titulos += 1



        indice = 0
        texto_com_url = ""

        while indice < len(texto):  #Percorre o texto dentro da linha
            if texto[indice:indice + 7] == "widgets":
                while True:
                    if texto[indice+5:indice+8] == "} ]":
                        break
                    else:
                        texto_com_url += texto[indice+8]
                        indice += 1
                break 
            else:
                indice += 1


        indice = 0
        numero_atual_de_titulos = 0

        while indice < len(texto_com_url) and numero_atual_de_titulos < contador_de_titulos:
            if texto_com_url[indice : indice+3] == "url":
                link = ""
                while True:
                    if texto_com_url[indice+7] == '"':
                        numero_atual_de_titulos += 1
                        break
                    else:
                        link += texto_com_url[indice+7]
                        indice += 1
                lista_links.append(link)
            else:
                indice += 1
    #------------------------------------------------------------------
    indice_lista = 0
    while indice_lista < len(lista_links):
        contador_de_https = 0
        contador = 0
        link = lista_links[indice_lista]
        while contador < len(link):
            if link[contador:contador+5] == "https" or link[contador:contador+4] == "http":
                contador_de_https += 1
            if contador_de_https == 2:
                link_completo = link[contador:len(link)]
                link_final = ""
                indice_google = 0
                while indice_google < len(link_completo):

                    if link_completo[indice_google : indice_google+7] == "u0026ct":
                        break
                    else:
                        link_final += link_completo[indice_google]
                        indice_google += 1

                lista_links[indice_lista] = link_final
                break
            contador += 1

        indice_lista += 1
    #------------------------------------------------------------------
    
    dicionario = {}
    
    dicionario['Manchetes'] = lista_manchetes
    #dicionario['Indice'] = email
    dicionario['Link'] = lista_links
    
    data_manchetes = pd.DataFrame(data=dicionario)
    
    result = pd.concat([data, data_manchetes], ignore_index=True, axis=1)
    
    result.columns = ['Data','De','HTML','Resumo','Manchete','Link']
    
    result["Relevância"] = int(0)
            
    return result

def preve(random_forest, svm, dtc, lg, data_test):
    model1 = int(dtc.predict(dado))
    model2 = int(random_forest.predict(dado))
    model3 = int(svm.predict(dado))
    model4 = int(lg.predict(dado)) 
        
    result = (model1+model2+model3+model4)/4
    
    if result >= 2/4:
        return 1
    else:
        return 0
        
    

# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

def classificar (treino, arquivo):
    # Pegando as manchetes e suas respctivas relevâncias 
    X = treino.loc[:, "Manchete"]
    y = treino.loc[:, "Relevância"]
    # Vetorizando
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    # Sepando em teste e treino
    # Porém vou colocar tudo para treino
    X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, y, test_size=0.01, random_state=42)

    # TREINOOOOOOO
    model = svm.SVC(kernel = 'linear')
    model.fit(X_train, y_train)
    
    clf =RandomForestClassifier(random_state=1)
    clf.fit(X_train, y_train)
    
    dtc = DecisionTreeClassifier()
    dtc.fit(X_train, y_train)
    
    model_lg = LogisticRegression(solver='lbfgs', multi_class='auto')
    model_lg.fit(X_train, y_train)
    
    NB = MultinomialNB()
    NB.fit(X_train, y_train)
    
    
   
     
    
    
    # Lendo o arquivo novo
    #arquivo = pd.read_excel(arquivo)

    # Prepara a base 
    arquivo = prepara_novo_data_set(arquivo)

    # Pegando as manchestes do arquivo novo
    X_novo = arquivo.loc[:, "Manchete"]

    #Classificação ATRAVES DO MIXED!!
    # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    y_pred = []
    for dado in X_novo:
        previsao = preve(clf, model, dtc, model_lg, dado)
        y_pred.append(previsao)

    # Fazer o retorno

    # Lista
    manchetes = X_novo
    pred = y_pred

    # Dicionarios\n",
    dic = {}

    dic['Manchetes'] = manchetes
    dic['Classificação'] = pred

    # Data
    classificados = pd.DataFrame(data=dic)

    # Tranformando em Excel
    planilha = classificados.to_excel (r'base_classificada.xlsx ', index = False)
    

    
# -----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------

base_para_treinar = pd.read_excel("base_pronta.xlsx")
content = None

def open_file(): 
    global content
    file = askopenfile(mode ='r', filetypes =[('Excel Files', '*.xlsx')]) 
    if file is not None: 
        file_name = file.name
        print(file_name)
        content = pd.read_excel(file_name)  
  
btn = Button(root, text ='Open', command = lambda:open_file()) 
btn.pack(side = TOP, pady = 10)     
    

proc = Button (root, text ='Processar', command = lambda:classificar(base_para_treinar, content)) 
proc.pack() 

  
mainloop() 