# -*- coding: latin_1 -*-

#----------------------------------------------------------------------
#   Funcao para criar as variaveis de saida de hidrograma
def gerarVariaveisSaidaJUNCAO(codigo_operacoes_hidrologicas, numero_intervalos_tempo):
    """Cria a matriz de saida para calcular as operacoes MKC"""
    #   Import...        
    from numpy import array, float64
    
    #   Contador
    numero_operacoes_juncao = 0
    #   Conte as operacoes MKC:
    for i in xrange(len(codigo_operacoes_hidrologicas)):
        #   3 e' JUNCAO
        if codigo_operacoes_hidrologicas[i] == 4:
            #   Conte...
            numero_operacoes_juncao += 1
    
    #   Variavel que armazena os hidrogramas gerados pelo chuva-vazao ...
        hidrogramas_saida_juncao = array([[0.0 for i in xrange(numero_intervalos_tempo)] for y in xrange(numero_operacoes_juncao)], float64)

    #   Retorne
    return hidrogramas_saida_juncao
#----------------------------------------------------------------------------------
#   Variavel para pegar o hidrograma de entrada para rodar o MKC
def preparacaoJUNCAO(numero_intervalos_tempo, hidrogramas_entrada_juncoes, ordpq, ordp, ordm, ordj, hidsaipq, hidsaip, hidsaim, hidsaij):
    #   Import...        
    from numpy import array, float64
    
    #   Declarar
    hidrogramas_usados_nesta_juncao = array([[0.0 for i in xrange(numero_intervalos_tempo)]for numero_hidrogramas in xrange(len(hidrogramas_entrada_juncoes))], float64)

    #   Itero entre os termos da variavel que diz que tem hidrogramas entrando nesta juncao
    for numero_hidrograma in xrange(len(hidrogramas_entrada_juncoes)):
        #   Analisar o tipo do hidrograma que entra na juncao...
        if ((type(hidrogramas_entrada_juncoes[numero_hidrograma]) == int) and (hidrogramas_entrada_juncoes[numero_hidrograma]) >= 0):
            
            #   Analisar se esse hidrograma nao e' oriundo de uma operacao PQ
            if (hidrogramas_entrada_juncoes[numero_hidrograma] in ordpq):
                #   Pegar o indice do hidrograma
                indice_hidrograma = ordpq.index(hidrogramas_entrada_juncoes[numero_hidrograma])
                #   Pegar os valores
                hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaipq[indice_hidrograma]
    
            #   Analisar se esse hidrograma nao e' oriundo de uma operacao PULS
            if (hidrogramas_entrada_juncoes[numero_hidrograma] in ordp):
                #   Pegar o indice do hidrograma
                indice_hidrograma = ordp.index(hidrogramas_entrada_juncoes[numero_hidrograma])
                #   Pegar os valores
                hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaip[indice_hidrograma]
                
            #   Analisar se esse hidrograma nao e' oriundo de uma operacao PQ
            if (hidrogramas_entrada_juncoes[numero_hidrograma] in ordm):
                #   Pegar o indice do hidrograma
                indice_hidrograma = ordm.index(hidrogramas_entrada_juncoes[numero_hidrograma])
                #   Pegar os valores
                hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaim[indice_hidrograma]
                
            #   Analisar se esse hidrograma nao e' oriundo de uma operacao PQ
            if (hidrogramas_entrada_juncoes[numero_hidrograma] in ordj):
                #   Pegar o indice do hidrograma
                indice_hidrograma = ordj.index(hidrogramas_entrada_juncoes[numero_hidrograma])
                #   Pegar os valores
                hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaij[indice_hidrograma]
        
        #   Se entrar aqui, e' pra entrar com um hidrograma observado...
        else:  #e' um hidrograma observado, deve-se ler o arquivo.
            #   Contar o numero de linhas do arquivo da curva cota-volume
            numero_linhas = sum(1 for linha in open(hidrogramas_entrada_juncoes[numero_hidrograma],'r'))
            #   Abra o arquivo
            arquivo_hidrograma = open(hidrogramas_entrada_juncoes, 'r') #abrir o arquivo para le-lo.
            
            #   Loop para ler linhas do arquivo
            for linha in xrange(numero_linhas):
                #   Ler a linha
                conteudo_hidrograma = arquivo_hidrograma.readline().split(";")            #ler a linha e dividir 
                #   Armazenar seu valor
                hidrogramas_usados_nesta_juncao[numero_hidrograma][linha] = float(conteudo_hidrograma[0])        #valores de hidrograma
            #   Fechar o arquivo -> poupar memoria.
            arquivo_hidrograma.close() 
        
    return hidrogramas_usados_nesta_juncao
#----------------------------------------------------------------------------------
#   Funcao para calcular as variaveis de saida de hidrograma
def calcularOperacaoJUNCAO(hidrogramas_entrada, numero_intervalos_tempo):
    #   Import
    from Hydrolib import somar_Hidrogramas
        
    #   Aplicar JUNCAO
    hidrograma_resultante = somar_Hidrogramas(numero_intervalos_tempo, hidrogramas_entrada)
    
    #if (self.plotar_graficos) == 1:
    #        #Plotar grafico puls da operacao
    #        #se e' algo que ja' esta' definido antes de rodar o programa, usa-se [dados_utilizados]; Se e' algo que esta' definido agora (como HIDROGRAMAS), usa-se [contador_manual];
    #                
    #    Hydrolib.plotar_Hidrogramas_PULS( HIDROGRAMA_ENTRA, HIDROGRAMA_SAI, NUMERO_INTERVALOS_TEMPO, self.caminho_arquivo_entrada, NOMES_OPERACOES_HIDROLOGICAS, numero_do_grafico )
        
    #   Retornar hidrograma de saida
    return hidrograma_resultante
#----------------------------------------------------------------------------------
#   Escreva o arquivo de saida para as operacoes de MKC
def escreverSaidaJUNCAO(numero_intervalos_tempo, duracao_intervalo_tempo, numero_operacoes_hidrologicas, codigo_operacoes_hidrologicas, hidrogramas_entrada_juncoes, hidrogramas_saida_pq, hidrogramas_saida_puls, hidrogramas_saida_mkc, hidrogramas_saida_juncoes, ordpq, ordp, ordm, ordj, diretorio_saida, nome_arquivo):
    #   Import...
    from os import path
    
    #   Preparo arquivo de saida
    saidaPULS, fileExtension = path.splitext(diretorio_saida +"/Saida_JUN_" + nome_arquivo)
    saidaPULS               += ".ohy" #arquivo saida igual ao de entrada + o(output) hy(drology)
    saidaPULS                = open(saidaPULS, 'w', buffering = 0)

    #   Cabecalho
    saidaPULS.write ("\n                          MODELO HYDROLIB\n                     RESULTADOS DA MODELAGEM")
    saidaPULS.write ("\n------------------------------------------------------------------------\n\n")

    #   Escrevo os parametros no arquivo de saida
    saidaPULS.write("\n ---- PARAMETROS GERAIS DA SIMULACAO  ----\n\n")
    saidaPULS.write("Numero de intervalos de tempo           : "+str(numero_intervalos_tempo)+"\n")
    saidaPULS.write("Duracao do intervalo de tempo (seg)     : "+str(duracao_intervalo_tempo)+"\n")
    saidaPULS.write("Numero total de simulacoes hidrologicas : "+str(len(codigo_operacoes_hidrologicas))+"\n")
    saidaPULS.write("Numero de simulacoes de Juncoes         : "+str(len(hidrogramas_saida_juncoes))+"\n\n")
    
    #   faz parte do cabecalho do programa
    for i in xrange( len(codigo_operacoes_hidrologicas) ):
        #   Se essa operacao for de JUNCAO.... == 4
        if codigo_operacoes_hidrologicas[i] == 4:
            
            #   Saber qual e' o indice correto para a matriz de saida de dados
            indice_saida = ordj.index(i)
    
            saidaPULS.write("\n-------------------------------------------------------------------------------------------\n")
            saidaPULS.write("Operacao hidrologica numero: " + str(i+1))
            
            #   Criar a matriz que juntara' os resultados
            hidrogramas_usados_nesta_juncao = [[0. for nint_tempo in xrange(numero_intervalos_tempo)] for numero_hidrogramas in xrange(len(hidrogramas_entrada_juncoes[i]))]
            
            #    loop para comecar a copiar os valores
            for numero_hidrograma in xrange(len(hidrogramas_entrada_juncoes[i])):
        
                    #        Analisar de onde eu pego o hidrograma.... Este loop e' necessario pois temos hidrogramas oriundo de ate' 4 variaveis e dados por txt...
                    #        Este algoritmo seleciona a parte interessante do algoritmo para facilitar o proximo algoritmo (escrever).. se isso nao fosse feito,
                    #    seria necessario varios IFs que seriam testados a cada NUMERO_INTERVALO_TEMPO, deixando o programa mais lento.
                    
                #   Analisar o tipo do hidrograma que entra na juncao...
                if ((type(hidrogramas_entrada_juncoes[i][numero_hidrograma]) == int) and (hidrogramas_entrada_juncoes[i][numero_hidrograma]) >= 0):
                            
                    #   Analisar se esse hidrograma nao e' oriundo de uma operacao PQ
                    if (hidrogramas_entrada_juncoes[i][numero_hidrograma] in ordpq):
                        #   Pegar o indice do hidrograma
                        indice_hidrograma = ordpq.index(hidrogramas_entrada_juncoes[i][numero_hidrograma])
                        #   Pegar os valores
                        hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaipq[indice_hidrograma]
            
                    #   Analisar se esse hidrograma nao e' oriundo de uma operacao PULS
                    if (hidrogramas_entrada_juncoes[i][numero_hidrograma] in ordp):
                        #   Pegar o indice do hidrograma
                        indice_hidrograma = ordp.index(hidrogramas_entrada_juncoes[i][numero_hidrograma])
                        #   Pegar os valores
                        hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaip[indice_hidrograma]
                        
                    #   Analisar se esse hidrograma nao e' oriundo de uma operacao PQ
                    if (hidrogramas_entrada_juncoes[i][numero_hidrograma] in ordm):
                        #   Pegar o indice do hidrograma
                        indice_hidrograma = ordm.index(hidrogramas_entrada_juncoes[i][numero_hidrograma])
                        #   Pegar os valores
                        hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaim[indice_hidrograma]
                        
                    #   Analisar se esse hidrograma nao e' oriundo de uma operacao PQ
                    if (hidrogramas_entrada_juncoes[i][numero_hidrograma] in ordj):
                        #   Pegar o indice do hidrograma
                        indice_hidrograma = ordj.index(hidrogramas_entrada_juncoes[i][numero_hidrograma])
                        #   Pegar os valores
                        hidrogramas_usados_nesta_juncao[numero_hidrograma] = hidsaij[indice_hidrograma]
                    
                #   Se entrar aqui, e' pra entrar com um hidrograma observado...
                else:  #e' um hidrograma observado, deve-se ler o arquivo.
                        #contar quantas linhas tem o arquivo
                    numero_linhas  = sum(1 for linha in open(hidrogramas_entrada_juncoes[i][numero_hidrograma],'r')) #contar o numero de linhas do arquivo da curva cota-volume
                    
                        #Nao sei se isto e' necessario, mas se o arquivo fornecido pelo usuario nao tiver o mesmo numero de termos que NUMERO_INTERVALOS_TEMPO, o programa deve ser finalizado, pois nao sei como proceder neste caso.
                    if (not numero_linhas == numero_intervalos_tempo): #ERRO?
                        tkMessageBox.showinfo("Verifique os arquivos de entrada das operações Junção!", "Um dos hidrogramas fornecidos pelo usuário (arquivo .txt) não tem o mesmo número de termos (linhas) que o número de intervalos de tempo da simulação.") 
                        tkMessageBox.showinfo("O modelo será finalizado.", "Revise os arquivos de hidrogramas e tente novamente.\nDica: Não deixe linhas em branco no final do arquivo.") 
                        self.ragequit()
                    
                    arquivo_hidrograma = open(hidrogramas_entrada_juncoes[i][numero_hidrograma], 'r') #abrir o arquivo para le-lo.
                    
                        #loop para ler linhas do arquivo da curva cota-volume
                    for linha in xrange(numero_linhas):
                        conteudo_hidrograma = arquivo_hidrograma.readline().split(";")            #ler a linha e dividir 
                        hidrogramas_usados_nesta_juncao[numero_hidrograma][linha] = float(conteudo_hidrograma[0])        #valores de hidrograma
                    
                    arquivo_hidrograma.close() #fechar o arquivo -> poupar memoria.
            
                #   Fazer algoritmo para escrever o conteudo no arquivo de saida
            
                #    saber qual e' o indice da operacao em ordem crescente-----> e' diferente da ordem da execucao.....
                indice_hidrograma_saida = ordj.index(i)  #usado pra variavel de saida do juncao
                
                #   Cabecalho
                saidaJUNCAO.write("\n\n\n\t\t--- HIDROGRAMAS SOMADOS NESTA JUNCAO ---\n\n")
                
                #   Escrever os hidrogramas no arquivo de saida
                for cabecalho in xrange(len(hidrogramas_entrada_juncoes[i])):
                    if type(hidrogramas_entrada_juncoes[i][cabecalho] == int):
                        saidaJUNCAO.write("Hidrograma " + (str(cabecalho+1)) + ": " + str((hidrogramas_entrada_juncoes[i][cabecalho]) + 1) + "\n")
                    else:
                        saidaJUNCAO.write("Hidrograma " + (str(cabecalho+1)) + ": " + str(hidrogramas_entrada_juncoes[i][cabecalho]) + "\n")
                
                #   Escrever o detalhamento dos valores
                saidaJUNCAO.write("\n\n\t\t\t---- DETALHAMENTO ----\n\n")
                string_aux = "      dt   HIDResultante"
                
                #   Loop para montar o cacecalho do detalhamento
                for x in xrange(len(hidrogramas_entrada_juncoes[i])):
                    if x >= 9: # Logo e' somado 1, por isso >= 9
                        string_aux += (" Hidrograma" + str(x+1))
                    else:
                        string_aux += ("  Hidrograma" + str(x+1))
            
                #   Organizacao do arquivo de saida
                saidaPQ.write(string_aux)
                saidaPQ.write("\n")
            
                #   Loop para as linhas
                for valor in xrange(numero_intervalos_tempo):
                    saidaJUNCAO.write("%8d, %16.8f" %((valor+1), hidrogramas_saida_juncoes[indice_hidrograma_saida][valor]) )
                
                    #   Loop para colunas
                    for numero_hidrograma in xrange(len(hidrogramas_entrada_juncoes[i])):
                        saidaJUNCAO.write("%13.7f" %(hidrogramas_usados_nesta_juncao[numero_hidrograma][valor])) #varia o hidrograma e o intervalo de tempo fica fixo.
                    saidaJUNCAO.write("\n")
                
    #   Feche o arquivo...
    saidaJUNCAO.close()
#----------------------------------------------------------------------