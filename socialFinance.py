# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 19:58:37 2020

@author: Fernando
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import ActionChains

#determina a url do site desejado
url = "https://sibdatabase.socialfinance.org.uk/"

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
            elementos = driver.find_elements_by_class_name("project")
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

#a função a seguir serve para, após encontrar os elementos que compõe a lista
#de projetos do social Fincance, pegar somente o código dos elementos da página 
    
#def define_codigo_da_lista(lista_de_elementos_web):
#    
#    #cria uma lista vazia a qual será alimentada somente com os 
#    #códigos dos elementos da página
#    lista_filtrada = []
#    
#    
#    for elemento in lista_de_elementos_web:
#        
#        #define o valor do codigo caso ele não seja encontrado no elemento
#        codigo = "código não encontrado"
#        
#        #texto do elemento não-filtrado
#        texto = str(elemento)
#
#        #define indice inicial                
#        indice = 0
#        
#        #percorre o texto em busca da palavra elements...
#        while indice < len(texto):
#            
#            #caso encontre a palavra element, pegamos o código posterior a ela
#            if str(texto[indice:indice+8]) == "element=": 
#                
#                #caso encontre a palavra element, pegamos o codigo que vem depois da palavra
#                codigo = str(texto[indice+9:len(texto)-3])
#                
#                #o codigo foi encontrado, podemos parar o while
#                break
#                
#            #caso a palavra não seja encontrada precisamos avnaçar o indice
#            else:
#                indice += 1
#        
#        
#        #depois de encontrar o codigo, adicionamos ele na lista filtrada
#        lista_filtrada.append(codigo)
#        
#    return lista_filtrada

#def encontra_codigos_novos(lista_inseridos, lista_de_codigos):
#    
#    #cria uma lista para retornar os codigos novos
#    lista_de_codigos_novos = []
#    
#    #para cada elementos da "lista_de_codigos" tenta achar um correspondente
#    #na "lista_inseridos"
#    for codigo in lista_de_codigos:
#        
#        #se o codigo em questão não estiver na lista de inseridos...
#        if lista_inseridos.count(str(codigo)) == 0:
#            
#            #adiciona o novos codigo na "lista_de_codigos_novos"
#            lista_de_codigos_novos.append(codigo)
#    
#    return lista_de_codigos_novos
        

#def encontra_titulo(lista_selenium):
#    dicionario_de_projetos = dict()
#    
#    indice_projeto = 1
#    
#    for elemento in lista_selenium:
#        
    
# a lista abaixo contem todos os codigos dos projetos que já foram lidos e inseridos na
#Base OBC, assim é necessario manter essa lista atualizada.
    
codigo_projetos_ja_inseridos = ['a7652de7-a440-4051-a71f-65eaee8599e9', 'e9262386-63f0-487c-96c3-ee811e6d9185', '64a82801-c766-497e-a989-030fc1e18310', 'ac79dd35-866e-4a63-9305-50cf72e01c85', '58393248-ff4f-4d60-8e9f-51f6aba3cbfa', '8e92e792-bf5c-465c-ad96-bc45ed5d8746', 'c991ced9-a10a-45fe-b515-2f60bc2b6d68', 'ff86d906-630e-4061-bcf9-4ac509b053b5', '40207699-04ee-4c2f-8c5b-3a790875ecb5', '643af7f5-79b0-4374-a2e0-0c7ac2f65490', 'e1146e15-df06-40fb-bee1-effc9093fdac', '1cd68700-679e-4a85-b207-9dbaa59c49fb', '980d38e2-2e40-4e62-8165-2d8316883543', 'becb4b42-0e47-43c8-953a-03fd2bf45a84', 'f4f39ba1-a613-466a-a6fa-c1109803fefa', '1a659930-6bd3-40b7-b4b6-15543aba5d8f', '968c0cb4-428e-476f-9d61-c3719acbba49', 'ff9188f2-276b-4c18-8784-d436ebfd01b7', '436d6f0f-d6c2-45a9-871e-6d1129a23cf7', 'de176a89-0b81-4cc3-9485-6aead2e0a18d', 'a50375b0-ad67-436c-96b5-1ee9fb250208', 'bca235a8-38fc-4a1b-8ff6-623081943722', '5fbcd1aa-2410-48e3-9449-3b194ac70e24', '57f6e89e-3045-40a8-a9e6-15cafa0ea54c', 'd9e7546f-1846-4761-ae7d-ef1d696f9211', '0ac5aa7d-8b1c-436e-b943-be584e111672', 'ee04eb36-89af-41c6-a0ff-6ec032c519ce', '472418de-bbd7-4b68-9bcf-0d649ac58062', '67d2e661-332a-479e-ab07-295ca9d37248', 'baf2ef28-7a49-401e-bc52-069b18996be3', 'fc84bf02-6be9-446b-8b6b-d710c889c87d', '9fa220c8-bf9d-4c48-bf4a-0bea06ad0c20', 'b841c3c9-ad1f-4440-9f90-666e39a217fa', 'b484d92f-0f22-44ed-8bd7-75ab6db2aaec', 'a34ca6a7-eaa1-466a-a8d2-718b26cfff07', '79c75edf-8b18-499e-a272-f3b8364de1a5', '063515c7-6d3e-4248-a075-62ad54532d19', 'ebfd2d90-74a8-4286-a402-44d721f903b1', '4c12f104-215b-446f-b041-8ce062ae0a40', '60c1cc74-5efc-49f7-8c10-f585d4a296e7', '6742f368-f796-45a4-8342-cfa6e21db9af', '284144e5-51fd-4abd-b62c-d127f54884c2', '70506087-2f7d-4e04-a84f-8f4996e74c36', '6685a28d-b63d-4745-bc1e-c2b592e4523b', '0f114bd8-62f5-4cd7-b155-b1e194d13dc2', 'fe6ba12d-3c02-4c5a-ac45-b696a78bd3eb', 'a8e3f632-e2d1-407c-aad8-8f636292cc1d', '2ec4ea72-ed0e-461c-992f-1e0e46ec3d5d', '4d424760-243d-492c-80eb-121859c4dd2c', '8738aa91-f7ac-437e-ba4b-1eac50db0639', '4299aaf3-3c43-4266-8739-a7acf2e663dc', '304c99cb-f7cf-471e-a7c1-26cd579fd427', '51a8d5a4-fd0c-4d36-b50a-e3d045b7a577', '0785aa97-1449-4bac-b15a-985c03058be6', '0b88ed0a-2e2a-4623-9dd1-46182d609f4e', '9507cf20-ea25-451d-9d26-1f23705d4e67', '68fe7ffa-f1f4-4896-8868-5f9151b60814', '54d4c28c-5341-4e02-96d9-8d6286ff6730', 'bf345eb6-a1c5-4ef8-b1ca-1cd0af9f8eef', '03e817b5-62e9-49f7-8dd2-16c9fbead227', '0806b9e9-b77a-404a-9db2-22b6236ad19e', '3ae21d3b-cf9a-4edd-a24c-e7510cecd372', '83c91059-4de8-4b1a-a1d8-621bc57ddc2d', '3ae94a66-bd41-4452-919e-ce0fd1a81d99', 'b8427823-15bc-4db6-aab2-f5eb635d224d', '19cc1217-c648-4f8b-8cc5-29cef85d02ae', 'f519d648-fb9e-44f8-bc35-cb0cb7b42bd7', '6b5c08ea-e550-48a1-8b9a-7b2a6080d57b', '35601b2e-be73-4288-ad1d-5aa7ea8c4a48', 'f52d449c-fb24-4266-9bb3-387d620afcb8', '7c40f931-1f8a-4ab3-b211-1665168eb3c1', '06eabb9a-f660-486e-9692-faa2cabb52bf', '78464a37-b535-456b-b177-6c1b8756b7b1', '2f2c0db1-f8d5-4ed4-a6a1-b0fb2d18535b', 'd89fd599-26e6-40ad-8bc3-0bd307ae6961', '91e528d6-e807-47c5-adb0-c16d62270add', 'e72d507e-f4e3-4612-b6a4-c1c302afdcb4', '59dd1c56-16bb-4785-8c80-a38d14a7b99b', 'f85deecd-48c9-4ec8-bfbb-9e24f07e86ef', '10dc6bd2-6bcb-4d18-8097-7f9f6d1ac93a', 'a0812fde-b8c1-48f8-81e5-aef14d8507a3', 'e7192bc9-4612-4694-af8f-fc9859854dcd', 'e1b9a071-bf38-47e0-9eef-fa4c07c2d4a4', '09a43cf6-3de6-4319-8927-2941f45fbf88', '0d040d0f-001e-4c04-a2f4-d9fba06e6edf', '5cf56326-6f17-4335-8c1b-dccef0bbc2c6', '1c35668e-86a6-4e5b-ac01-edaa362b1ca0', 'f0afcf32-b53c-4cc4-8ddd-ebbbf60bb113', 'e913496a-d9d0-4a36-9d5f-26c186d051dd', 'ab3acb0d-1e93-4f8c-915f-8ca2e1f4be54', '5ebd3814-be57-494e-b12a-9953ece6c53e', 'ef746836-17d2-40b4-9aa6-0840b4917225', 'ed0a2d24-2eb3-49b1-b439-24ddd7cd0818', 'b5b1752c-6bcf-4716-b263-1fedc757e524', '312bd97a-dc52-4fae-a6c8-c83f3856621b', 'a72e9e14-1839-4ce8-8978-5bd6d5a6fb53', 'c9fb9b31-4a57-4771-b806-d10e7edba0b2', '2bb9e43c-0d16-4ac2-8d61-461a331ea69c', 'f211f280-58e8-4efe-8959-03b98052f817', '60fb043f-d874-4012-919f-3c5d065c65fc', '69e6fc6e-7a92-45bb-8d89-a64ad4b8432a', 'ba18b12a-f0cf-4f61-b539-c942e8c601e7', 'c5194a74-9202-4e8c-b0ee-310a54fcd7d4', 'f19b567f-9fc7-4d87-8e86-b0c8e3f9dbe1', '80c28c18-0e73-4746-8d80-d079b50a581c', '54ba7ff6-864d-457f-8e72-a214b7341961', '9b66b23a-54b7-4f7a-9170-9e5b56439938', 'cb8cce15-6401-409f-ada8-8a9cfd562fa3', '42302389-1c26-44b2-8dfa-e763f7fadff7', '419ecc8a-14bf-4f5a-8353-4dcb1c8c3c90', '692e21fa-e430-4d7e-8fe7-e5f39e8111b8', 'bf2624af-7c86-4d06-aed9-ea6eb7cc4f08', '3551bafe-35c5-422e-a2c9-1b211c4c30be', 'a2fceda9-2602-4d00-af44-8a8b7591e749', '9f8149ee-9b38-44aa-b012-305054520217', '35481f68-64d3-4d2a-ad94-0dc35270059a', 'f6b3eefc-77ad-4c0d-8d4b-c19ccd0d4a26', '0596af27-c536-4449-b4af-788ce6125227', 'aa0f9b9e-fbb3-40c7-8816-327b764fe029', '380ed9ea-23f5-403b-850e-4232471246a4', 'e7afa038-13ba-4a65-9d4f-c441fdbc4751', '6d9db5f1-ddb4-497a-88db-048f65c1df15', '87876ed2-94b8-4fb1-a34a-acf4d62e4761', '28ba1e30-1bd1-4b86-9e9f-ccb85fd55c15', 'd86379eb-7371-486e-bfd3-1ddfa19aab30', 'ae7f1a9b-10e6-4c0d-934d-34132de27e6c', '7c0f064a-a4f4-4010-a39c-6e128b1a2fc9', 'ef2aa351-d7eb-47fb-9509-656aa3aa67de', '0e122c2d-4b76-4664-ac92-c62cca60a312', '8bf1816d-8764-4cbd-84b9-18f0c92e71df', '0bb4c5f8-75ed-4169-995f-cce93f0075a6', 'baed49b7-0700-484a-a1b7-bd5de2a44811', 'dda7845d-ff79-43a8-9044-6492af85b065', '5fa3d8e1-40a2-4ffc-a831-a1435ae45b66', 'fff540c1-5da2-4ae2-bf2e-65efd1f68f1e', '2161166b-9b5b-4e14-972f-efe8dce57cbc', 'e512766a-9e75-4d11-b24c-a3f3d69c97aa', '92b557eb-74e7-4d74-8cfb-9599c884de11']

#fecha pop-up
tentativa(1000, "#ngo > div.ngo-popup > div.got-it")

#encontra a lista de projetos com os respectivos códigos
lista_de_projetos = acha_lista(1000, "#ngo > div.project-list.clearfix > div")

#cria uma lista somente com os codigos encontrados                
#lista_de_codigo_elementos = define_codigo_da_lista(lista_de_projetos)

#cria uma lista somente com os codigos novos encontrados
#lista_de_codigos_novos = encontra_codigos_novos(codigo_projetos_ja_inseridos, lista_de_codigo_elementos) 

for elemento in lista_de_projetos:
    print(elemento.text + " ------------------------------ " + str(type(elemento)))

#print("------------------------------codigos_novos-----------------------------")
#print(lista_de_codigos_novos)










