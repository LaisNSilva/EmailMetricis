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

root = Tk() 
root.geometry('400x150') 

progress = Progressbar(root, orient = HORIZONTAL, 
              length = 180, mode = 'determinate') 
file_text = Text(root, height=0.5, width=22)

output_text = Text(root, height=0.5, width=40)
  
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
    data = dataset.loc[dataset["De"] == "googlealerts-noreply@google.com"]
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
    
    progress['value'] = 40
    root.update_idletasks() 
    time.sleep(0.01) 
    
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
    
    result["Relevância"] = int(1)
            
    return result

def classifica_dataset(dataset, model, count_vect):
    X = dataset.loc[:,"Manchete"]
    pred = count_vect.transform(X).toarray()
    predict = model.predict(pred)

    dataset["Relevância"] = pd.Series(predict)

    return dataset


def classificar (treino, arquivo):
    global relevantes
    
    progress['value'] = 0
    root.update_idletasks() 
    time.sleep(1) 
    
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
    
    progress['value'] = 20
    root.update_idletasks() 
    #time.sleep(1) 
     # -------------------------------------------------------------------------------------------------------------   
    #Tratando o dataset escolhido
    
    try:
        dataset_escolhido_preparado = prepara_novo_data_set(arquivo)
    except:
        output_text.insert(END, ' ')
        output_text.insert(END, 'Excel format error!')
        return
        
        
    
    progress['value'] = 60
    root.update_idletasks() 
    time.sleep(1) 
    
    planilha_classificada = classifica_dataset(dataset_escolhido_preparado, model, count_vect)
    progress['value'] = 80
    root.update_idletasks() 
    time.sleep(1) 

    if planilha_classificada["Relevância"].max() == 0:
        output_text.insert(END, 'Nenhuma manchete relevante encontrada!')
        print("NENHUMA MANCHETE RELEVANTE ENCONTRADA!")
    else:
        planilha_final = planilha_classificada.loc[planilha_classificada["Relevância"] == 1][["Link", "Manchete", "Relevância"]]
        planilha_final.columns = ["Manchete","Link", "Relevância"]
        
        planilha_final = pd.DataFrame(planilha_final)
        planilha_final.drop_duplicates() 
        try:
            
            planilha = planilha_final.to_excel('BASE_CLASSIFICADA.xlsx', index = False)
            output_text.insert(END, ' ')
            output_text.insert(END, 'Done!')
        except:
            output_text.insert(END, ' ')
            output_text.insert(END, 'The file already exists!')
    
    # Tranformando em Excel
    #planilha = planilha_pandas.to_excel (r'base_classificada.xlsx ', index = False)
    
    progress['value'] = 100
    root.update_idletasks() 
    time.sleep(1) 
    

base_para_treinar = pd.read_excel("base_pronta.xlsx")
content = None

def open_file(): 
    global content
    file = askopenfile(mode ='r', filetypes =[('Excel Files', '*.xlsx')]) 
    if file is not None: 
        file_name = file.name
        print(file_name)
        file_text.insert(END, file_name)
        content = pd.read_excel(file_name)  
  
btn = Button(root, text ='Open', command = lambda:open_file()) 
btn.pack()     


proc = Button(root, text = 'Process', command = lambda:classificar(base_para_treinar, content)) 
proc.pack() 

root.title("Insper Metricis Classifier")

btn.place(relx = 0.2, x =20, y = 20, anchor = NE)
proc.place(relx = 0.2, x =20, y = 60, anchor = NE)

file_text.pack(pady = 22)
progress.pack(pady =0.15)
output_text.pack(pady = 20)



#Now to update the Label text, simply `.set()` the `StringVar`
#my_string_var.set("Insper Metricis Classifier")

  
mainloop() 