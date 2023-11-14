import time
import colorama
from selenium.common.exceptions import NoSuchElementException
import tkinter as ademir
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import glob
import pandas
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
Autor: Adriano Angioletto
Data de Criação: 19 de setembro de 2023
Descrição: Boot, para o SAJ
"""


# Configuração do ChromeOptions
opcao_chrome = webdriver.ChromeOptions() # argumentos para metodo construtor
opcao_chrome.add_argument("--start-maximized")  # argumeto 2 para metodo construtor
opcao_chrome.add_argument("--disable--gpu") # necessario para rodar, o arquivo .exe se não so funcionara Visual, code bebe

class SajAdemir:  
    
    def __init__(self, chrome_opcao):  #Metodo Construtor
        bemvindo_bb = '''
            +===========================================================================+
            |             BEM VINDO,  Ao Robô, SAJ Ademir                               |
            |                                                                           |
            |                                                                           |
            |          Procuradoria Geral da Fazenda 3° Regiao                          |
            |                                                                           |
            |                                                                           |    
            |                                                                           |
            | Devs:  AdrianoAngioletto                                                  |
            +===========================================================================+
            '''
        print(bemvindo_bb)
                
        self.chrome_opcao = chrome_opcao
        self.google = webdriver.Chrome(options=chrome_opcao) # recebe argumento, bebe!
        #   self.saj_pge = SjPge() FUTURA MENTE IR BUSCAR OS DADOS LÁ DO PGE!! JA DEIXEI AQUI NO JEITO AMOR!
    
                 

    def InicioSAJ(self): # FUNÇÃO PAPAI 
        arquivo_excel = "PROCESSOS TRABALHISTAS - NAJ - GREF _ PRFN3 Regiao.xlsx"     
        if not os.path.isfile(arquivo_excel):   # VERIFICA, SE O ARQUIVO DO PROCESSOS, EXISTE SE EXISTIR DA CONTINUIDADE SE NÃO FECHA O PROGRAMA
            print(colorama.Fore.WHITE + "PROCESSOS NÃO ENCONTRADOS, POR FAVOR COLOQUE OS PROCESSOS NA PASTA")
            return 
        self.google.get("https://saj.pgfn.fazenda.gov.br/saj/login.jsf?dswid=3754") # chama o site
        time.sleep(2)
        # alerta = 'alert("ROBÔ SAJ_ADEMIR > LOGUE COM TOKEN, OU CPF, VOCÊ TEM 30 SEGUNDOS PARA LOGAR, APÓS ISSO CLICAREMOS, EM ENTRAR, PARA FUNCIONAMENTO CORRETO, DEIXE CLICAR SOZINHO");' # aqui ja ta explicado
        # self.google.execute_script(alerta) # executa o script
        campo_login = self.google.find_element(By.ID, "frmLogin:username")
        campo_senha = self.google.find_element(By.ID, "frmLogin:password")
        campo_login.send_keys("")
        campo_senha.send_keys("")
        botao_ok = self.google.find_element(By.ID, "frmLogin:entrar")
        time.sleep(2) 
        botao_ok.click()
        time.sleep(3)
              
    def SegundoPassoSaj(self): # é a segunda parte do codigo, onde ele clica e Consulta os Processos
    
        print('Estamos Carregando, a Segunda Parte do código, para Clicar nos Processos, e Consultar')  
        botao_processo = self.google.find_element(By.CLASS_NAME, "ui-menuitem-text")  # PEGA  ID DA LISTA > PROCESSO
        webdriver.ActionChains(self.google).move_to_element(botao_processo).perform() # MOVE MOUSE ATÉ A LISTA 
        time.sleep(1) # TEMPO NECESSARIO
        botao_consulta = self.google.find_element(By.ID, "j_idt15:formMenus:menuPerfilConsulta") # PEGA O ITEM DA LISTA >>> CONSULTA
        time.sleep(1) 
        botao_consulta.click() # CLICA NO ITEM >>> CONSULTA
        time.sleep(1) # TEMPO PARA RETONAR O PROCESSO.

    def ConsultarProcessos(self):
    
        ListaProcessos = glob.glob('PROCESSOS TRABALHISTAS - NAJ - GREF _ PRFN3 Regiao*.xlsx')
    
        arquivo_html_todos_processos = "todos_processos.html"

        with open(arquivo_html_todos_processos, "w", encoding="utf-8") as arquivo_todos_processos:
            for arquivo_excel in ListaProcessos:
            # Leia o arquivo Excel e armazene-o em um DataFrame
                dados_temporarios = pandas.read_excel(arquivo_excel)

            for valor in dados_temporarios['NÚMERO DO PROCESSO CNJ']:
                print(f'Robô Saj Ademir Acabou de ler e salvar o Processo Numero: {valor}')

                caixa_consulta = self.google.find_element(By.ID, "consultarProcessoForm:numeroProcesso")
                time.sleep(1)
                caixa_consulta.clear()  
                caixa_consulta.send_keys(str(valor))
                
               
                botao_consulta = self.google.find_element(By.ID, "consultarProcessoForm:consultarProcessos")
                time.sleep(1)
                botao_consulta.click()
                time.sleep(1)
                
               
                mensagem_erro = self.google.find_elements(By.CLASS_NAME, 'ui-messages-fatal')
                # mensagem_ato_judicial = self.google.find_elements(By.ID, 'frmDetalhar:j_idt104:0:fieldAto')
                
               
                if not mensagem_erro:
                    
                    try:
                        elemento = self.google.find_element(By.ID, 'frmDetalhar:j_idt104:0:fieldInscricoes')
                    except NoSuchElementException:
                        print(f'Processo Diferenciado Numero: {valor} Verifique no Arquivo LOG, da pasta')
                        with open("Processos_Diferenciados.txt", "a") as arquivo_erro:
                            arquivo_erro.write(f'Processo Diferenciado Numero:  {valor} Verifique Manualmente \n')
                        botao_processo = self.google.find_element(By.CLASS_NAME, "ui-menuitem-text")  # PEGA  ID DA LISTA > PROCESSO
                        webdriver.ActionChains(self.google).move_to_element(botao_processo).perform() # MOVE MOUSE ATÉ A LISTA 
                        time.sleep(1) # TEMPO NECESSARIO
                        botao_consulta = self.google.find_element(By.ID, "j_idt15:formMenus:menuPerfilConsulta") # PEGA O ITEM DA LISTA >>> CONSULTA
                        time.sleep(1) 
                        botao_consulta.click() # CLICA NO ITEM >>> CONSULTA
                        time.sleep(1)
                        
                        continue
    
                                      
                    html_tabela = elemento.get_attribute("innerHTML")

                    
                    arquivo_todos_processos.write(f'<h2>Processo Numero: {valor}</h2>\n')
                    arquivo_todos_processos.write(html_tabela)
                    arquivo_todos_processos.write('\n')
                    
                    # Restante do código para voltar à tela inicial e iniciar uma nova consulta
                    botao_processo = self.google.find_element(By.CLASS_NAME, "ui-menuitem-text")  # PEGA  ID DA LISTA > PROCESSO
                    webdriver.ActionChains(self.google).move_to_element(botao_processo).perform() # MOVE MOUSE ATÉ A LISTA 
                    time.sleep(1) # TEMPO NECESSARIO
                    botao_consulta = self.google.find_element(By.ID, "j_idt15:formMenus:menuPerfilConsulta") # PEGA O ITEM DA LISTA >>> CONSULTA
                    time.sleep(1) 
                    botao_consulta.click() # CLICA NO ITEM >>> CONSULTA
                    time.sleep(1) 
                else:
                    print(f'AVISO DE ERRO: Alguem não salvou corretamente o Numero de Processo {valor}')
                    time.sleep(1)
                    botao_okay = self.google.find_element(By.ID, "j_idt220:btn")
                    time.sleep(1)
                    botao_okay.click()
                   
                    with open("processos_nao_encontrados.txt", "a") as arquivo_erro:
                        arquivo_erro.write(f'Processo Numero: {valor} não encontrado\n')
                    
                    botao_processo = self.google.find_element(By.CLASS_NAME, "ui-menuitem-text")  # PEGA  ID DA LISTA > PROCESSO
                    webdriver.ActionChains(self.google).move_to_element(botao_processo).perform() # MOVE MOUSE ATÉ A LISTA 
                    time.sleep(1) # TEMPO NECESSARIO
                    botao_consulta = self.google.find_element(By.ID, "j_idt15:formMenus:menuPerfilConsulta") # PEGA O ITEM DA LISTA >>> CONSULTA
                    time.sleep(1) 
                    botao_consulta.click() # CLICA NO ITEM >>> CONSULTA
                    time.sleep(1)


   
Sj = SajAdemir(opcao_chrome)
Sj.InicioSAJ() #  dá inicio a função
Sj.SegundoPassoSaj() # chama a segunda e dai por diante.
Sj.ConsultarProcessos()


#SOLUÇÃO EXCEL 

# def ConsultarProcessos(self): 
#     # Encontre todos os arquivos Excel que correspondem ao padrão
#         ListaProcessos = glob.glob('processos*.xlsx')
        
#         for arquivo_excel in ListaProcessos:
#             # Crie uma pasta para salvar os resultados deste arquivo Excel
#             nome_da_pasta = os.path.splitext(arquivo_excel)[0]  # Remova a extensão do arquivo
#             os.makedirs(nome_da_pasta, exist_ok=True)
            
#             df_todos_os_processos = pandas.DataFrame()    
#             # Leia o arquivo Excel e armazene-o em um DataFrame
#             dados_temporarios = pandas.read_excel(arquivo_excel)

#             for index, row in dados_temporarios.iterrows():
#                 valor = row.iloc[0]  # Supondo que o número do processo está na primeira coluna do DataFrame               
#                 print(f'Robô Saj Ademir Acabou de ler e salvar o Processo Numero: {valor}')          
#                 caixa_consulta = self.google.find_element(By.ID, "consultarProcessoForm:numeroProcesso")
#                 time.sleep(1)
#                 # Insira o número do processo
#                 caixa_consulta.send_keys(valor)
#                 # Execute a pesquisa clicando no botão "Consultar"
#                 botao_consulta = self.google.find_element(By.ID, "consultarProcessoForm:consultarProcessos")
#                 time.sleep(1)
#                 botao_consulta.click()
#                 time.sleep(1)
#                 # Localize o elemento pelo ID
#                 elemento = self.google.find_element(By.ID, 'frmDetalhar:j_idt104:0:fieldInscricoes')               
#                 # Extraia o texto do elemento
#                 texto_do_elemento = elemento.text#.replace("\n")   
                
#                 remover = ["DIV.ATIVA-IRPJ", "DIV.ATIVA-", "\n", "INSCRIÇÕES SIDA", "APA", 
#                            "DESCRIÇÃO DA RECEITA", "PROCESSO ADMINISTRATIVO", 
#                            "VALOR INICIAL DE AJUIZAMENTO", "DATAVALOR", "ATUALIZADO", 
#                            "SITUAÇÃO DA INSCRIÇÃO", "DATA", "Inscrições", "Carregando ...", 
#                            "R$", "//", "-", ",", ".//", "..", "Não foram localizadas informações de inscrições com falha.",
#                            "Informações atualizadas no momento da consulta (fonte: SIDA).", "INSCRIÇÃO COM FALHA",
#                            "DIV ATIVA-SIMPLES NACIONAL", "DIV.ATIVA-PIS", "DIV.ATIVA-CONTRIBUICAO SOCIAL", "DIV.ATIVA-IRPJ",
#                            "DIV.ATIVA-IRPJ FONTE", "DIV.ATIVA-IPI", "DIV.ATIVA-COFINS"]


#                 # Substitua as palavras a serem removidas por uma string vazia
#                 for palavra in remover:
#                     texto_do_elemento = texto_do_elemento.replace(palavra, "")

#                 # Separe números e letras
#                 numeros = re.findall(r'\d+', texto_do_elemento)  # Encontra todos os números
#                 texto_do_elemento = re.sub(r'\d+', '', texto_do_elemento)  # Remove os números

#                 print("Números:", numeros)
#                 print("Texto restante:", texto_do_elemento)

#                 # Crie um DataFrame com as colunas 'Processo', 'Numeros' e 'Texto'
#                 df_temporario = pandas.DataFrame({'Processo': [valor], 'Numeros': [' '.join(numeros)], 'Situacao': [texto_do_elemento]})
#                 df_todos_os_processos = pandas.concat([df_todos_os_processos, df_temporario], ignore_index=True)

#                 caminho_arquivo_resultado = os.path.join(nome_da_pasta, 'Todos_Processos.csv')

#                 # Salve o DataFrame em um arquivo CSV com ponto e vírgula como delimitador
#                 df_todos_os_processos.to_csv(caminho_arquivo_resultado, sep=';', index=False)
#                 botao_processo = self.google.find_element(By.CLASS_NAME, "ui-menuitem-text")  # PEGA  ID DA LISTA > PROCESSO
#                 webdriver.ActionChains(self.google).move_to_element(botao_processo).perform() # MOVE MOUSE ATÉ A LISTA 
#                 time.sleep(1) # TEMPO NECESSARIO
#                 botao_consulta = self.google.find_element(By.ID, "j_idt15:formMenus:menuPerfilConsulta") # PEGA O ITEM DA LISTA >>> CONSULTA
#                 time.sleep(1) 
#                 botao_consulta.click() # CLICA NO ITEM >>> CONSULTA
#                 time.sleep(1) 