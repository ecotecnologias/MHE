# -*- coding: latin_1 -*-

from sys import stdout

#----------------------------------------------------------------------
def progressBar(n, nmax):
    """"""
    #   proporcoes
    progresso = int((float(n+1)/(nmax))*50)
    faltante = 50 - progresso
    #   inicio
    b = "\t|"
    #   progresso
    for ii in xrange(progresso):
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
    stdout.write(b + "\r")
#----------------------------------------------------------------------
#   Funcao para criar as variaveis de saida de hidrograma
def gerarVariaveisSaidaPQ(codigo_chuvas, codigo_operacoes_hidrologicas, numero_intervalos_tempo, chuvas_entrada_pq, numero_chuvas, numero_intervalos_tempo_chuva, duracao_intervalo_tempo, parametro_a, parametro_b, parametro_c, parametro_d, limites_idf, posicao_pico, tempo_retorno, diretorios_chuvas):
    """Cria a matriz de saida para calcular as operacoes PQ e cria (e calcula aqui mesmo) a matriz de chuvas utilizadas nessas operacoes (chuva-vazao)"""
    #   Import...        
    from numpy import array, float64
    from sys import exit
    from Leitura import checarIntegridadeArquivoTexto, lerSerieObservada
    
    #   Contador
    numero_operacoes_pq = 0
    #   Conte as operacoes PQ:
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   1 e' PQ
        if codigo_operacoes_hidrologicas[ii] == 1:
            #   Conte...
            numero_operacoes_pq += 1
    
    #   Variavel que armazena os hidrogramas gerados pelo chuva-vazao ...
    hidrogramas_saida_pq   = array([[0.0 for ii in xrange(numero_intervalos_tempo)] for y in xrange(numero_operacoes_pq)], float64)
    precipitacoes_efetivas = array([[0.0 for ii in xrange(numero_intervalos_tempo)] for y in xrange(numero_operacoes_pq)], float64)
    
    #   Contador
    precipitacoes_pq = []
    #   Logica para verificar quantas series de Pord serao necessarias (objetivo: alcancar o menor numero possivel. Se alguma repetir, nao calcularemos de novo);
    for ii in xrange(len(codigo_operacoes_hidrologicas)):
        #   Ou seja, se for operacao PQ ->E<- ela nao esta' nas numero_pord;
        if ((codigo_operacoes_hidrologicas[ii] == 1) and (not chuvas_entrada_pq[ii] in precipitacoes_pq)): 
            #   aqui eu terei somente UM numero de cada posto que FOR DA OPERACAO PQ
            precipitacoes_pq.append(chuvas_entrada_pq[ii]) 
    
    #   Variavel que armazena valores de precipitacao ordenada: Nao repita chuvas
    precipitacoes_ordenadas = array([[0.0 for x in xrange(numero_intervalos_tempo_chuva)] for y in xrange(len(precipitacoes_pq))], float64)
    
    print "\n\tGerando series de chuva."
    
    #   Inicializar barra: Pra inicializar precisa dar +1 no limite
    progressBar(0, numero_chuvas+1)
    
    #   Loop para declaracao das variaveis de chuva das operacoes chuva-vazao
    for chuva in xrange(numero_chuvas):
        #   Testar se a chuva e' observada ou nao
        if codigo_chuvas[chuva] == 1:
            #   Atualizar o indice para pegar a referencia do lugar certo
            indice_idf = precipitacoes_pq[chuva]
            #   E' chuva de IDF, calcular com a funcao;
            precipitacoes_ordenadas[chuva] = calcularChuvasOrdenadas(numero_intervalos_tempo_chuva, duracao_intervalo_tempo, parametro_a[indice_idf], parametro_b[indice_idf], parametro_c[indice_idf], parametro_d[indice_idf], limites_idf[indice_idf], posicao_pico[indice_idf], tempo_retorno[indice_idf])
        
        #   Testar se a chuva e' observada ou nao
        elif codigo_chuvas[chuva] == 0:
            #   Pegar o diretorio do arquivo de chuva observada
            diretorio_arquivo = diretorios_chuvas[chuva]
            ##   Testar integridado do arquivo de chuva fornecido
            integridade_arquivo, linha = checarIntegridadeArquivoTexto(diretorio_arquivo, numero_intervalos_tempo_chuva)
            
            #
            if integridade_arquivo == True:
                #   Ler valores
                precipitacoes_ordenadas[chuva] = lerSerieObservada(diretorio_arquivo, numero_intervalos_tempo_chuva)
                
            else: #   Deu ruim
                #   Finalizo a barra de progresso
                progressBar(numero_chuvas, numero_chuvas); print "\n\n"
                #   Que ruim que deu?
                if linha == 0: #    Numero de dados incorretos
                    print("Foi detectado um erro na leitura da chuva %d.\nReveja os dados de entrada." %(chuva+1))
                    showerror("Erro no arquivo fornecido","O arquivo fornecido para a chuva %d não possui %d linhas (que é o número de intervalos de tempo com chuva da simulação)." %((chuva+1), numero_intervalos_tempo_chuva))
                    showerror("Erro na leitura de chuvas","A simulação não pode continuar sem a informação da chuva %d.\nFaça as correções necessárias e tente novamente.\n\nO modelo será finalizado." %(chuva+1))
                    exit()
                
                else: # Linha X e' o problema
                    print("Foi detectado um erro na leitura da chuva %d.\nReveja os dados de entrada." %(chuva+1))
                    showerror("Erro no arquivo fornecido","Erro na linha %d.\nO arquivo fornecido para a chuva %d não obedece os padrões utilizados pelo programa.\n\nDica: As linhas devem possuir o seguinte padrão: 'valor do dado;'." %(linha, (chuva+1)))
                    showerror("Erro na leitura de chuvas","A simulação não pode continuar sem a informação da chuva %d.\nFaça as correções necessárias e tente novamente.\n\nO modelo será finalizado." %(chuva+1))
                    exit()
        
        #   Something went wrong...
        else:
            progressBar(numero_chuvas, numero_chuvas); print "\n\n"
            print("Foi detectado um erro na leitura da chuva %d.\nCodigo inexistente: %d\nReveja os dados de entrada." %((chuva+1), codigo_chuvas[chuva]))
            showerror("Erro na leitura de chuvas","Código %d inexistente (chuva %d).\n\nO modelo será finalizado." %(codigo_chuvas[chuva], (chuva+1)));
            exit()
        
        #   Atualizar barra
        progressBar(chuva, numero_chuvas)
            
    #   Retorne
    return hidrogramas_saida_pq, precipitacoes_ordenadas, precipitacoes_efetivas
#----------------------------------------------------------------------------------
#   Funcao para criar as variaveis de chuva utilizadas
def calcularChuvasOrdenadas(numero_intervalos_tempo_chuva, duracao_intervalo_tempo, parametro_a, parametro_b, parametro_c, parametro_d, limite_idf, posicao_pico, tempo_retorno):
    #   Import
    from Hydrolib import calcular_PrecipitacaoDesacumulada, aplicar_BlocosAlternados
    #   Calcule a precipitacao desacumulada
    precipitacao_artificial = calcular_PrecipitacaoDesacumulada(numero_intervalos_tempo_chuva, duracao_intervalo_tempo, tempo_retorno, parametro_a, parametro_b, parametro_c, parametro_d, limite_idf)
    #   Transforme-a em ordenada
    precipitacao_artificial = aplicar_BlocosAlternados(precipitacao_artificial, numero_intervalos_tempo_chuva, posicao_pico)
    #   Retorne
    return precipitacao_artificial
#----------------------------------------------------------------------------------
#   Funcao para calcular as variaveis de saida de hidrograma
def calcularOperacaoPQ(numero_intervalos_tempo, duracao_intervalo_tempo, numero_intervalos_tempo_chuva, nome_operacao_hidrologica, coeficiente_cn, area_km2, tc_horas, precipitacao_ordenada, numero_operacao, diretorio_saida, gerar_plotagens):
    #   Import
    from Hydrolib import calcular_PrecipitacaoEfetiva_CN, calcular_HUT_SCS, aplicar_Convolucao, plotar_Hidrogramas_PQ
    #   Calcular a Precipitacao Efetiva
    precipitacao_efetiva = calcular_PrecipitacaoEfetiva_CN(coeficiente_cn, precipitacao_ordenada, numero_intervalos_tempo, numero_intervalos_tempo_chuva)
    #   Calcular HUT da operacao
    tempo_subida, vazao_pico_hut, tempo_base = calcular_HUT_SCS(tc_horas, area_km2, duracao_intervalo_tempo) #Caracteristicas do HUT para convolucao
    #   Calular Hidrograma da operacao
    hidrograma_resultante = aplicar_Convolucao(tempo_base, vazao_pico_hut, tempo_subida, duracao_intervalo_tempo, numero_intervalos_tempo, precipitacao_efetiva) #Convolucao para HUT
    ##   Graficos
    #if gerar_plotagens == 1:
    #    #...
    #    plotar_Hidrogramas_PQ(hidrograma_resultante, precipitacao_ordenada, precipitacao_efetiva, numero_intervalos_tempo, duracao_intervalo_tempo, diretorio_saida, nome_operacao_hidrologica, numero_operacao)
    #   Retorne
    return hidrograma_resultante, precipitacao_efetiva
#----------------------------------------------------------------------------------
#   Escreva o arquivo de saida para as operacoes de PQ
def escreverSaidaPQ(numero_intervalos_tempo, duracao_intervalo_tempo, numero_intervalos_tempo_chuva, numero_operacoes_hidrologicas, codigo_operacoes_hidrologicas, coeficiente_cn, area_km2, tc_horas, chuvas_entrada_pq, precipitacoes_ordenadas, hidrogramas_saida_pq, precipitacoes_efetivas, diretorio_saida, nome_arquivo, nomes_operacoes):
    #   IMport...
    from os import path
    from numpy import argmax
    import codecs
    
    #   Preparo arquivo de saida
    diretorio_saida = str(diretorio_saida + "/Saida_Chuva-vazao_" + nome_arquivo + ".ohy")
    saidaPQ = codecs.open(diretorio_saida, mode='w', buffering=0, encoding='latin_1')

    #   Cabecalho
    saidaPQ.write(u"\u000A                         MODELO HYDROLIB\u000A                     RESULTADOS DA MODELAGEM")
    saidaPQ.write(u"\u000A------------------------------------------------------------------------\u000A")

    #   Escrevo os parametros no arquivo de saida
    saidaPQ.write(u"\u000A ---- PARAMETROS GERAIS DA SIMULACAO  ----\u000A\u000A")
    saidaPQ.write(u"Número de intervalos de tempo            = %d\u000A" %(numero_intervalos_tempo))
    saidaPQ.write(u"Número de intervalos de tempo com chuva  = %d\u000A" %(numero_intervalos_tempo_chuva))
    saidaPQ.write(u"Duração do intervalo de tempo (segundos) = %d\u000A" %(duracao_intervalo_tempo))
    saidaPQ.write(u"Número total de simulações hidrológicas  = %d\u000A" %(len(codigo_operacoes_hidrologicas)))
    saidaPQ.write(u"Número de simulações chuva-vazão         = %d\u000A" %(len(hidrogramas_saida_pq)))
    saidaPQ.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    saidaPQ.write(u" ---- INFORMAÇÕES DAS SIMULAÇÕES CHUVA-VAZÃO ---- \u000A")
    #   faz parte do cabecalho do programa
    for ii in xrange( len(codigo_operacoes_hidrologicas) ):
        #   Se o codigo dizer que e' PQ....
        if codigo_operacoes_hidrologicas[ii] == 1:
            saidaPQ.write(u"\u000AHidrograma %d:%s\u000A" %((ii+1), nomes_operacoes[ii].decode('latin_1')))
            saidaPQ.write(u"\u0009Calculada a partir da chuva de projeto: %d\u000A" %(chuvas_entrada_pq[ii] + 1))
            saidaPQ.write(u"\u0009       Coeficiente CN = %10.4f [  -  ]\u000A" %(coeficiente_cn[ii]))
            saidaPQ.write(u"\u0009        Área da bacia = %10.4f [ km² ]\u000A" %(area_km2[ii]))
            saidaPQ.write(u"\u0009Tempo de concentração = %10.4f [horas]\u000A" %(tc_horas[ii]))
    saidaPQ.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    
    saidaPQ.write(u" ---- VAZÕES DE PICO (m³/s) E VOLUMES ESCOADOS (m³) ----\u000A")
    #   Organizacao do arquivo de saida
    for ii in xrange(len(hidrogramas_saida_pq)):
        #   Declarar/resetar
        volume_hidrograma = 0.
        #   Calcular o volume
        for jj in xrange(numero_intervalos_tempo-1):
            #   Metodo dos retangulos
            volume_hidrograma += (((hidrogramas_saida_pq[ii][jj] + hidrogramas_saida_pq[ii][jj+1])/2.) * duracao_intervalo_tempo)
        #   SpaguettiSpaguettiSpaguettiSpaguettiSpaguettiSpaguetti.. Youcandoanythingifyousetyourmindtoman
        saidaPQ.write(u"\u000AHidrograma %d:%s\u000A" %((ii+1), nomes_operacoes[ii].decode('latin_1')))
        saidaPQ.write(u"\u0009Vazão de pico   = %.4f [m³/s]\u000A" %(max(hidrogramas_saida_pq[ii])))
        saidaPQ.write(u"\u0009Posicao do pico = %d (em %d segundos)\u000A" %((argmax(hidrogramas_saida_pq[ii])+1), (argmax(hidrogramas_saida_pq[ii])*duracao_intervalo_tempo)))
        saidaPQ.write(u"\u0009Volume escoado  = %.4f [m³]\u000A" %(volume_hidrograma))

        
    #   Deixar espaco em branco apos \u000A
    saidaPQ.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    saidaPQ.write(u" ---- CHUVAS DE PROJETO (mm) ---- \u000A\u000A")
    #   Precisa ser declarada
    string_aux = u"      dt"
    #   Organizacao do arquivo de saida
    for ii in xrange(len(precipitacoes_ordenadas)):
        #   100 ou mais
        if ii >= 99: #      "  Chuva 100"
            string_aux += (u"   Chuva%4d"%(ii+1))
        #   10 a 99
        elif ii >= 9: #     "  Chuva 10"
            string_aux += (u"   Chuva%3d"%(ii+1))
        #   1 a 9
        else:          #   "  Chuva 1"
            string_aux += (u"   Chuva%2d"%(ii+1))

    #   Organizacao do arquivo de saida
    saidaPQ.write(string_aux)
    saidaPQ.write(u"\u000A")
 
    #   Escrevo a chuva no arquivo de saida
    print "\n\tEscrevendo series de chuva de projeto no arquivo de saida."
    
    #   Loop para escrever a chuva
    for jj in xrange(numero_intervalos_tempo_chuva):
        #   Escrever o intervalo na esquerda do arquivo
        saidaPQ.write(u"%8d" %int(jj+1))
        #   Loop para esrever a chuva
        for ii in xrange(len(precipitacoes_ordenadas)):
            #   100 ou mais
            if ii >= 99:
                saidaPQ.write(u"%12.4f" %(precipitacoes_ordenadas[ii][jj]))
            #   10 a 99
            elif ii >= 9:
                saidaPQ.write(u"%11.4f" %(precipitacoes_ordenadas[ii][jj]))
            #   1 a 9
            else:
                saidaPQ.write(u"%10.4f" %(precipitacoes_ordenadas[ii][jj]))
        #   Nova linha
        saidaPQ.write(u"\u000A")
    
    
    #   Deixar espaco em branco apos \u000A
    saidaPQ.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    saidaPQ.write(u" ---- CHUVAS EFETIVAS (mm) ---- \u000A\u000A")
    #   Precisa ser declarada
    string_aux = u"      dt"
    #   Organizacao do arquivo de saida
    for ii in xrange(len(precipitacoes_efetivas)):
        #   100 ou mais
        if ii >= 99: #      "  Chuva 100"
            string_aux += (u"   Chuva%4d"%(ii+1))
        #   10 a 99
        elif ii >= 9: #     "  Chuva 10"
            string_aux += (u"   Chuva%3d"%(ii+1))
        #   1 a 9
        else:          #   "  Chuva 1"
            string_aux += (u"   Chuva%2d"%(ii+1))

    #   Organizacao do arquivo de saida
    saidaPQ.write(string_aux)
    saidaPQ.write(u"\u000A")
    
    #   Escrevo a chuva no arquivo de saida
    print "\n\tEscrevendo series de chuva efetiva no arquivo de saida."
    
    #   Loop para escrever a chuva
    #   Apesar da variavel "precipitacoes_efetivas" terem "numero_intervalos_tempo" termos, escreveremos somente ate' "numero_intervalos_tempo_chuva" pois o excedente e' ZERO.
    for jj in xrange(numero_intervalos_tempo_chuva): 
        #   Escrever o intervalo na esquerda do arquivo
        saidaPQ.write(u"%8d" %int(jj+1))
        #   Loop para esrever a chuva
        for ii in xrange(len(precipitacoes_efetivas)):
            #   100 ou mais
            if ii >= 99:
                saidaPQ.write(u"%12.4f" %(precipitacoes_efetivas[ii][jj]))
            #   10 a 99
            elif ii >= 9:
                saidaPQ.write(u"%11.4f" %(precipitacoes_efetivas[ii][jj]))
            #   1 a 9
            else:
                saidaPQ.write(u"%10.4f" %(precipitacoes_efetivas[ii][jj]))
        #   Nova linha
        saidaPQ.write(u"\u000A")

        
    saidaPQ.write(u"\u000A------------------------------------------------------------------------\u000A\u000A")
    saidaPQ.write(u" ---- HIDROGRAMAS CHUVA-VAZAO (m³/s) ----\u000A\u000A")
    #   Precisa ser declarada
    string_aux = u"      dt"
    #   Organizacao do arquivo de saida
    for ii in xrange(len(hidrogramas_saida_pq)):
        #   100 ou mais
        if ii >= 99: #      "  Hidrograma 100"
            string_aux += (u"   Hidrograma%4d"%(ii+1))
        #   10 a 99
        elif ii >= 9: #     "  Hidrograma 10"
            string_aux += (u"   Hidrograma%3d"%(ii+1))
        #   1 a 9
        else:          #   "  Hidrograma 1"
            string_aux += (u"   Hidrograma%2d"%(ii+1))

    #   Organizacao do arquivo de saida
    saidaPQ.write(string_aux)
    saidaPQ.write(u"\u000A")
    
    #   Escrevo a chuva no arquivo de saida
    print "\n\tEscrevendo os hidrogramas das operacoes chuva-vazao no arquivo de saida."
    
    #   Loop para escrever o hidrograma
    for jj in xrange(numero_intervalos_tempo):
        #   Escrever o intervalo na esquerda do arquivo
        saidaPQ.write(u"%8d" %(jj+1))
        #   Loop para escrever o hidrograma
        for ii in xrange(len(hidrogramas_saida_pq)):
            #   100 ou mais
            if ii >= 99:
                saidaPQ.write(u"%17.5f" %(hidrogramas_saida_pq[ii][jj]))
            #   10 a 99
            elif ii >= 9:
                saidaPQ.write(u"%16.5f" %(hidrogramas_saida_pq[ii][jj]))
            #   1 a 9
            else:
                saidaPQ.write(u"%15.5f" %(hidrogramas_saida_pq[ii][jj]))
        #   Nova linha
        saidaPQ.write(u"\u000A")
    #   Feche o arquivo
    saidaPQ.close()
#----------------------------------------------------------------------