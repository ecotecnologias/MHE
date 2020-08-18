# -*- coding: latin_1 -*-

import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
    
from os import path, listdir
from tkMessageBox import showinfo, showerror
from tkFileDialog import askopenfile, askdirectory
from Hydrolib import calcular_TC_Kirpich

#----------------------------------------------------------------------
def progressBar(n, nmax):
    """"""
    #   proporcoes
    progresso = int((float(n+1)/(nmax))*50)
    faltante = 50 - progresso
    #   inicio
    b = "\t|"
    #   progresso
    for i in xrange(progresso):
        b += "#"
    #   faltante
    for i2 in xrange(faltante):
        b += " "
    #   fim
    if not  progresso == 50:
        b += "|"
    else:
        b += "|\n"
    #   escreva barra
    sys.stdout.write(b + "\r")
#----------------------------------------------------------------------
def gerenciarLeitura(diretorio_do_software):
    """"""
    #   Abra o arquivo... Se 'diretorio_arquivo_entrada' == None, o arquivo nao e' txt.
    diretorio_arquivo_entrada = procurarArquivo(diretorio_do_software)
    
    #   Se um diretorio foi detectado, e' um arquivo txt.
    if not diretorio_arquivo_entrada == None:
        #   Selecionar extensao
        extensao_arquivo = diretorio_arquivo_entrada.split("/")[-1].split(".")[-1]
        
        #   Verificar se um arquivo txt foi selecionado
        if (extensao_arquivo == "txt") or (extensao_arquivo == "TXT") or (extensao_arquivo == "hyd") or (extensao_arquivo == "HYD"):
            #   Faca o teste de integridade do arquivo, isto vou deixar para depois.
            integridade = checarIntegridadeEntrada(diretorio_arquivo_entrada)
        
            #   Se o arquivo for integro (nao possuir erros), continue
            if integridade == True:
                #   Armazenar o diretorio de saida
                diretorio_saida = path.dirname(diretorio_arquivo_entrada)
                #   Retorne o diretorio
                return [diretorio_arquivo_entrada], diretorio_saida
            #   Arquivo ruim
            else:
                print "\n\tArquivo de entrada com problemas. Cheque seu arquivo de entrada.\n"
                return [None], None
        #   Formato incorreto
        else:
            print "\n\tExtensao do arquivo de entrada e' incompativel.\n"
            showerror("Erro", "A extensão do arquivo de entrada é incompatível.\nSelecione um arquivo *.txt ou *.hyd.")
            return [None], None
    #   Se NAO for dado um arquivo de entrada
    else:
        print "\n\tNenhum arquivo selecionado.\n"
        showinfo("Atenção", "Nenhum arquivo selecionado. Tente novamente.")
        return [None], None
#----------------------------------------------------------------------
def procurarArquivo(diretorio_do_software):
    """Abre a janela para procurar um arquivo de entrada"""
    #   Iniciar nova janela
    root4 = Tk()
    root4.withdraw()
    entrada = askopenfile(mode = 'r', title = "Selecione o arquivo de entrada", initialdir = diretorio_do_software)
    root4.destroy()
    
    #    verificar se algo foi selecionado
    if (not entrada == None):
        #   Armazenar nome
        diretorio_arquivo_entrada = entrada.name
        #   Fechar aquivo
        entrada.close()
        #   Retornar informacao relevante
        return diretorio_arquivo_entrada.encode()
    #   Nada foi selecionado
    else:
        return None
#----------------------------------------------------------------------
def gerenciarLeituraPasta(diretorio_do_software):
    """"""
    #   Abra o arquivo... Se 'diretorio_arquivo_entrada' == None, o arquivo nao e' txt.
    diretorio_pasta_entrada = procurarPasta(diretorio_do_software)
    
    #   Se um diretorio foi detectado, e' um arquivo txt.
    if not diretorio_pasta_entrada == None:
        #   Listar os arquivos presentes nesta pasta... Nome.extensao
        arquivos_da_pasta = listdir(diretorio_pasta_entrada) 
        #   Variavel Auxiliar
        arquivos_deletados = 0
        #   Loop para tirar os arquivos de saida (ohy) dos diretorios de entrada
        for numero_arquivo in xrange(len(arquivos_da_pasta)):
            #   Selecionar extensao
            extensao_arquivo = arquivos_da_pasta[numero_arquivo - arquivos_deletados].split(".")[-1]
            #   Testar extensao
            if (not extensao_arquivo == "hyd") and (not extensao_arquivo == "HYD") and (not extensao_arquivo == "txt") and (not extensao_arquivo == "TXT"):
                #   Delete o arquivo da lista
                del arquivos_da_pasta[numero_arquivo - arquivos_deletados]
                #   Somar um...
                arquivos_deletados += 1
        
        #   Se nao sobrou nenhum arquivo na lista, e' porque nenhum deles e' valido
        if len(arquivos_da_pasta) == 0:
            print "\n\tNenhum dos arquivos da pasta possui o formato valido.\n"
            showinfo("Atenção", "Nenhum dos arquivos da pasta selecionada possui a extenção adequada.\n\nNenhuma pasta selecionada. Tente novamente")
            return None, None
        
        #   Loop principal... de arquivo em arquivo
        for numero_arquivo in xrange(len(arquivos_da_pasta)):
            #   Especificar arquivo
            diretorio_arquivo_entrada = (diretorio_pasta_entrada + "/" + arquivos_da_pasta[numero_arquivo])
            #   Selecionar extensao
            extensao_arquivo = arquivos_da_pasta[numero_arquivo].split(".")[-1]
        
            #   Verificar se um arquivo txt foi selecionado
            if (extensao_arquivo == "txt") or (extensao_arquivo == "TXT") or (extensao_arquivo == "hyd") or (extensao_arquivo == "HYD"):
                #   Faca o teste de integridade do arquivo, isto vou deixar para depois.
                integridade = checarIntegridadeEntrada(diretorio_arquivo_entrada)
            
                #   Se o arquivo for integro (nao possuir erros), continue
                if integridade == True:
                    #   Testar se e' o ultimo loop
                    if numero_arquivo == (len(arquivos_da_pasta))-1:
                        #   Retorne o diretorio
                        return diretorio_pasta_entrada, arquivos_da_pasta
                #   Arquivo ruim
                else:
                    print "\n\tArquivo '%s' com problemas.\n\tCheque seu arquivo de entrada.\n" %(arquivos_da_pasta[numero_arquivo])
                    return None, None
            #   Formato incorreto
            else:
                print "\n\tA extensao do arquivo '%s' e' incompativel.\n" %(arquivos_da_pasta[numero_arquivo])
                showerror("Erro", "A extensão do arquivo '%s' é incompatível.\nSelecione um arquivo *.txt ou *.hyd." %(arquivos_da_pasta[numero_arquivo]))
                return None, None
    #   Se NAO for dado um arquivo de entrada
    else:
        print "\n\tNenhuma pasta selecionada.\n"
        showinfo("Atenção", "Nenhuma pasta selecionada. Tente novamente")
        return None, None
#----------------------------------------------------------------------
def procurarPasta(diretorio_do_software):
    """Abre a janela para procurar uma pasta com arquivos de entrada"""
    #   Iniciar nova janela
    root4 = Tk()
    root4.withdraw()
    pasta = askdirectory(initialdir = diretorio_do_software)
    root4.destroy()
    
    #    verificar se algo foi selecionado
    if (not pasta == '') and (not pasta == None):
        #   Armazenar nome
        diretorio_pasta_entrada = pasta.encode()
       #   Testar se o diretorio e' valido, remocao de erros basicamente
        if (path.isdir(diretorio_pasta_entrada) == True):
            #   Retornar informacao relevante
            return diretorio_pasta_entrada
        #   Diretorio nao existe
        else:
            #   Avisa duas vezes
            showerror("Erro", "A pasta selecionada ('%s') não existente." %(diretorio_pasta_entrada))
            return None
    #   Nada foi selecionado
    else:
        return None
#----------------------------------------------------------------------
def checarIntegridadeEntrada(diretorio_arquivo_entrada):
    """Testa o conteudo do arquivo de entrada em busca de erros."""
    #   Avisar que estamos testando
    print "\n\tExaminando o arquivo: %s" %(diretorio_arquivo_entrada.split("/")[-1])
    #   Contar numero de linhas
    numero_linhas = contarLinhas(diretorio_arquivo_entrada)
    linhas_lidas = 0
    
    #   Declarar auxiliares
    linhas_comentario = 0
    nch = 0
    nop = 0
    nblocos = 0
    numero_intervalos_tempo = 0
    numero_intervalos_tempo_chuva = 0
    numero_estruturas_puls = 0
    nch_declaradas = 0
    nop_declaradas = 0
    lista_repeticao = []
    
    #   Abrir arquivo de entrada
    arquivo_entrada = open(diretorio_arquivo_entrada, 'r')
    
    #   Ler arquivo de entrada ate' pegar inicio
    conteudo_linha = arquivo_entrada.readline().split(";")
    linhas_lidas += 1
    
    #   Desconsiderar comentario
    while (not conteudo_linha[0] == "INICIO"):
        #   Cuidar se existe a palavra "INICIO" no arquivo de entrada
        if linhas_comentario < numero_linhas:
            #   Ler arquivo de entrada ate' pegar inicio
            conteudo_linha = arquivo_entrada.readline().split(";")
            linhas_lidas += 1
            #   Acrescer comentario
            linhas_comentario += 1
        #   Nao ha' a palavra "INICIO"
        else:
            #   Avise o usuario
            arquivo_entrada.close(); showerror("Erro no arquivo de entrada", "Não foi detectado a palavra 'INICIO' no arquivo de entrada.\n\nCertifique-se de que a palavra esteja presente no arquivo de entrada para que o modelo inicie o processo de leitura do mesmo."); return False
    
    #   Testar tamanho da linha
    if not len(conteudo_linha) == 7:
        #   Avise o usuario
        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes. Verifique o arquivo de entrada.\n\nDica: Não se esqueça dos ponto-e-vírgula (;) após cada dado (inclusive o último de cada linha)."); return False
    
    #   Leu inicio, teste informacoes gerais
    try: int(conteudo_linha[1]) #numero_intervalos_tempo
    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de intervalos de tempo da simulação deve ser um número inteiro."); return False
    
    try: int(conteudo_linha[2]) #duracao_intervalo_tempo
    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A duração do intervalo de tempo deve ser um número inteiro."); return False
    
    try: int(conteudo_linha[3]) #numero_chuvas
    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de chuvas da simulação deve ser um número inteiro."); return False
    
    try: int(conteudo_linha[4]) #numero_intervalos_tempo_chuva
    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de intervalos de tempo das chuvas deve ser um número inteiro."); return False
    
    try: int(conteudo_linha[5]) #numero_operacoes_hidrologicas
    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de operações hidrológicas deve ser um número inteiro."); return False

    #   Se o nint_tempo_chuva > nint_tempo, ta errado
    if int(conteudo_linha[4]) > int(conteudo_linha[1]):
        #   Avise o usuario
        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de intervalos da simulação deve ser maior ou igual ao número de intervalos de tempo com chuva."); return False
        
    #   Armazenar os valores
    numero_intervalos_tempo = int(conteudo_linha[1]) 
    numero_intervalos_tempo_chuva = int(conteudo_linha[4])
    nch_declaradas = int(conteudo_linha[3])
    nop_declaradas = int(conteudo_linha[5])
    entrada_operacoes = [0 for i in xrange(nop_declaradas)]
    
    #   Nao pode ser zero
    if int(conteudo_linha[1]) == 0:
        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de intervalos de tempo da simulação não pode ser zero."); return False
    if int(conteudo_linha[2]) == 0:
        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A duração do intervalo de tempoo da simulação não pode ser zero"); return False
    #if int(conteudo_linha[3]) == 0:
    #    arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de chuvas da simulação não pode ser zero"); return False
    if int(conteudo_linha[4]) == 0:
        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de intervalos de tempo das chuvas não pode ser zero"); return False
    if int(conteudo_linha[5]) == 0:
        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de operações hidrológicas da simulação não pode ser zero"); return False
        
    #   Ver quantos blocos de leitura
    nblocos = int(conteudo_linha[3]) + int(conteudo_linha[5])
    
    #   Loop para ler o restante:
    for bloco in xrange(nblocos):
        #   Ler a linha
        conteudo_linha = arquivo_entrada.readline().split(";")
        linhas_lidas += 1
        #   Testar conteudo
        #   Se for chuva
        if conteudo_linha[0] == "CHUVA":
            #   Testar tamanho da linha
            if len(conteudo_linha) < 3:
                #   Avise o usuario
                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes para a chuva %d.\n\nExemplo:'CHUVA; 1;'" %(nch+1)); return False
        
            #   Testar o numero dela
            try: int(conteudo_linha[1]) #numero da chuva
            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da chuva deve ser inteiro."); return False
            
            #   Testar o numero dela
            if (int(conteudo_linha[1]) == (nch+1)):
                #   Ler a linha
                conteudo_linha = arquivo_entrada.readline().split(";")
                linhas_lidas += 1
                #   Testar se e' IDF ou OBS
                if conteudo_linha[0] == "IDF":
                    #   Testar tamanho da linha
                    if len(conteudo_linha) < 10:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes para a chuva %d.\n\nExemplo: 'IDF; 1; 0.5; 10; 823.4; 10.2; 1.42; 0.79; 0;'" %(nch+1)); return False
                        
                    #   TEstar valores das linhas
                    try: int(conteudo_linha[1]) #tipo IDF
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O tipo da IDF deve ser um número inteiro."); return False
                    
                    try: float(conteudo_linha[2]) #posicao do pico
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A posição do pico da chuva deve ser um número decimal."); return False
                    
                    try: int(conteudo_linha[3]) #tempo de retorno
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O tempo de retorno deve ser um número inteiro."); return False
                    
                    try: float(conteudo_linha[4]) #parametro a
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro A da IDF deve ser um número decimal."); return False
                    
                    try: float(conteudo_linha[5]) #parametro b
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro B da IDF deve ser um número decimal."); return False
                    
                    try: float(conteudo_linha[6]) #parametro c
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro C da IDF deve ser um número decimal."); return False
                    
                    try: float(conteudo_linha[7]) #parametro d
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro D da IDF deve ser um número decimal."); return False
                    
                    try: int(conteudo_linha[8]) #limitante
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O limite de intensidade de chuva dos primeiros intervalos de tempo deve ser um número inteiro.\n\nDica: Para desativar o limitante de intensidade da chuva dos primeiros intervalos de tempo utilize zero."); return False
                    
                    #   Nao pode ser zero
                    if not int(conteudo_linha[1]) == 1:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Tipo da IDF '%s' desconhecido.\nTipo(s) conhecido(s): 1" %(conteudo_linha[1])); return False
                    if (float(conteudo_linha[2]) < 0) or (float(conteudo_linha[2]) > 1):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O valor da posição do pico deve ser maior ou igual a 0 e menor ou igual a 1."); return False
                    if int(conteudo_linha[3]) == 0:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O tempo de retorno não pode ser zero."); return False
                    if float(conteudo_linha[4]) <= 0.0:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro A da IDF não pode ser zero."); return False
                    if float(conteudo_linha[5]) <= 0.0:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro B da IDF não pode ser zero."); return False
                    if float(conteudo_linha[6]) <= 0.0:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro C da IDF não pode ser zero."); return False
                    if float(conteudo_linha[7]) <= 0.0:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O parâmetro D da IDF não pode ser zero."); return False
                    if int(conteudo_linha[8]) < 0:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O limite de intensidade de chuva dos primeiros intervalos de tempo (em minutos) não pode ser negativo."); return False

                    #   Deu tudo certo, some uma chuva
                    nch += 1
                    
                #   Se for chuva observada
                elif conteudo_linha[0] == "OBS":
                    #   Testar tamanho da linha
                    if not len(conteudo_linha) == 3:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas), "Informações insuficientes para a chuva %d.\n\nExemplo:'CHUVA; 1;'" %(nch+1)); return False
                        
                    #   Substituir a \ por /
                    conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                    #   Tirar os espacos em branco do diretorio informado, se houver
                    while conteudo_linha[1][0] == " ":
                        conteudo_linha[1] = conteudo_linha[1][1:]
                        
                    #   Verificar se o arquivo existe
                    if (path.isfile(conteudo_linha[1]) == True):
                        #   Selecionar ultimo nome
                        extensao_arquivo = conteudo_linha[1].split("/")
                        #   Selecionar extensao
                        extensao_arquivo = extensao_arquivo[-1].split(".")[-1]
                        
                        #   Verificar se a extensao dele e' txt
                        if ((not extensao_arquivo == "txt") or (not extensao_arquivo == "TXT")):
                            #   Testar o arquivo de entrada
                            integridade_arquivo, linha = checarIntegridadeArquivoTexto(conteudo_linha[1], numero_intervalos_tempo_chuva)
                            
                            #   Se deu bom
                            if integridade_arquivo == True:
                                #   Some uma chuva
                                nch += 1
                            
                            else: #   Deu ruim
                                #   Que ruim que deu?
                                if linha == 0: #    Numero de dados incorretos
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","O arquivo fornecido para a chuva %d não possui %d linhas (que é o número de intervalos de tempo com chuva da simulação)." %((nch+1), numero_intervalos_tempo_chuva)); return False
                                
                                else: # Linha X e' o problema
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","Erro na linha %d.\n\nO arquivo fornecido para a chuva %d não obedece os padrões utilizados pelo programa.\n\nDica: As linhas devem possuir o seguinte padrão: 'valor do dado;'." %(linha, (nch+1))); return False
                        
                        else: # nao e' txt
                            #   Avise o usuario
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A extensão do arquivo fornecido para a chuva %d deve ser txt." %(nch+1)); return False
                        
                    else: #   Arquivo nao encontrado
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O arquivo fornecido para a chuva %d não foi localizado." %(nch+1)); return False
                    
                else: #   Tipo de chuva incorreto
                    #   Avise o usuario
                    arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas), "Tipo de chuva '%s' não definido.\n\nTipos definidos: 'IDF' ou 'OBS'." %(conteudo_linha[0])); return False
                    
            else: #   Numero incorreto
                #   Avise o usuario
                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Número da chuva incorreto.\nNúmero esperado: %d" %(nch+1)); return False
        
        #   Se for operacao
        elif conteudo_linha[0] == "OPERACAO":
            #   Teste o tipo de operacao
            #   Testar tamanho da linha
            if len(conteudo_linha) < 3:
                #   Avise o usuario
                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes para a operação %d.\n\nExemplo:'OPERACAO; 1;'" %(nop+1)); return False
        
            #   Testar o numero dela
            try: int(conteudo_linha[1]) #numero da operacao
            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da operação hidrológica deve ser inteiro."); return False
            
            #   Testar o numero dela
            if (int(conteudo_linha[1]) == (nop+1)):
                #   Ler a linha
                conteudo_linha = arquivo_entrada.readline().split(";")
                linhas_lidas += 1
                
                #   Testar se e' PQ
                if conteudo_linha[0] == "PQ":
                    #   Testar tamanho da linha
                    if not len(conteudo_linha) == 3:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes na operação %d (chuva-vazão)." %(nop+1)); return False
                    
                    #   Numero da chuva correspondente
                    try: int(conteudo_linha[1]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da chuva utilizada nas operações hidrológicas de chuva-vazão deve ser inteiro."); return False
                    
                    #   Checar se o numero da chuva e' possivel de ser encontrada no arquivo de entrada
                    if int(conteudo_linha[1]) > nch_declaradas:
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Não é possível utilizar a chuva número %d na operação %d pois há apenas %d chuvas declaradas nas informações gerais." %((int(conteudo_linha[1])),(nop+1),(nch_declaradas))); return False
                    
                    #   Ler a linha
                    conteudo_linha = arquivo_entrada.readline().split(";")
                    linhas_lidas += 1
                    
                    #   Testar tamanho da linha
                    if not len(conteudo_linha) == 3:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes ao fornecer o coeficiente CN.\n\nExemplo: 'CN; 83;'"); return False
                    
                    #   Espera-se um CN
                    if not conteudo_linha[0] == "CN":
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Estrutura da linha incorreta ao inserir o coeficiente CN.\n\nExemplo: 'CN; 75;'"); return False
                        
                    #   COeficiente CN
                    try: float(conteudo_linha[1]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente CN deve ser um número decimal."); return False
                        
                    #   Testar seu valor
                    if (float(conteudo_linha[1]) <= 0.0) or (float(conteudo_linha[1]) > 100.0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O valor de CN deve ser maior que zero e menor ou igual a 100."); return False
                        
                    #   Ler a linha
                    conteudo_linha = arquivo_entrada.readline().split(";")
                    linhas_lidas += 1
                    
                    #   Testar tamanho da linha
                    if len(conteudo_linha) < 3:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes de propagação de escoamento\n\nExemplo: 'HUT; 43.3; 1.73;' ou 'HUT; 43.3; KIRPICH; 40.2; 10.2;'"); return False
                        
                    #   Espera-se um HUT
                    if not conteudo_linha[0] == "HUT":
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Estrutura da linha incorreta ao inserir as informações de propagação de escoamento.\n\nExemplo: 'HUT; 43.3; 1.73;' ou 'HUT; 43.3; KIRPICH; 40.2; 10.2;'"); return False
                    
                    #   Area
                    try: float(conteudo_linha[1]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O valor da área da bacia deve ser decimal."); return False
                    
                    #   Testar seu valor
                    if (float(conteudo_linha[1]) <= 0.0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O valor da área da bacia deve ser maior que zero."); return False
                        
                    #   Testar TC
                    #if conteudo_linha[2] == "KIRPICH":
                    if "KIRPICH" in conteudo_linha[2]:
                        #   Diferenca cota
                        try: float(conteudo_linha[3]) 
                        except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A diferença de cota da bacia (m) deve ser um número decimal."); return False
                        #   Comprimento canal
                        try: float(conteudo_linha[4])
                        except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O comprimento do canal (km) deve ser um número decimal."); return False
                        
                        #   Testar seu valor
                        if (float(conteudo_linha[3]) <= 0.0):
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A diferença de cota da bacia deve ser maior que zero."); return False
                        #   Testar seu valor
                        if (float(conteudo_linha[4]) <= 0.0):
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O comprimento do canal deve ser maior que zero."); return False
                        
                    else:   #   E' o valor em hora
                        try: float(conteudo_linha[2]) #numero da chuva correspondente
                        except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O valor do tempo de concentração deve ser um número decimal."); return False
                        
                        #   Testar seu valor
                        if (float(conteudo_linha[2]) <= 0.0):
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O valor do tempo de concentração deve ser um maior que zero."); return False
                    
                    #   Dizer que ela nao precisa da saida de outra operacao, ou seja, 0
                    entrada_operacoes[nop] = 0
                    
                    #   Somar uma op
                    nop += 1
                    
                #   Testar se e' PULS
                elif conteudo_linha[0] == "PULS":
                    #   Testar tamanho da linha
                    if not len(conteudo_linha) == 5:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes para operação %d (propagação de reservatórios de Puls)." %(nop+1)); return False
                    
                    #   Substituir a \ por /
                    conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                    #   Tirar os espacos em branco do diretorio informado, se houver
                    while conteudo_linha[1][0] == " ":
                        conteudo_linha[1] = conteudo_linha[1][1:]
                    
                    #   hidrograma de entrada
                    #   Verificar se o arquivo existe
                    if (path.isfile(conteudo_linha[1]) == True):
                        #   Selecionar ultimo nome
                        extensao_arquivo = conteudo_linha[1].split("/")
                        #   Selecionar extensao
                        extensao_arquivo = extensao_arquivo[-1].split(".")[-1]
                        
                        #   Verificar se a extensao dele e' txt
                        if ((not extensao_arquivo == "txt") or (not extensao_arquivo == "TXT")):
                            #   Testar o arquivo de entrada
                            integridade_arquivo, linha = checarIntegridadeArquivoTexto(conteudo_linha[1], numero_intervalos_tempo)
                            
                            #   Dizer ao programa que essa operacao nao precisa da saida de outra
                            entrada_operacoes[nop] = 0
                            
                            #   Se deu bom
                            if integridade_arquivo == False:
                                #   Que ruim que deu?
                                if linha == 0: #    Numero de dados incorretos
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","O arquivo fornecido para o hidrograma de entrada não possui %d linhas (que é o número de intervalos de tempo de simulação)." %(numero_intervalos_tempo)); return False
                                
                                else: # Linha X e' o problema
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","Erro na linha %d.\n\nO arquivo fornecido para o hidrograma de entrada não obedece os padrões utilizados pelo programa.\n\nDica: As linhas devem possuir o seguinte padrão: 'valor do dado;'." %(linha)); return False
                        
                        else: # nao e' txt
                            #   Avise o usuario
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A extensão do arquivo fornecido para o hidrograma de entrada para a operação de Puls deve ser txt."); return False
                        
                    else: #   Nao e' path, teste numero
                        try: int(conteudo_linha[1]) 
                        except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da operação que originará o hidrograma de entrada deve ser inteiro."); return False
                        
                        #   Testar seu valor
                        if (int(conteudo_linha[1]) <= 0):
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da operação que originará o hidrograma de entrada deve ser maior que zero."); return False
                            
                        #   Checar se o numero do hidrograma de entrada e' possivel de ser encontrado no arquivo de entrada
                        if int(conteudo_linha[1]) > nop_declaradas:
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Não é possível utilizar o hidrograma oriundo da operação número %d na operação %d pois há apenas %d operações hidrológicas declaradas nas informações gerais." %((int(conteudo_linha[1])),(nop+1),(nop_declaradas))); return False
                    
                        #   Dizer ao software que essa operacao precisa da saida de outra
                        entrada_operacoes[nop] = int(conteudo_linha[1])
                    
                    #   Cota inicial
                    try: float(conteudo_linha[2]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota inicial do reservatório deve ser um número decimal."); return False
                    
                    #   Testar seu valor
                    if (int(conteudo_linha[2]) < 0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota inicial do reservatório não pode ser negativa."); return False
                    
                    #   Numero Estruturas
                    try: int(conteudo_linha[3]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de estruturas de extravasão deve ser um número inteiro."); return False
                    
                    #   Testar seu valor
                    if (int(conteudo_linha[3]) <= 0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número de estruturas de extravasão deve ser maior que zero."); return False
                    
                    #   Armazenar
                    numero_estruturas_puls = int(conteudo_linha[3])
                    
                    #   loop para estruturas
                    for estrutura in xrange(numero_estruturas_puls):
                        #   Ler a linha
                        conteudo_linha = arquivo_entrada.readline().split(";")
                        linhas_lidas += 1
                        #   Vertedor
                        if conteudo_linha[0] == "VERTEDOR":
                            #   C. descarga
                            try: float(conteudo_linha[1]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente de descarga do vertedor deve ser um número decimal."); return False
                            #   Largura soleira
                            try: float(conteudo_linha[2]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A largura de soleira do vertedor deve ser um número decimal."); return False
                            #   COta soleira
                            try: float(conteudo_linha[3]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota de soleira do vertedor deve ser um número decimal."); return False
                            #   Cota maxima
                            try: float(conteudo_linha[4]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota máxima do vertedor deve ser um número decimal."); return False
                            
                            #   Testar os valores
                            if (float(conteudo_linha[1]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente de descarga do vertedor deve ser maior que zero."); return False
                            if (float(conteudo_linha[2]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A largura de soleira do vertedor deve ser maior que zero."); return False
                            if (float(conteudo_linha[3]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota de soleira do vertedor deve ser maior que zero."); return False
                            if (float(conteudo_linha[4]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota máxima do vertedor deve ser maior que zero."); return False
                                
                        #   Orificio
                        elif conteudo_linha[0] == "ORIFICIO":
                            #   C. descarga
                            try: float(conteudo_linha[1]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente de descarga do orifício deve ser um número decimal."); return False
                            #   Area
                            try: float(conteudo_linha[2]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A área do orifício deve ser um número decimal."); return False
                            #   Altura/DIametro
                            try: float(conteudo_linha[3]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A altura/diâmetro do orifício deve ser um número decimal."); return False
                            #   Cota do centro
                            try: float(conteudo_linha[4]) 
                            except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota do centro do orifício deve ser um número decimal."); return False
                        
                            #   Testar os valores
                            if (float(conteudo_linha[1]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente de descarga do orifício deve ser maior que zero."); return False
                            if (float(conteudo_linha[2]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A área do orifício deve ser maior que zero."); return False
                            if (float(conteudo_linha[3]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A altura/diâmetro do orifício deve ser maior que zero."); return False
                            if (float(conteudo_linha[4]) <= 0):
                                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A cota do centro do orifício deve ser maior que zero."); return False
                                
                        else: # Bobagem escrita
                            #   Avise o usuario
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Estrutura de extravasão '%s' desconhecida.\n\nUtilize: 'VERTEDOR' ou 'ORIFICIO'." %(conteudo_linha[0])); return False
                        
                    #   Ler a linha
                    conteudo_linha = arquivo_entrada.readline().split(";")
                    linhas_lidas += 1
                    
                    #   Substituir a \ por /
                    conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                    #   Tirar os espacos em branco do diretorio informado, se houver
                    while conteudo_linha[1][0] == " ":
                        conteudo_linha[1] = conteudo_linha[1][1:]
                        
                    #   Curva cota volume
                    #   Verificar se o arquivo existe
                    if (path.isfile(conteudo_linha[0]) == True):
                        #   Selecionar ultimo nome
                        extensao_arquivo = conteudo_linha[0].split("/")
                        #   Selecionar extensao
                        extensao_arquivo = extensao_arquivo[-1].split(".")[-1]
                        
                        #   Verificar se a extensao dele e' txt
                        if ((not extensao_arquivo == "txt") or (not extensao_arquivo == "TXT")):
                            #   Testar o arquivo de entrada
                            integridade_arquivo, linha = checarIntegridadeArquivoTexto(conteudo_linha[0], numero_intervalos_tempo)
                            
                            #   Se deu ruim
                            if integridade_arquivo == False:
                                #   Que ruim que deu?
                                if linha == 0: #    Numero de dados incorretos
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","O arquivo fornecido para a curva cota-volume não possui %d (que é o número de intervalos de tempo de simulação) termos (ou linhas)." %(numero_intervalos_tempo)); return False
                                
                                else: # Linha X e' o problema
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","Erro na linha %d.\n\nO arquivo fornecido para a curva cota-volume não obedece os padrões utilizados pelo programa.\n\nDica: As linhas devem possuir o seguinte padrão: 'valor do dado;'."%(linha)); return False
                        
                        else: # nao e' txt
                            #   Avise o usuario
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A extensão do arquivo fornecido para a curva cota-volume deve ser txt."); return False
                        
                    else: #   Nao e' path, teste numero
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O arquivo fornecido para a curva cota-volume não foi localizado."); return False
                    
                    #   Somar uma op
                    nop += 1
                
                #   Testar se e' MKC
                if conteudo_linha[0] == "MKC":
                    #   Testar tamanho da linha
                    if len(conteudo_linha) < 6:
                        #   Avise o usuario
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Informações insuficientes na operação %d (Muskingun-Cunge)." %(nop+1)); return False
                    
                    #   Substituir a \ por /
                    conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                    #   Tirar os espacos em branco do diretorio informado, se houver
                    while conteudo_linha[1][0] == " ":
                        conteudo_linha[1] = conteudo_linha[1][1:]
                    
                    #   hidrograma de entrada
                    #   Verificar se o arquivo existe
                    if (path.isfile(conteudo_linha[1]) == True):
                        #   Selecionar ultimo nome
                        extensao_arquivo = conteudo_linha[1].split("/")
                        #   Selecionar extensao
                        extensao_arquivo = extensao_arquivo[-1].split(".")[-1]
                        
                        #   Verificar se a extensao dele e' txt
                        if ((not extensao_arquivo == "txt") or (not extensao_arquivo == "TXT")):
                            #   Testar o arquivo de entrada
                            integridade_arquivo, linha = checarIntegridadeArquivoTexto(conteudo_linha[1], numero_intervalos_tempo)
                            
                            #   Dizer ao programa que essa operacao nao precisa da saida de outra
                            entrada_operacoes[nop] = 0
                            
                            #   Se deu bom
                            if integridade_arquivo == False:
                                #   Que ruim que deu?
                                if linha == 0: #    Numero de dados incorretos
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","O arquivo fornecido para o hidrograma de entrada não possui %d linhas (que é o número de intervalos de tempo de simulação)." %(numero_intervalos_tempo)); return False
                                
                                else: # Linha X e' o problema
                                    arquivo_entrada.close(); showerror("Erro no arquivo fornecido","Erro na linha %d.\n\nO arquivo fornecido para o hidrograma de entrada não obedece os padrões utilizados pelo programa.\n\nDica: As linhas devem possuir o seguinte padrão: 'valor do dado;'." %(linha)); return False
                        
                        else: # nao e' txt
                            #   Avise o usuario
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A extensão do arquivo fornecido para o hidrograma de entrada para a operação de Muskingun-Cunge deve ser txt."); return False
                        
                    else: #   Nao e' path, teste numero
                        try: int(conteudo_linha[1]) 
                        except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da operação que originará o hidrograma de entrada desta operação deve ser inteiro."); return False
                        
                        #   Testar seu valor
                        if (int(conteudo_linha[1]) <= 0):
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O número da operação que originará o hidrograma de entrada desta operação deve ser maior que zero."); return False
                            
                        #   Checar se o numero do hidrograma de entrada e' possivel de ser encontrado no arquivo de entrada
                        if int(conteudo_linha[1]) > nop_declaradas:
                            arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Não é possível utilizar o hidrograma oriundo da operação número %d na operação %d pois há apenas %d operações hidrológicas declaradas nas informações gerais." %((int(conteudo_linha[1])),(nop+1),(nop_declaradas))); return False
                    
                        #   Dizer ao software que essa operacao precisa da saida de outra
                        entrada_operacoes[nop] = int(conteudo_linha[1])
                        
                    #   DIferenca cota (m)
                    try: float(conteudo_linha[1]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A diferença de cota do canal deve ser um número decimal."); return False
                    #   Comprimento canal (km)
                    try: float(conteudo_linha[2]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O comprimento do canal deve ser um número decimal."); return False
                    #   Largura canal (m)
                    try: float(conteudo_linha[3]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A largura do canal deve ser um número decimal."); return False
                    #   Coeficiente de rugosidade
                    try: float(conteudo_linha[4]) 
                    except: arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente de rugosidade médio deve ser um número decimal."); return False
                    
                    #   Testar os valores
                    if (float(conteudo_linha[1]) <= 0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A diferença de cota do canal deve ser maior que zero."); return False
                    if (float(conteudo_linha[2]) <= 0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O comprimento do canal deve ser maior que zero."); return False
                    if (float(conteudo_linha[3]) <= 0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"A largura do canal deve ser maior que zero."); return False
                    if (float(conteudo_linha[4]) <= 0):
                        arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O coeficiente de rugosidade médio deve ser maior que zero."); return False
                
            else: #   Numero operacao incorreto
                #   Avise o usuario
                arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Número da operação hidrológica incorreto.\nNúmero esperado: %d." %(nop+1)); return False
                
        else: #   Deu erro ai, ta escrito bobagem
            if linhas_lidas < (numero_linhas+1):
                #   Que erro que e'? LInhas em branco no final do arquivo?
                if conteudo_linha[0] == "\n":
                    #   Avise o usuario
                    arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"Não deixe mais de uma linha em branco no final do arquivo de entrada."); return False
                #   Escrito bobagem
                else:
                    #   Avise o usuario
                    arquivo_entrada.close(); showerror("Erro na linha: %d" %(linhas_lidas),"O comando '%s' não está definido no programa.\n\nComandos definidos: 'INICIO', 'CHUVA' e 'OPERACAO'." %(conteudo_linha[0])); return False

    #   Fechar arquivo de entrada
    arquivo_entrada.close()
    
    #   Checar se o numero de chuvas lido corresponde ao numero de chuvas declarado
    if not nch == nch_declaradas:
        showerror("Erro no arquivo de entrada","Foram declaradas %d chuvas nas informações gerais, porém há informação de %d chuvas no arquivo de entrada.\n\nRevise o arquivo de entrada." %((nch_declaradas), (nch))); return False
        
    #   Checar se o numero de operacoes lidas corresponde ao numero de operacoes declaradas
    if not nop == nop_declaradas:
        showerror("Erro no arquivo de entrada","Foram declaradas %d operações nas informações gerais, porém há informação de %d operações no arquivo de entrada.\n\nRevise o arquivo de entrada." %((nop_declaradas), (nop))); return False
    
    #   Checar se não há lógica circular nas operacoes (4->5, 5->6 e 6->4) : Verificar a ordem das operacoes
    for i in xrange(nop_declaradas):
        #   Resetar variaveis
        operacao_a_calcular = i
        decisao = False
        grupo = []
        #   While para cada teste novo
        while decisao == False:
            #   Testar se ela e' uma operacao standalone
            if not entrada_operacoes[operacao_a_calcular] == 0:
                #   Testar se nao vai dar em logica circular
                if not entrada_operacoes[operacao_a_calcular] in grupo:
                    #   Adicione ao grupo
                    grupo.append(entrada_operacoes[operacao_a_calcular])
                    #   Avalie a proxima
                    operacao_a_calcular = entrada_operacoes[operacao_a_calcular] - 1
                #   Logica circular detectada
                else:
                    #   Criar o aviso
                    aviso = str(grupo[0])
                    #   Adicionar demais operacoes ao aviso
                    for i2 in xrange(1, len(grupo)):
                        aviso += ", " + str(grupo[i2])
                    #   Mostrar ao usuario
                    showerror("Erro no arquivo de entrada","Não é possível determinar a ordem de execução das seguintes operações hidrológicas: %s.\n\nRevise os números dos hidrogramas de entrada dessas operações." %(aviso)); return False
            #   Achei uma operacao standalone
            else:
                #   Pare o while e segue para a proxima
                decisao = True
    
    #   Checar se uma operação não dá saída para mais de uma operação. (exemplo: operação 4 e 5 terem (ambas) a operação 3 como entrada)
    for i in xrange(nop_declaradas):
        #   Adicionar na lista somente se a operacao nao for "standalone"
        if not entrada_operacoes[i] == 0:
            #   Verificar se a operacao ja' nao esta' adicionada
            if not entrada_operacoes[i] in lista_repeticao:
                #   Adicionar na lista
                lista_repeticao.append(entrada_operacoes[i])
            #   Se ja esta' adicionada, temos um erro
            else:
                showerror("Erro no arquivo de entrada","A operação %d é saída de duas ou mais operações (o hidrograma de saída de uma operação hidrológica pode somente ser usado como entrada de uma única outra operação hidrologica).\n\nRevise o arquivo de entrada." %(entrada_operacoes[i])); return False
    
    #   Se chegou ate' aqui, o arquivo e' feitoria
    return True
#----------------------------------------------------------------------
def checarIntegridadeArquivoTexto(diretorio_arquivo, numero_linhas_deve_ter):
    """
    Checa o conteudo de arquivos de texto que são dados de entrada, com excessão do arquivo de chuva-observada.
    Retorna: True/False (se e' íntegro), numero (da linha com o erro - 0 significa sem erro)
    """
    #   Contar numero de linhas
    numero_linhas = contarLinhas(diretorio_arquivo)
    
    #   Verificar se ele possui o mesmo numero de termos que o numero de intervalos de tempo de chuva
    if (not numero_linhas == numero_linhas_deve_ter):
        return False, 0
        
    #   Verificar se todos os valores sao de fato valores.... 
    arquivo_leitura_dados = open(diretorio_arquivo,'r')
    
    #   Verificar o arquivo de chuva dado: esta verificacao sera' movida para uma funcao de integridade no inicio do processamento
    for linha_arquivo in xrange(numero_linhas):
        #   Ler a linha e substituir virgulas por ponto
        conteudo_linha = arquivo_leitura_dados.readline().split(";")
        conteudo_linha = conteudo_linha[0].replace(",",".")
        
        #   Tentar transformar o conteudo da linha em numero flutante
        try: float(conteudo_linha)
        except: arquivo_leitura_dados.close(); return False, (linha_arquivo+1)
    
    #   Se chegou ate' aqui, e' porque esta' tudo certo
    arquivo_leitura_dados.close()
    #   Se chegou ate' aqui, retorne verdadeiro
    return True, 0
#----------------------------------------------------------------------
def lerSerieObservada(diretorio_arquivo, numero_linhas_arquivo):
    """Le os valores dos arquivos TXT e joga numa lista para ser retornada"""
    
    from numpy import array, float64
    
    serie_observada = array([0.0 for x in xrange(numero_linhas_arquivo)], float64)
    
    #   Verificar se todos os valores sao de fato valores.... 
    arquivo_leitura_dados = open(diretorio_arquivo,'r')
    
    for linha in xrange(numero_linhas_arquivo):
        #   Ler a linha e substituir virgulas por ponto
        conteudo_linha = arquivo_leitura_dados.readline().split(";")
        conteudo_linha = conteudo_linha[0].replace(",",".")
        
        serie_observada[linha] = float(conteudo_linha)
        
    return serie_observada
#----------------------------------------------------------------------
def contarLinhas(diretorio_arquivo):
    """"""
    numero_linhas = sum(1 for linha in open(diretorio_arquivo,'r'))
    return numero_linhas
#----------------------------------------------------------------------
def lerArquivoEntrada(diretorio_arquivo_entrada):
    """Le o arquivo de entrada e armazena as informacoes"""
    
    import codecs
    
    print "\n\tLendo dados de entrada."
    #   Abrir o arquivo de entrada
    arquivo_entrada = codecs.open(diretorio_arquivo_entrada, mode='r', buffering=0, encoding='latin_1')
    #   A primeira linha le-se manualmente
    conteudo_linha = arquivo_entrada.readline().split(";") # so' leio, mas nao faco nada com isso....
    
    #   Ler linhas ate' que a primeira coisa que o modelo le e' "INICIO" - isto possibilita criar um cabecalho com quantas linhas o usuario desejar
    while not conteudo_linha[0] == "INICIO":
        #   Leia outra linha....
        conteudo_linha = arquivo_entrada.readline().split(";")
    
    #   Assim que o modelo le "INICIO" no inicio da linha, comeca a armazenar o conteudo.
    if conteudo_linha[0] == "INICIO":
        #   Parametros gerais da simulacao - valem para todas as operacoes e chuvas a serem calculadas
        numero_intervalos_tempo       = int(conteudo_linha[1]) # (nint)
        duracao_intervalo_tempo       = int(conteudo_linha[2]) # (dt)
        numero_chuvas                 = int(conteudo_linha[3]) # (nch)
        numero_intervalos_tempo_chuva = int(conteudo_linha[4]) # (nintch)
        numero_operacoes_hidrologicas = int(conteudo_linha[5]) # (nop)
        
        #   Variaveis da logica do programa - controlam os processos e a maneira como o programa vai resolver as operacoes hidrologicas
        codigo_operacoes_hidrologicas  = [None for i in xrange(numero_operacoes_hidrologicas)] # (cdoh) # 1->CHUVA-VAZAO; 2->PULS; 3->MKC; 4->JUNCAO; 5->CENARIOS CHUVA-VAZAO;
        controle_operacoes_hidrologias = [   0 for i in xrange(numero_operacoes_hidrologicas)] # (ctoh) # 0->operacao NAO calculada; 1->operacao CALCULADA
        codigo_chuvas                  = [None for i in xrange(numero_chuvas)] # (cdch) # 0->OBSERVADA; 1->IDF;
        #controle_chuvas                = [   0 for i in xrange(numero_chuvas)] # (ctch) # 0->chuva NAO calculada; 1->chuva CALCULADA
        nomes_operacoes_hidrologicas   = [u" ".encode('latin_1') for i in xrange(numero_operacoes_hidrologicas)] # (nomes) # Recebe o nome das operacoes hidrologicas -> plotagem dos graficos
        
        #   Variaveis das chuvas IDFs
        parametro_a   = [None for i in xrange(numero_chuvas)] # (a)
        parametro_b   = [None for i in xrange(numero_chuvas)] # (b)
        parametro_c   = [None for i in xrange(numero_chuvas)] # (c)
        parametro_d   = [None for i in xrange(numero_chuvas)] # (d)
        tipo_idf      = [None for i in xrange(numero_chuvas)] # (tdif)
        posicao_pico  = [None for i in xrange(numero_chuvas)] # (pp)
        tempo_retorno = [None for i in xrange(numero_chuvas)] # (tr)
        limites_idf   = [None for i in xrange(numero_chuvas)] # (limites)

        #   Variaveis para chuvas OBS
        diretorios_chuvas_observadas = [None for i in xrange(numero_chuvas)] # (dirch)
        
        #   Variaveis das operacoes hidrologicas
                
        #   Chuva-Vazao
        #hidrogramas_saida_pq = [[None] for i in xrange(numero_operacoes_hidrologicas)]
        coeficiente_cn       = [None for i in xrange(numero_operacoes_hidrologicas)] # (cn)
        area_km2             = [None for i in xrange(numero_operacoes_hidrologicas)] # (area)
        tc_horas             = [None for i in xrange(numero_operacoes_hidrologicas)] # (tc)
        chuvas_entrada_pq    = [None for i in xrange(numero_operacoes_hidrologicas)] # (chpq)
        
        #   Chuva-vazao e Muskingum-Cunge
        diferenca_cota_m     = [None for i in xrange(numero_operacoes_hidrologicas)] # (difcot)
        comprimento_canal_km = [None for i in xrange(numero_operacoes_hidrologicas)] # (compcan)
        
        #   PULS
        curvas_cota_volume       = [[None, None] for i in xrange(numero_operacoes_hidrologicas)] # (ccv)
        estruturas_puls          = [None for i in xrange(numero_operacoes_hidrologicas)] # (estp)
        cotas_iniciais_puls_m    = [None for i in xrange(numero_operacoes_hidrologicas)] # (cotinp)
        hidrogramas_entrada_puls = [None for i in xrange(numero_operacoes_hidrologicas)] # (hidentp)
        
        #   MUSKINGUM-CUNGE
        largura_canal_m         = [None for i in xrange(numero_operacoes_hidrologicas)] # (largcan)
        coeficiente_rugosidade  = [None for i in xrange(numero_operacoes_hidrologicas)] # (nmann)
        hidrogramas_entrada_mkc = [None for i in xrange(numero_operacoes_hidrologicas)] # (hidentm)
        
        #   JUNCAO
        hidrogramas_juncoes = [None for i in xrange(numero_operacoes_hidrologicas)] # (hidentj)
        
        #   CENARIOS
        #
        #
        #
        
    #conteudo_linha = self.arquivo_entrada.readline().split(";") #ler a segunda linha, deve ser a dos cenarios....
    #CENARIOS_ANOS = [] #auxiliar do Cenarios, possui QUAIS os anos de cenarios
    # 
    #
    #if conteudo_linha[0] == "CENARIOS": # informacoes dos cenarios
    #    
    #    if ((conteudo_linha[1] != " 0") and (conteudo_linha[1] != '') and (conteudo_linha[1] != '0') and (conteudo_linha[1] != '\n')):    
    #        for i in xrange(1, len(conteudo_linha)):
    #            
    #            if ((conteudo_linha[i] != '0') and (conteudo_linha[i] != ' 0') and (conteudo_linha[i] != '') and (conteudo_linha[i] != '\n')): #cenario 0 nao rola....
    #                CENARIOS_ANOS.append(int(conteudo_linha[i]))

    #   Determinar quantos blocos de linhas serao lidos
    numero_blocos = (numero_chuvas + numero_operacoes_hidrologicas) #saber quantos blocos de linhas deverei ler... cada bloco pode ser uma chuva ou uma operacao

    #   Loop da leitura de dados
    for i in xrange(numero_blocos): #botar barra de progresso para leitura do arquivo de entrada
        #   Ler e quebrar a linha em blocos
        conteudo_linha = arquivo_entrada.readline().split(";") #lera' "CHUVA" ou "OPERACAO" e a chuva que corresponde

        #*--------------------------------- Ler CHUVA ---------------------------------*#
        
        #   Ler CHUVA
        if conteudo_linha[0] == "CHUVA": #e' pra colocar chuva observada ou idf
            #   Armazenar o numero da chuva. Reduz-se 1 pois Python comeca a contar em zero
            numero_chuva_correspondente = (int(conteudo_linha[1]) - 1)
            #   Ler e quebrar a proxima linha em blocos
            conteudo_linha = arquivo_entrada.readline().split(";") #ler IDF e parametros ou OBS
            
            #   Caso for chuva IDF
            if conteudo_linha[0] == "IDF":
                #   Armazenar o codigo
                codigo_chuvas[numero_chuva_correspondente] = 1
                #   Armazenar as variaveis
                tipo_idf[numero_chuva_correspondente]      = (int(conteudo_linha[1]))
                posicao_pico[numero_chuva_correspondente]  = (float(conteudo_linha[2]))
                tempo_retorno[numero_chuva_correspondente] = (int(conteudo_linha[3]))
                parametro_a[numero_chuva_correspondente]   = float(conteudo_linha[4])
                parametro_b[numero_chuva_correspondente]   = float(conteudo_linha[5])
                parametro_c[numero_chuva_correspondente]   = float(conteudo_linha[6])
                parametro_d[numero_chuva_correspondente]   = float(conteudo_linha[7])
                limites_idf[numero_chuva_correspondente]   = int(conteudo_linha[8])
            
            #   Caso for chuva OBSERVADA
            elif conteudo_linha[0] == "OBS": 
                #   Armazenar o codigo
                codigo_chuvas[numero_chuva_correspondente] = 0
                #   Substituir a \ por /
                conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                #   Tirar os espacos em branco do diretorio informado, se houver
                while conteudo_linha[1][0] == " ":
                    conteudo_linha[1] = conteudo_linha[1][1:]
                
                #   Armazenar a chuva
                diretorios_chuvas_observadas[numero_chuva_correspondente] = conteudo_linha[1]

        #*--------------------------------- Ler OPERACAO ---------------------------------*#
        
        #   Ler OPERACAO
        elif conteudo_linha[0] == "OPERACAO": #e' uma operacao hidrologica
            #   Armazenar o numero da operacao
            numero_operacao = (int(conteudo_linha[1]) -1) #guarda a ordem que as operacoes sao entradas no programa.... e' o valor seguido de "OPERACAO;"
            
            #   CASO o usuario informar o nome/local da operacao, armazene-o
            if len(conteudo_linha) > 3: # > 3 pois o terceiro elemento da linha quando o usuário não insere nome algum é "\n" e isso estava ocasionando problemas.
                #   Armazenar o local/nome da operacao
                nomes_operacoes_hidrologicas[numero_operacao] = conteudo_linha[2].encode('latin_1') #o nome e' o terceiro termo da linha
                
            #   Ler a proxima linha para saber qual operacao que o usuario esta' entrando
            conteudo_linha = arquivo_entrada.readline().split(";") #ler qual operacao (PQ, PULS....) e qual e' a chuva que ela utiliza
                
            #*--------------------------------- Ler PQ ---------------------------------*#
            
            #   Caso for operacao de CHUVA-VAZAO
            if conteudo_linha[0] == "PQ":
                #   Colocar o codigo 1 (PQ) na variavel de controle de operacoes
                codigo_operacoes_hidrologicas[numero_operacao] = 1
                #   Determinar o numero da chuva que sera' utilizada na operacao
                operacao_usa_chuva = (int(conteudo_linha[1]) -1) #guarda o numero que nos diz qual chuva sera' usada nesta operacao
                #   Armazenar o numero da chuva que entra nesta operacao
                chuvas_entrada_pq[numero_operacao] = operacao_usa_chuva
                #   Ler e quebrar a proxima linha
                conteudo_linha = arquivo_entrada.readline().split(";") #le qual sera o algoritmo de separacao de escoamento utilizado (1:CN-SCS, se CN do LADO o valor do CN)
                
                #   Armazene o valor de CN
                coeficiente_cn[numero_operacao] = float(conteudo_linha[1])
                
                #   Continue lendo esta operacao chuva-vazao
                conteudo_linha = arquivo_entrada.readline().split(";") #le qual sera' o algoritmo de propagacao do escoamento superficial e valores de tc
                
                #   Armazene a area da bacia em km2
                area_km2[numero_operacao] = float(conteudo_linha[1])
                
                #   Caso o segundo termo da linha for "KIRPICH", o usuario quer calcular o tempo de concentracao da bacia pela equacao de Kirpich
                #if conteudo_linha[2] == "KIRPICH":
                if "KIRPICH" in conteudo_linha[2]:
                    #   Armazenar os valores requeridos pela equacao de Kirpich
                    diferenca_cota_m[numero_operacao]     = float(conteudo_linha[3])
                    comprimento_canal_km[numero_operacao] = float(conteudo_linha[4])
                    
                    tc_horas[numero_operacao] = calcular_TC_Kirpich(diferenca_cota_m[numero_operacao], comprimento_canal_km[numero_operacao])
                
                #   Caso o segundo termo nao for "KIRPICH", apenas armazene o valor do TC (em HORAS)
                else:
                    #   Armazenar o tempo de concentracao (horas)
                    tc_horas[numero_operacao] = float(conteudo_linha[2])
                        
            #*--------------------------------- Ler PULS ---------------------------------*#
            
            #   Caso for operacao de PULS
            elif conteudo_linha[0] == "PULS":
                #   Colocar o codigo 2 (PULS) na variavel de controle de operacoes
                codigo_operacoes_hidrologicas[numero_operacao] = 2
                
                #   O hidrograma de entrada das operacoes PULS podem ser a saida de outra operacao OU dado em um arquivo de entrada
                try:
                    #   Veja se a entrada e' a saida de outra operacao - > Se for um numero inteiro
                    hidrogramas_entrada_puls[numero_operacao] = (int(conteudo_linha[1]) - 1)
                
                #   Nao e' um numero -> entrada feita por um arquivo de entrada
                except:
                    #   Substituir a \ por /
                    conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                    #   Tirar os espacos em branco do diretorio informado, se houver
                    while conteudo_linha[1][0] == " ":
                        conteudo_linha[1] = conteudo_linha[1][1:]
                
                    #   Armazenar o diretorio do arquivo de entrada
                    hidrogramas_entrada_puls[numero_operacao] = conteudo_linha[1].encode('latin_1')
                
                #   Armazenar as cotas iniciais
                cotas_iniciais_puls_m[numero_operacao] = int(conteudo_linha[2]) #armazenar a cota inicial desta operacao puls... se for 0 nao e' puls (pode ser que seja, com cota inicial zero)
                #   Esta variavel e' auxiliar, e' resetada cada operacao. Ela guarda a informacao de cada estrutura em [...], e de cada operacao em [[,,,],[,,,]]
                estruturas_desta_operacao = [[0,0,0,0,0] for i2 in xrange(int(conteudo_linha[3]))] #variavel que deve ser resetada a cada nova operacao puls
                
                #   Loop para ler as estruturas de determinada operacao
                for estrutura in xrange(int(conteudo_linha[3])):
                    #   Ler a estrutura
                    conteudo_linha = arquivo_entrada.readline().split(";")          #ler cada estrutura
                    #   Armazenar a informacao
                    estruturas_desta_operacao[estrutura][0] = (conteudo_linha[0])        #Armazenar "VERTEDOR" ou "ORIFICIO"
                    estruturas_desta_operacao[estrutura][1] = (float(conteudo_linha[1])) #Armazenar coeficiente da estrutura
                    estruturas_desta_operacao[estrutura][2] = (float(conteudo_linha[2])) #Armazenar informacoes da estrutura
                    estruturas_desta_operacao[estrutura][3] = (float(conteudo_linha[3])) #Armazenar informacoes da estrutura
                    estruturas_desta_operacao[estrutura][4] = (float(conteudo_linha[4])) #Armazenar informacoes da estrutura
                
                #   Armazenar toda a informacao das estruturas em uma sublista de estruturas_puls
                estruturas_puls[numero_operacao] = (estruturas_desta_operacao) #ORGANIZADA DE MANEIRA QUE CADA TERMO E' UMA OPERACAO, E CADA LISTA DENTRO DE CADA TERMO E' UMA ESTRUTURA
                    #                                                                                                              #
                    #     Exemplo: 3 operacoes: A primeira com 3 estruturas. A segunda com 1 estrutura. A terceira com 2 estruturas#
                    #estruturas_puls = [ [ [],[],[] ], [ [] ], [ [],[] ] ]  <--- Estrutura da variavel                             #
                    #                    (          ), (    ), (       )   <--- Conteudo de cada OPERACAO                          #
                    #                      (),(),()      ()      (),()   <--- Conteudo de cada ESTRUTURA                           #
                    ################################################################################################################
                
                #   Continue a ler o arquivo de entrada
                conteudo_linha = arquivo_entrada.readline().split(";") #ler o diretorio do arquivo de cota-vazao
                #   Armazenar o diretorio do arquivo com a informacao da cota-volume
                diretorio_curva_cotavolume = conteudo_linha[0]  #diretorio armazenado, abra ele agora.
                #   Contar quantas linhas tem o arquivo da curva cota-volume
                numero_linhas    = sum(1 for linha in open(diretorio_curva_cotavolume,'r'))      #contar o numero de linhas do arquivo da curva cota-volume
                #   Criar uma variavel temporaria que armazenara o conteudo da linha
                curva_provisoria = [[0 for i3 in xrange(numero_linhas)] for i4 in xrange(2)]     #cria uma lista com 2 termos, cada um deles com numero_linhas linhas.
                #   Abra o arquivo
                arquivo_curva    = open(diretorio_curva_cotavolume, 'r')                         #abrir o arquivo para le-lo.
                
                #   Loop para ler linhas do arquivo da curva cota-volume
                for linha in xrange(numero_linhas):
                    #   Ler e quebrar a linha
                    conteudo_curva = arquivo_curva.readline().split(";")    #ler a linha e dividir 
                    #   Armazenar o conteudo
                    curva_provisoria[0][linha] = float(conteudo_curva[0])   #valores de cota
                    curva_provisoria[1][linha] = float(conteudo_curva[1])   #valores de volume
                
                #   Fechar o arquivo da curva cota-volume
                arquivo_curva.close() #fechar o arquivo -> poupar memoria.
                #   Armazenar a curva na variavel que sera' retornada mais tarde
                curvas_cota_volume[numero_operacao] = (curva_provisoria) #somente havera' curva se for puls, logo, usar contador manual aqui.##################################
                    #                                                                                                                                                         #
                    #curvas_cota_volume = [ [ [...],[...] ], [ [...],[...] ], [ [...],[...] ], ... ]                                                                          #
                    #                       (             ), (             ), (             )  <--- Conteudo de cada curva cota-volume, cada puls com seu (    )              #
                    #                         (...),(...)      (...),(...)      (...),(...)    <--- Conteudo das curvas, o primeiro (...) e' cota, o segundo (...) e' volume. #
                    ###########################################################################################################################################################
                
            #*--------------------------------- Ler MKC ---------------------------------*#
            
            #   Caso for operacao de MKC
            elif conteudo_linha[0] == "MKC":  #OPERACAO DE MUSKINGUN-CUNGE!!
                #   Colocar o codigo 3 (MKC) na variavel de controle de operacoes
                codigo_operacoes_hidrologicas[numero_operacao] = 3
                
                #   O hidrograma de entrada das operacoes PULS podem ser a saida de outra operacao OU dado em um arquivo de entrada
                try:
                    #   Veja se a entrada e' a saida de outra operacao - > Se for um numero inteiro
                    hidrogramas_entrada_mkc[numero_operacao] = (int(conteudo_linha[1]) - 1)
                    
                #   Nao e' um numero -> entrada feita por um arquivo de entrada
                except:
                    #   Substituir a \ por /
                    conteudo_linha[1] = conteudo_linha[1].replace("\\","/")
                
                    #   Tirar os espacos em branco do diretorio informado, se houver
                    while conteudo_linha[1][0] == " ":
                        conteudo_linha[1] = conteudo_linha[1][1:]
                    
                    #   Armazenar o diretorio do arquivo de entrada
                    hidrogramas_entrada_mkc[numero_operacao] = conteudo_linha[1].encode('latin_1')
                    
                #   Armazenar as demais informacoes da operacao
                diferenca_cota_m[numero_operacao]       = float(conteudo_linha[2]) #armazenar a diferenta de cota do canal em metros.
                comprimento_canal_km[numero_operacao]   = float(conteudo_linha[3]) #armazenar o comprimento do canal em quilometros.
                largura_canal_m[numero_operacao]        = float(conteudo_linha[4]) #armazenar a largura canal em metros.
                coeficiente_rugosidade[numero_operacao] = float(conteudo_linha[5]) #armazenar o coeficiente de rugosidade de manning.
            
            #*--------------------------------- Ler JUNCAO ---------------------------------*#
            
            #OPERACAO; n; Nome/local operacao
            #JUNCAO;2;3;    ou    #JUNCAO;2;3;;;;
            
        #    #   Caso for operacao de JUNCAO
        #    elif conteudo_linha[0] == "JUNCAO": #OPERACAO DE JUNCAO DE HIDROGRAMAS
        #        #   Colocar o codigo 4 (JUNCAO) na variavel de controle de operacoes
        #        codigo_operacoes_hidrologicas[numero_operacao] = 4
        #        
        #        #   E' -2 pois o primeiro termo e' a escrita "JUNCAO" e o ultimo e' um enter (que sempre ha' apos o ultimo ;) 
        #        if conteudo_linha[-1] == ";":
        #            hidrogramas_juncao = [-1 for indices in xrange((len(conteudo_linha)-1))] # Vai ser sempre [ -1, -1, -1, ... ]; Fazer as verificacoes com >= 0 !!!
        #            
        #        else:
        #            hidrogramas_juncao = [-1 for indices in xrange((len(conteudo_linha)-2))] # Vai ser sempre [ -1, -1, -1, ... ]; Fazer as verificacoes com >= 0 !!!
        #        
        #        #   Loop dos hidrogramas
        #        for ler_hid in xrange(1,(len(conteudo_linha)-1)): #vai de 1 a len(conteudo_linha)-1 pois tem um enter depois do ultimo ; 
        #            #   Manejo de erro
        #            try:
        #                hidrogramas_juncao[(ler_hid-1)] = (int(conteudo_linha[ler_hid]) - 1) #sempre reduzir 1 pois os indices em python comecam em ZERO.
        #            
        #            #   Tratamento de erro
        #            except ValueError: #nao consegue converter o conteudo em numero: caso -> JUNCAO;x;y;;;;
        #                
        #                while (conteudo_linha[(ler_hid)][0] == ' '): #correcao de bug: se o diretorio fornecido pelo usuario comecar com espaco ' ', o programa nao encontra o arquivo
        #                    conteudo_linha[ler_hid] = conteudo_linha[ler_hid][1:]  #remover todos os espacos que estao antes do diretorio
        #                    
        #                hidrogramas_juncao[(ler_hid-1)] = str(conteudo_linha[ler_hid]) #caso ter texto escrito (diretorio entrada)
        #                
        #            #   Tratamento de erro
        #            except IndexError: #nao ha' mais termos na linha: caso -> JUNCAO;x;y; .... Deve ocorrer se nenhum numero for colocado ou ';' estiver faltando.....
        #                hidrogramas_juncao[(ler_hid-1)] = -1
        #            
        #        #   Armazenar os numeros dos hidrogramas que serao somados.
        #        hidrogramas_juncoes[numero_operacao] = hidrogramas_juncao
        #    
        #    #   CASO A OPERACAO NAO FOR IDENTIFICADA
        #    else:
        #        print "\n\nOperacao nao identificada. Revise o arquivo de entrada."
        #        raw_input("\nPressione enter para sair.")
        #        sys.exit();
                
        #   Atualizar barra de progresso
        progressBar(i, numero_blocos)
        
    #   Fazer o retorno das variaveis
    return numero_intervalos_tempo, duracao_intervalo_tempo, numero_chuvas, numero_intervalos_tempo_chuva, numero_operacoes_hidrologicas, codigo_operacoes_hidrologicas, controle_operacoes_hidrologias, codigo_chuvas, nomes_operacoes_hidrologicas, parametro_a, parametro_b, parametro_c, parametro_d, limites_idf, tipo_idf, posicao_pico, tempo_retorno, diretorios_chuvas_observadas, coeficiente_cn, area_km2, tc_horas, chuvas_entrada_pq, diferenca_cota_m, comprimento_canal_km, curvas_cota_volume, estruturas_puls, cotas_iniciais_puls_m, hidrogramas_entrada_puls, largura_canal_m, coeficiente_rugosidade, hidrogramas_entrada_mkc, hidrogramas_juncoes
#-----------------------------------------------------------------------