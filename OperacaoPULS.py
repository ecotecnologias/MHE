# -*- coding: latin_1 -*-

#----------------------------------------------------------------------
#   Funcao para criar as variaveis de saida de hidrograma
def gerarVariaveisSaidaPULS(codigo_operacoes_hidrologicas, numero_intervalos_tempo):
    """Cria a matriz de saida para calcular as operacoes PULS"""
    #   Import...        
    from numpy import array, float64
    
    #   Contador
    numero_operacoes_puls = 0
    #   Conte as operacoes PQ:
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   2 e' PULS
        if codigo_operacoes_hidrologicas[ii] == 2:
            #   Conte...
            numero_operacoes_puls += 1
    
    #   Variavel que armazena os hidrogramas gerados pelo chuva-vazao ...
        hidrogramas_saida_puls = array([[0.0 for ii in xrange(numero_intervalos_tempo)] for y in xrange(numero_operacoes_puls)], float64)

    #   Retorne
    return hidrogramas_saida_puls
#----------------------------------------------------------------------------------
#   Variavel para pegar o hidrograma de entrada para rodar o Puls
def preparacaoPULS(numero_intervalos_tempo, hidrogramas_entrada_puls, operacao_a_calcular, ordpq, ordp, ordm, ordj, hidsaipq, hidsaip, hidsaim, hidsaij):
    """
    Retorna um 'array' que e' usado para como hidrograma de entrada da simulacao de Puls.
    Pode ocasioar termino da execucao do software se o hidrograma for observado e o arquivo fornecido nao foi integro.
    """
    
    #   Import...        
    from numpy import array, float64
    from sys import exit
    from Leitura import checarIntegridadeArquivoTexto, lerSerieObservada
    
    #   Declarar
    hidrograma_usado_neste_puls = array([0.0 for ii in xrange(numero_intervalos_tempo)], float64)
    
    #   Aqui comeco a analise: Ver se o hidrograma de entrada e' oriund ode outra operacao hidrologica
    if (type(hidrogramas_entrada_puls[operacao_a_calcular]) == int):
        #   Ver se e' oriunda da operacao de PQ
        if hidrogramas_entrada_puls[operacao_a_calcular] in ordpq:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordpq.index(hidrogramas_entrada_puls[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_puls = hidsaipq[ind_hid]
        
        #   Ver se e' oriunda da operacao de PULS
        elif hidrogramas_entrada_puls[operacao_a_calcular] in ordp:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordp.index(hidrogramas_entrada_puls[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_puls = hidsaip[ind_hid]
            
        #   Ver se e' oriunda da operacao de MKC
        elif hidrogramas_entrada_puls[operacao_a_calcular] in ordm:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordm.index(hidrogramas_entrada_puls[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_puls = hidsaim[ind_hid]
    
        #   Ver se e' oriunda da operacao de JUNC
        elif hidrogramas_entrada_puls[operacao_a_calcular] in ordj:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordj.index(hidrogramas_entrada_puls[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_puls = hidsaij[ind_hid]
    
    #   Ele e' oriundo de um arquivo de texto
    else:
        #   Pegar o diretorio do arquivo de chuva observada
        diretorio_arquivo = hidrogramas_entrada_puls[operacao_a_calcular]
        #   Testar integridado do arquivo de chuva fornecido
        integridade_arquivo, linha = checarIntegridadeArquivoTexto(diretorio_arquivo, numero_intervalos_tempo)
        
        #
        if integridade_arquivo == True:
            #   Ler valores
            hidrograma_usado_neste_puls = lerSerieObservada(diretorio_arquivo, numero_intervalos_tempo)
            
        else: #   Deu ruim
            #   Que ruim que deu?
            if linha == 0: #    Numero de dados incorretos
                print("Foi detectado um erro na leitura do hidrograma observado da operacao %d (PULS).\nReveja os dados de entrada." %(operacao_a_calcular+1))
                showerror("Erro no arquivo fornecido","O arquivo '%s' (fornecido para o hidrograma de entrada observado da operação %d - PULS) não possui %d linhas (que é o número de intervalos de tempo da simulação)." %(diretorio_arquivo, (operacao_a_calcular+1), numero_intervalos_tempo))
                showerror("Erro na leitura de hidrogramas","A simulação não pode continuar sem a informação do hidrograma %d.\nFaça as correções necessárias e tente novamente.\n\nO modelo será finalizado." %(operacao_a_calcular+1))
                exit()
            
            else: # Linha X e' o problema
                print("Foi detectado um erro na leitura do hidrograma observado da operacao %d (PULS).\nReveja os dados de entrada." %(operacao_a_calcular+1))
                showerror("Erro no arquivo fornecido","Erro na linha %d.\nO arquivo '%s' (fornecido para o hidrograma de entrada observado da operação %d - PULS) não obedece os padrões utilizados pelo programa.\n\nDica: As linhas devem possuir o seguinte padrão: 'valor do dado;'." %(linha, diretorio_arquivo, (operacao_a_calcular+1)))
                showerror("Erro na leitura de hidrogramas","A simulação não pode continuar sem a informação do hidrograma %d.\nFaça as correções necessárias e tente novamente.\n\nO modelo será finalizado." %(operacao_a_calcular+1))
                exit()
    
    return hidrograma_usado_neste_puls
#----------------------------------------------------------------------------------
#   Funcao para calcular as variaveis de saida de hidrograma
def calcularOperacaoPULS(hidrograma_entrada, cota_inicial, estruturas_puls, curva_cota_volume, duracao_intervalo_tempo, numero_intervalos_tempo, nome_operacao_hidrologica, numero_operacao, diretorio_saida, gerar_plotagens):
    #   Import
    from Hydrolib import calcular_VazaoSaida_Puls, aplicar_Puls
    #   Obter a curva de vazoes
    curva_de_vazoes, alturas_vazoes_calculadas = calcular_VazaoSaida_Puls(estruturas_puls, curva_cota_volume[0]) # curva_cota_volume[0] por que nesta etapa nao preciso de volume, so' de cota, entao mando so' a curva de cota.
    #   Aplicar puls
    hidrograma_resultante = aplicar_Puls(curva_cota_volume, hidrograma_entrada, curva_de_vazoes, alturas_vazoes_calculadas, cota_inicial, numero_intervalos_tempo, duracao_intervalo_tempo)
    ##   Graficos
    #if gerar_plotagens == 1:
    #    #...
    #    Hydrolib.plotar_Hidrogramas_PULS( HIDROGRAMA_ENTRA, HIDROGRAMA_SAI, NUMERO_INTERVALOS_TEMPO, self.caminho_arquivo_entrada, NOMES_OPERACOES_HIDROLOGICAS, numero_do_grafico )
    #   Retornar hidrograma de saida
    return hidrograma_resultante
#----------------------------------------------------------------------------------
#   Escreva o arquivo de saida para as operacoes de PULS
def escreverSaidaPULS(numero_intervalos_tempo, duracao_intervalo_tempo, numero_operacoes_hidrologicas, codigo_operacoes_hidrologicas, hidrogramas_entrada_puls, hidrogramas_saida_pq, hidrogramas_saida_puls, ordpq, ordp, ordm, ordj, diretorio_saida, nome_arquivo, nomes_operacoes):
    #   Import...
    from os import path
    from numpy import argmax
    import codecs
    
    #   Preparo arquivo de saida
    diretorio_saida = str(diretorio_saida + "/Saida_Puls_" + nome_arquivo + ".ohy")
    saidaPULS = codecs.open(diretorio_saida, mode='w', buffering=0, encoding='latin_1')
    
    #   Cabecalho
    saidaPULS.write(u"\u000A                          MODELO HYDROLIB\u000A                     RESULTADOS DA MODELAGEM")
    saidaPULS.write(u"\u000A------------------------------------------------------------------------\u000A")

    #   Escrevo os parametros no arquivo de saida
    saidaPULS.write(u"\u000A ---- PARAMETROS GERAIS DA SIMULAÇÃO  ----\u000A\u000A")
    saidaPULS.write(u"Número de intervalos de tempo            = %d\u000A" %(numero_intervalos_tempo))
    saidaPULS.write(u"Duração do intervalo de tempo (segundos) = %d\u000A" %(duracao_intervalo_tempo))
    saidaPULS.write(u"Número total de simulações hidrológicas  = %d\u000A" %(len(codigo_operacoes_hidrologicas)))
    saidaPULS.write(u"Número de simulações de Puls             = %d\u000A" %(len(hidrogramas_saida_puls)))
    saidaPULS.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    saidaPULS.write(u" ---- INFORMAÇÕES DAS SIMULAÇÕES DE PROPAGAÇÃO DE PULS ---- \u000A")
    #   Loop para escrever as informacoes
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   Se o codigo dizer que e' Puls....
        if codigo_operacoes_hidrologicas[ii] == 2:
            #   Cabecalho da operacao
            saidaPULS.write(u"\u000AHidrograma %d:%s\u000A" %((ii+1), nomes_operacoes[ii].decode('latin_1')))
            
            #   Se entrar neste loop e' porque o hidrograma de entrada do puls que sera' escrito e' oriundo de outra operacao
            if (type(hidrogramas_entrada_puls[ii]) == int): 
                #   Oriundo de uma operacao hidrologica qualquer
                saidaPULS.write(u"\u0009Número do hidrograma de entrada = %d\u000A" %(hidrogramas_entrada_puls[ii] + 1))
                
                #   Tenho que descobrir se e' oriundo de um chuva-vazao, puls ou mkc (nao incluso ainda)
                if (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 1):
                    #   e' oriundo de chuva-vazao
                    saidaPULS.write(u"\u0009Hidrograma oriundo de uma operação de chuva-vazão.\u000A")
                    
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de puls tambem
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 2):
                    #   se e' oriundo de outro PULS
                    saidaPULS.write(u"\u0009Hidrograma oriundo de uma operação de propagação de reservatórios de Puls.\u000A")
                    
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de muskigun-cunge
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 3):
                    #   se e' oriundo de MKC
                    saidaPULS.write(u"\u0009Hidrograma oriundo de uma operação de propagação de canais de Muskingun-Cunge.\u000A")
                    
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de JUNCAO
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 4):
                    #  se e' oriundo de JUNCAO
                    saidaPULS.write(u"\u0009Hidrograma oriundo de uma operação de junção entre hidrogramas.\u000A")
                    
            #   Caso o hidrograma de entrada da operacao X for oriundo de um arquivo de entrada fornecido pelo usuario
            else:
                #   Oriundo de uma operacao hidrologica qualquer
                saidaPULS.write(u"\u0009Hidrograma fornecido pelo usuário.\u000A")
                saidaPULS.write(u"\u0009Diretório: '%s'\u000A" %(hidrogramas_entrada_puls[ii].decode('latin_1')))
    #   Finalizacao
    saidaPULS.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    #   faz parte do cabecalho do programa
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   Se essa operacao for de Puls.... == 2
        if codigo_operacoes_hidrologicas[ii] == 2:
            
            #   Saber qual e' o indice correto para a matriz de saida de dados
            indice_saida = ordp.index(ii)
            saidaPULS.write(u"Operação hidrológica número: %d\u000A\u000A" %(ii+1))
            
            #   Se entrar neste loop e' porque o hidrograma de entrada do puls que sera' escrito e' oriundo de outra operacao
            if (type(hidrogramas_entrada_puls[ii]) == int): 
                
                #   Tenho que descobrir se e' oriundo de um chuva-vazao, puls ou mkc (nao incluso ainda)
                if (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 1): #e' oriundo de chuva-vazao
                    #   Se entrou aqui, e' porque o hidrograma de entrada do puls ii e' oriundo de uma operacao chuva-vazao
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordpq.index(hidrogramas_entrada_puls[ii])
                    #   Cabecalho
                    saidaPULS.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaPULS.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_pq[indice_entrada][jj], hidrogramas_saida_puls[indice_saida][jj]) ) #escrever os intervalos
            
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de puls tambem
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 2): #se e' oriundo de outro PULS
                    #   Se entrou aqui, e' porque o hidrograma de entrada do puls ii e' oriundo de outra operacao de puls
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordp.index(hidrogramas_entrada_puls[ii])
                    #   Cabecalho
                    saidaPULS.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaPULS.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_puls[indice_entrada][jj], hidrogramas_saida_puls[indice_saida][jj]) ) #escrever os intervalos
                
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de muskigun-cunge
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 3): #se e' oriundo de MKC
                    #   Se entrou aqui, e' porque o hidrograma de entrada do puls ii e' oriundo de outra operacao de mkc
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordm.index(hidrogramas_entrada_puls[ii])
                    #   Cabecalho
                    saidaPULS.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaPULS.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_m[indice_entrada][jj], hidrogramas_saida_puls[indice_saida][jj]) ) #escrever os intervalos
                
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de JUNCAO
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_puls[ii])] == 4): #se e' oriundo de JUNCAO
                    #   Se entrou aqui, e' porque o hidrograma de entrada do puls ii e' oriundo de outra operacao de juncao
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordj.index(hidrogramas_entrada_puls[ii])
                    #   Cabecalho
                    saidaPULS.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaPULS.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_j[indice_entrada][jj], hidrogramas_saida_puls[indice_saida][jj]) ) #escrever os intervalos
                
            #   Hidrograma de entrada do puls a ser escrito e' fornecido pelo usuario, em um arquivo de texto que deve ser lido novamente (troco memoria por velocidade de processamento)
            else: 
                #   Eu sei que e' um hidrograma valido pq eu ja' li ele antes pra fazer os calculos, portanto nao preciso testa'-lo
                #   Pegar o diretorio do arquivo de chuva observada
                diretorio_arquivo = hidrogramas_entrada_puls[ii]
                #   Ler valores
                hidrograma_usado_neste_puls = lerSerieObservada(diretorio_arquivo, numero_intervalos_tempo)
                #   Cabecalho
                saidaPULS.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                #   Corpo
                for jj in xrange(numero_intervalos_tempo):
                    saidaPULS.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), float(hidrograma_usado_neste_puls[jj]), hidrogramas_saida_puls[indice_saida][jj]) ) #escrever os intervalos
            #   Finalizacao
            saidaPULS.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
            
    #   Feche o arquivo...
    saidaPULS.close()
#----------------------------------------------------------------------