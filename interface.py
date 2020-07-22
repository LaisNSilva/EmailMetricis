# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:33:40 2020

@author: Fernando
"""
from tkinter import *
import pandas as pd
from tkinter import * 
from tkinter.ttk import *

# Importar a função que classifica as manchetes
#from funcao.ipynb import classificar
  
# importing askopenfile function 
# from class filedialog 
from tkinter.filedialog import askopenfile 

root = Tk() 
root.geometry('200x100') 

  
# This function will be used to open 
# file in read mode and only Python files 
# will be opened 
def open_file(): 
    file = askopenfile(mode ='r', filetypes =[('Excel Files', '*.xlsx')]) 
    if file is not None: 
        file_name = file.name
        print(file_name)
        content = pd.read_excel(file_name) 
        print(content) 
  
btn = Button(root, text ='Open', command = lambda:open_file()) 
btn.pack(side = TOP, pady = 10)     
    

proc = Button (root, text ='Processar', command = lambda:classificar(content)) 
proc.pack() 

  
mainloop() 