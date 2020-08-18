# -*- coding: latin_1 -*-

#----------------------------------------------------------------------
#   Funcao para criar as variaveis de saida de hidrograma
def gerarVariaveisSaidaMKC(codigo_operacoes_hidrologicas, numero_intervalos_tempo):
    """Cria a matriz de saida para calcular as operacoes MKC"""
    #   Import...        
    from numpy import array, float64
    
    #   Contador
    numero_operacoes_mkc = 0
    #   Conte as operacoes MKC:
    for i in xrange(len(codigo_operacoes_hidrologicas)):
        #   3 e' MKC
        if codigo_operacoes_hidrologicas[i] == 3:
            #   Conte...
            numero_operacoes_mkc += 1
    
    #   Variavel que armazena os hidrogramas gerados pelo chuva-vazao ...
        hidrogramas_saida_mkc = array([[0.0 for i in xrange(numero_intervalos_tempo)] for y in xrange(numero_operacoes_mkc)], float64)

    #   Retorne
    return hidrogramas_saida_mkc
#----------------------------------------------------------------------------------
#   Variavel para pegar o hidrograma de entrada para rodar o MKC
def preparacaoMKC(numero_intervalos_tempo, hidrogramas_entrada_mkc, operacao_a_calcular, ordpq, ordp, ordm, ordj, hidsaipq, hidsaip, hidsaim, hidsaij):
    #   Import...        
    from numpy import array, float64
    
    #   Declarar
    hidrograma_usado_neste_mkc = array([0.0 for i in xrange(numero_intervalos_tempo)], float64)
    
    #   Aqui comeco a analise: Ver se o hidrograma de entrada e' oriund ode outra operacao hidrologica
    if (type(hidrogramas_entrada_mkc[operacao_a_calcular]) == int):
        #   Ver se e' oriunda da operacao de PQ
        if hidrogramas_entrada_mkc[operacao_a_calcular] in ordpq:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordpq.index(hidrogramas_entrada_mkc[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_mkc = hidsaipq[ind_hid]
        
        #   Ver se e' oriunda da operacao de PULS
        elif hidrogramas_entrada_mkc[operacao_a_calcular] in ordp:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordp.index(hidrogramas_entrada_mkc[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_mkc = hidsaip[ind_hid]
            
        #   Ver se e' oriunda da operacao de MKC
        elif hidrogramas_entrada_mkc[operacao_a_calcular] in ordm:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordm.index(hidrogramas_entrada_mkc[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_mkc = hidsaim[ind_hid]
    
        #   Ver se e' oriunda da operacao de JUNC
        elif hidrogramas_entrada_mkc[operacao_a_calcular] in ordj:
            #   Faz parte dessa operacao, pegar o indice
            ind_hid = ordj.index(hidrogramas_entrada_mkc[operacao_a_calcular])
            #   Pegar seus valores
            hidrograma_usado_neste_mkc = hidsaij[ind_hid]
    
    #   Ele e' oriundo de um arquivo de texto
    else:
        #   Declarar
        hidrograma_usado_neste_mkc = array([0.0 for i in xrange(numero_intervalos_tempo)], float64)
        #   Contar o numero de linhas do arquivo da curva cota-volume
        numero_linhas  = sum(1 for linha in open(hidrogramas_entrada_mkc[operacao_a_calcular],'r')) 
        #   Abra o arquivo
        arquivo_hidrograma = open(hidrogramas_entrada_mkc[operacao_a_calcular], 'r') #abrir o arquivo para le-lo.
        
        #   Loop para ler linhas do arquivo
        for linha in xrange(numero_linhas):
            #   Ler a linha
            conteudo_hidrograma = arquivo_hidrograma.readline().split(";")            #ler a linha e dividir 
            #   Armazenar seu valor
            hidrograma_usado_neste_mkc[linha] = float(conteudo_hidrograma[0])        #valores de hidrograma
        #   Fechar o arquivo -> poupar memoria.
        arquivo_hidrograma.close()
    
    return hidrograma_usado_neste_mkc
#----------------------------------------------------------------------------------
#   Funcao para calcular as variaveis de saida de hidrograma
def calcularOperacaoMKC(hidrograma_entrada, duracao_intervalo_tempo, numero_intervalos_tempo, diferenca_cota, comprimento_canal, largura_canal, coef_rugosidade, nome_operacao_hidrologica, numero_operacao, diretorio_saida, gerar_plotagens):
    #   Import
    from Hydrolib import aplicar_MuskingunCunge
    #   Aplicar MKC
    hidrograma_resultante = aplicar_MuskingunCunge(hidrograma_entrada, numero_intervalos_tempo, duracao_intervalo_tempo, diferenca_cota, comprimento_canal, largura_canal, coef_rugosidade)
    ##   Graficos
    #if gerar_plotagens == 1:
    #    #...
    #    Hydrolib.plotar_Hidrogramas_PULS( HIDROGRAMA_ENTRA, HIDROGRAMA_SAI, NUMERO_INTERVALOS_TEMPO, self.caminho_arquivo_entrada, NOMES_OPERACOES_HIDROLOGICAS, numero_do_grafico )
    #   Retornar hidrograma de saida
    return hidrograma_resultante
#----------------------------------------------------------------------------------
#   Escreva o arquivo de saida para as operacoes de MKC
def escreverSaidaMKC(numero_intervalos_tempo, duracao_intervalo_tempo, numero_operacoes_hidrologicas, codigo_operacoes_hidrologicas, hidrogramas_entrada_mkc, hidrogramas_saida_pq, hidrogramas_saida_puls, hidrogramas_saida_mkc, ordpq, ordp, ordm, ordj, diretorio_saida, nome_arquivo, nomes_operacoes):
    #   Import...
    from os import path
    from numpy import argmax
    import codecs
    
    #   Preparo arquivo de saida
    diretorio_saida = str(diretorio_saida + "/Saida_MKC_" + nome_arquivo + ".ohy")
    saidaMKC = codecs.open(diretorio_saida, mode='w', buffering=0, encoding='latin_1')

    #   Cabecalho
    saidaMKC.write(u"\u000A                          MODELO HYDROLIB\u000A                     RESULTADOS DA MODELAGEM")
    saidaMKC.write(u"\u000A------------------------------------------------------------------------\u000A")
    
    #   Escrevo os parametros no arquivo de saida
    saidaMKC.write(u"\u000A ---- PARAMETROS GERAIS DA SIMULAÇÃO  ----\u000A\u000A")
    saidaMKC.write(u"Número de intervalos de tempo            = %d\u000A" %(numero_intervalos_tempo))
    saidaMKC.write(u"Duração do intervalo de tempo (segundos) = %d\u000A" %(duracao_intervalo_tempo))
    saidaMKC.write(u"Número total de simulações hidrológicas  = %d\u000A" %(len(codigo_operacoes_hidrologicas)))
    saidaMKC.write(u"Número de simulações de Muskingun-Cunge  = %d\u000A" %(len(hidrogramas_saida_mkc)))
    saidaMKC.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    saidaMKC.write(u" ---- INFORMAÇÕES DAS SIMULAÇÕES DE PROPAGAÇÃO DE MUSKINGUN-CUNGE ---- \u000A")
    #   Loop para escrever as informacoes
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   Se o codigo dizer que e' MKC....
        if codigo_operacoes_hidrologicas[ii] == 3:
            #   Cabecalho da operacao
            saidaMKC.write(u"\u000AHidrograma %d:%s\u000A" %((ii+1), nomes_operacoes[ii].decode('latin_1')))
            
            #   Se entrar neste loop e' porque o hidrograma de entrada do mkc que sera' escrito e' oriundo de outra operacao
            if (type(hidrogramas_entrada_mkc[ii]) == int): 
                #   Oriundo de uma operacao hidrologica qualquer
                saidaMKC.write(u"\u0009Número do hidrograma de entrada = %d\u000A" %(hidrogramas_entrada_mkc[ii] + 1))
                
                #   Tenho que descobrir se e' oriundo de um chuva-vazao, puls ou mkc (nao incluso ainda)
                if (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 1):
                    #   e' oriundo de chuva-vazao
                    saidaMKC.write(u"\u0009Hidrograma oriundo de uma operação de chuva-vazão.\u000A")
                    
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de puls tambem
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 2):
                    #   se e' oriundo de outro PULS
                    saidaMKC.write(u"\u0009Hidrograma oriundo de uma operação de propagação de reservatórios de Puls.\u000A")
                    
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de muskigun-cunge
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 3):
                    #   se e' oriundo de MKC
                    saidaMKC.write(u"\u0009Hidrograma oriundo de uma operação de propagação de canais de Muskingun-Cunge.\u000A")
                    
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de JUNCAO
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 4):
                    #  se e' oriundo de JUNCAO
                    saidaMKC.write(u"\u0009Hidrograma oriundo de uma operação de junção entre hidrogramas.\u000A")
                    
            #   Caso o hidrograma de entrada da operacao X for oriundo de um arquivo de entrada fornecido pelo usuario
            else:
                #   Oriundo de uma operacao hidrologica qualquer
                saidaMKC.write(u"\u0009Hidrograma fornecido pelo usuário.\u000A")
                saidaMKC.write(u"\u0009Diretório: '%s'\u000A" %(hidrogramas_entrada_mkc[ii].decode('latin_1')))
    #   Finalizacao
    saidaMKC.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    #   faz parte do cabecalho do programa
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   Se essa operacao for de MKC.... == 3
        if codigo_operacoes_hidrologicas[ii] == 3:
            
            #   Saber qual e' o indice correto para a matriz de saida de dados
            indice_saida = ordm.index(ii)
            saidaMKC.write(u"Operação hidrológica número: %d\u000A\u000A" %(ii+1))
            
            #   Se entrar neste loop e' porque o hidrograma de entrada do mkc que sera' escrito e' oriundo de outra operacao
            if (type(hidrogramas_entrada_mkc[ii]) == int): 
                
                #   Tenho que descobrir se e' oriundo de um chuva-vazao, puls ou mkc (nao incluso ainda)
                if (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 1): #e' oriundo de chuva-vazao
                    #   Se entrou aqui, e' porque o hidrograma de entrada do mkc ii e' oriundo de uma operacao chuva-vazao
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordpq.index(hidrogramas_entrada_mkc[ii])
                    #   Cabecalho
                    saidaMKC.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaMKC.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_pq[indice_entrada][jj], hidrogramas_saida_mkc[indice_saida][jj]) ) #escrever os intervalos
            
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de puls 
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 2): #se e' oriundo de outro PULS
                    #   Se entrou aqui, e' porque o hidrograma de entrada do mkc ii e' oriundo de outra operacao de puls
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordp.index(hidrogramas_entrada_mkc[ii])
                    #   Cabecalho
                    saidaMKC.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaMKC.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_puls[indice_entrada][jj], hidrogramas_saida_mkc[indice_saida][jj]) ) #escrever os intervalos
                
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de muskigun-cunge
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 3): #se e' oriundo de MKC
                    #   Se entrou aqui, e' porque o hidrograma de entrada do mkc ii e' oriundo de outra operacao de mkc
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordm.index(hidrogramas_entrada_mkc[ii])
                    #   Cabecalho
                    saidaMKC.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaMKC.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_mkc[indice_entrada][jj], hidrogramas_saida_mkc[indice_saida][jj]) ) #escrever os intervalos
                
                #   Caso o hidrograma de entrada da operacao X for oriundo da operacao Y que por sua vez e' de JUNCAO
                elif (codigo_operacoes_hidrologicas[(hidrogramas_entrada_mkc[ii])] == 4): #se e' oriundo de JUNCAO
                    #   Se entrou aqui, e' porque o hidrograma de entrada do mkc ii e' oriundo de outra operacao de juncao
                    #   Temos que descobrir qual e' o hidrograma que e' usado...
                    indice_entrada = ordj.index(hidrogramas_entrada_mkc[ii])
                    #   Cabecalho
                    saidaMKC.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                    #   Corpo
                    for jj in xrange(numero_intervalos_tempo):
                        saidaMKC.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), hidrogramas_saida_j[indice_entrada][jj], hidrogramas_saida_mkc[indice_saida][jj]) ) #escrever os intervalos
                
            #   Hidrograma de entrada do mkc a ser escrito e' fornecido pelo usuario, em um arquivo de texto que deve ser lido novamente (troco memoria por velocidade de processamento)
            else: 
                #   Eu sei que e' um hidrograma valido pq eu ja' li ele antes pra fazer os calculos, portanto nao preciso testa'-lo
                #   Pegar o diretorio do arquivo de chuva observada
                diretorio_arquivo = hidrogramas_entrada_mkc[ii]
                #   Ler valores
                hidrograma_usado_neste_mkc = lerSerieObservada(diretorio_arquivo, numero_intervalos_tempo)
                #   Cabecalho
                saidaMKC.write(u"      dt, Hidro_Entrada, Hidrogr_Saida\u000A")
                #   Corpo
                for jj in xrange(numero_intervalos_tempo):
                    saidaMKC.write(u"%8d,%14.5f,%14.5f\u000A" %((jj+1), float(hidrograma_usado_neste_mkc[jj]), hidrogramas_saida_mkc[indice_saida][jj]) ) #escrever os intervalos
            #   Finalizacao
            saidaMKC.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    #   Feche o arquivo...
    saidaMKC.close()
#----------------------------------------------------------------------