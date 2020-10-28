# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:22:18 2020

@author: ferna
"""
import pandas as pd
import datetime

def criaDicionario(social, instiglio, GOLab, ThirdSector):

    #cria o dataframe com as novidades de cada site
    df = pd.DataFrame({'Social_Finance': pd.Series(social), 'Instiglio': pd.Series(instiglio), 'GOLab': pd.Series(GOLab), 'Third Sector': pd.Series(ThirdSector)} )
    
    return df

def verificaNovidade(lista1, lista2, lista3, lista4):
    
    #se nao houver nenhuma novidade...
    if len(lista1) == 0 and len(lista2) == 0 and len(lista3) == 0 and len(lista4) == 0:
        return False
    else:
        return True
        

#executa o arquivo do socialFinance
exec(open('socialFinance.py').read())

#cria uma lista com os novos do social finance
novos_socialFinance = lista_links_novos

#executa o arquivo do socialFinance
exec(open('instiglio.py').read())

#cria uma lista com os novos do social finance
novos_instiglio = lista_novos_links

#executa o arquivo do GOLab
exec(open('GOLab.py').read())
#cria uma lista com os novos do GOLab
novos_GOLab = lista_novos_links

#executa o arquivo do Third Sector
exec(open('ThirdSector.py').read())
#cria uma lista com os novos do Third Sector
novos_ThirdSector = lista_novos_links



#verifica se tem novidade
novidade = verificaNovidade(novos_socialFinance, novos_instiglio, novos_GOLab, novos_ThirdSector)

#se tiver novidade...
if novidade == True:

    #cria o dataframe que será transformado em excel
    df = criaDicionario(novos_socialFinance, novos_instiglio, novos_GOLab, novos_ThirdSector)
    
    df = df.fillna("No Data")
    
    print(df)
    
    #variavel responsavel por pegar o tempo presente
    now = datetime.datetime.now()
    
    #monta o horário atual
    hora_data = "scraped_{0}_{1}".format(now.day, now.month)
    
    df.to_excel("./WebScrepedFiles/{0}.xlsx".format(hora_data), index=False)

#caso não tenha novidade...
else:
    print("Sorry, we don't have any news today!")
    



    
    
