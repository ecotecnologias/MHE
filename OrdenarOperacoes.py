# -*- coding: latin_1 -*-

#----------------------------------------------------------------------
#   Achar qual e' a proxima operacao a ser calculada
def ordenarOperacoes(numero_operacoes_hidrologicas, codigo_operacoes_hidrologicas, controle_operacoes_hidrologicas, hidrogramas_entrada_puls, hidrogramas_entrada_mkc, hidrogramas_juncoes, ordpq, ordp, ordm, ordj):
    """
    Determina qual operacao deve ser calculada em seguida, fazendo com que elas sejam realizadas em uma ordem correta.
    Ressalta-se que essa funcao e' "rodada" a cada nova operacao.
    Retorna o indice da operacao hidrologica que sera' calculada, e as atualiza as listas: controle_operacoes_hidrologicas, ordpq, ordp, ordm, ordj
    """

    #            O algoritmo a seguir serve para que o modelo acerte a ordem de execucao das operacoes hidrologicas, pois desta forma, o usuario
    #    pode entrar com as operacoes em ordem aleatoria, que mesmo assim o programa sabera' qual deve ser calculada antes. A seguir segue um exemplo
    #    de como o algorimo funciona: Operacao 5 recebe o resultado da operacao 9, a operacao 9 por sua vez, precisa do hidrograma gerado pela operacao 3,
    #    entao, o modelo calculara' a operacao 3, em seguida, a operacao 9 e por final a operacao 5. Apos, ele seguira' normalmente, pulando aquelas
    #    operacoes que ja' foram calculadas.
    
    #   Variaveis que vao controlar o algoritmo
    operacao_a_calcular = 0 # Comeca sempre em zero, assim, eu garanto que nao faltara' nenhuma operacao (ao custo de ter que que rodar varios while's ate' achar uma operacao nao calculada).
    decisao = False         # Variavel que diz se o modelo ja' decidiu qual operacao calcular.

    #   Este while roda ate' que encontra-se uma operacao que nao foi realizada ainda, por isso ele esta' dentro do for
    while(decisao == False): # Assumo que o programa nao sabe qual operacao calcular. Este loop e' rodado VARIAS vezes antes de calcular cada operacao.
        
        #   Testar se esta operacao ja' foi calculada
        if controle_operacoes_hidrologicas[operacao_a_calcular] == 1: 
            #   Some 1 para a variavel e tente novamente
            operacao_a_calcular += 1
            #   Decisao continua falsa...
            decisao = False
            
        #   Se a operacao nao foi calculada ainda, verificar os pre-requesitos
        else:
            #   Caso a operacao a ser testada for chuva-vazao
            if codigo_operacoes_hidrologicas[operacao_a_calcular] == 1: # 1 -> Chuva-vazao
                #   Se for chuva vazao, a decisao e' verdadeira, pois as operacoes de chuva-vazao nao necessitam de pre-requesitos (outras operacoes)
                decisao = True
                #   Marcar que a operacao de chuva-vazao sera' realizada
                controle_operacoes_hidrologicas[operacao_a_calcular] = 1
                #   Marcar a ordem que este tipo de operacao e' realizado
                ordpq.append(operacao_a_calcular)
                
            #   Caso a operacao a ser testada for PULS
            elif codigo_operacoes_hidrologicas[operacao_a_calcular] == 2: # 2 -> PULS
                #   O hidrograma de entrada pode ser oriundo de outra operacao ou fornecido pelo usuario por meio de um arquivo de texto.
                
                #   Caso o hidrograma for oriundo de outra operacao: Verificar se ela ja' foi realizada
                if (type(hidrogramas_entrada_puls[operacao_a_calcular]) == int):
                    
                    #   Verificar se a operacao que ele requere ja' foi realizada
                    if controle_operacoes_hidrologicas[(hidrogramas_entrada_puls[operacao_a_calcular])] == 1:
                        #   A operacao requerida ja' foi calculada, tome a decisao e calcule
                        decisao = True
                        #   Marcar que a operacao de chuva-vazao sera' realizada
                        controle_operacoes_hidrologicas[operacao_a_calcular] = 1
                        #   Marcar a ordem que este tipo de operacao e' realizado
                        ordp.append(operacao_a_calcular)
                
                    #   Caso a operacao requerida NAO foi calculada ainda:
                    else:
                        #   Investigue a operacao que e' requesito
                        operacao_a_calcular = hidrogramas_entrada_puls[operacao_a_calcular]
                        #   Decisao continua falsa...
                        decisao = False
                        
                #   Caso o hidrograma de entrada for fornecido pelo usuario por meio de um arquivo de texto - Pode calcular
                else:
                    #   O hidrograma de entrada ja' esta' pronto, e' so' rodar a operacao
                    decisao = True
                    #   Marcar que a operacao de chuva-vazao sera' realizada
                    controle_operacoes_hidrologicas[operacao_a_calcular] = 1
                    #   Marcar a ordem que este tipo de operacao e' realizado
                    ordp.append(operacao_a_calcular)
            
            #   Caso a operacao a ser testada for MKC
            elif codigo_operacoes_hidrologicas[operacao_a_calcular] == 3: # 3 -> MKC
                #   O hidrograma de entrada pode ser oriundo de outra operacao ou fornecido pelo usuario por meio de um arquivo de texto.
                
                #   Caso o hidrograma for oriundo de outra operacao: Verificar se ela ja' foi realizada
                if (type(hidrogramas_entrada_mkc[operacao_a_calcular]) == int):
                    
                    #   Verificar se a operacao que ele requere ja' foi realizada
                    if controle_operacoes_hidrologicas[(hidrogramas_entrada_mkc[operacao_a_calcular])] == 1:
                        #   A operacao requerida ja' foi calculada, tome a decisao e calcule
                        decisao = True
                        #   Marcar que a operacao de chuva-vazao sera' realizada
                        controle_operacoes_hidrologicas[operacao_a_calcular] = 1
                        #   Marcar a ordem que este tipo de operacao e' realizado
                        ordm.append(operacao_a_calcular)
                
                    #   Caso a operacao requerida NAO foi calculada ainda:
                    else:
                        #   Investigue a operacao que e' requesito
                        operacao_a_calcular = hidrogramas_entrada_mkc[operacao_a_calcular]
                        #   Decisao continua falsa...
                        decisao = False
                        
                #   Caso o hidrograma de entrada for fornecido pelo usuario por meio de um arquivo de texto - Pode calcular
                else:
                    #   O hidrograma de entrada ja' esta' pronto, e' so' rodar a operacao
                    decisao = True
                    #   Marcar que a operacao de chuva-vazao sera' realizada
                    controle_operacoes_hidrologicas[operacao_a_calcular] = 1
                    #   Marcar a ordem que este tipo de operacao e' realizado
                    ordm.append(operacao_a_calcular)

            #   Caso a operacao a ser testada for JUNCAO
            elif codigo_operacoes_hidrologicas[operacao_a_calcular] == 4: # 4 -> JUNCAO
                # Aqui a logica muda um pouco: deve-se verificar se os hidrogramas de entrada da juncao ja foram calculados.
                # 1 - Somente se verifica os hidrogramas >= 0;
                # 2 - Se todos os >= 0 ja' estao calculados (os negativos nao existem), eu posso calcular a juncao;
                # 3 - Se durante a verificacao dos hidrogramas >= 0 haver algum nao calculado, decisao = False e se analisa esta operacao (nao calculada).
                
                #   Variaveis que auxiliarao na tomada de decisao
                calcular_juncao = True # Comeco assumindo que pode-se calcular a juncao
                analisar_esta_operacao = [] # Lista que armazena as operacoes nao calculadas - usada SOMENTE se algumas das operacoes verificadas na juncao nao esta calculada.
                
                #   Testar-se-a' hidrograma a hidrograma da juncao
                for hidrograma_juncao in xrange(hidrogramas_juncoes[operacao_a_calcular]):
                    
                    #   Avaliar os hidrogramas que sao oriundos de outras operacoes, pois os que sao dados pelo usuario e' so' fazer
                    if (type(hidrogramas_juncoes[operacao_a_calcular][hidrograma_juncao]) == int):
                        
                        #   Testa-se somente os hidrogramas com numeros maiores ou iguais a zero
                        if not hidrogramas_juncoes[operacao_a_calcular][hidrograma_juncao] < 0:
                            
                            #   Verificar se ja' foi calculada
                            if controle_operacoes_hidrologicas[(hidrogramas_juncoes[operacao_a_calcular][hidrograma_juncao])] == 0:
                                #   Operacao NAO foi calculada, logo, nao posso calcular esta juncao
                                calcular_juncao = False
                                #   Adicionar a operacao nao calculada para ser calculada
                                analisar_esta_operacao.append(hidrogramas_juncoes[operacao_a_calcular][hidrograma_juncao])
                
                #   Verificar se a juncao pode ser calculada
                if calcular_juncao == True:
                    #   A juncao esta' pronta, e' so' rodar a operacao
                    decisao = True
                    #   Marcar que a operacao de chuva-vazao sera' realizada
                    controle_operacoes_hidrologicas[operacao_a_calcular] = 1
                    #   Marcar a ordem que este tipo de operacao e' realizado
                    ordj.append(operacao_a_calcular)
                    
                #   Caso houve alguma operacao/hidrograma que nao esta' pronta/o para ser calculada/o
                else:
                    #   Investigue a operacao que e' requesito, comecando da menor (que vem antes) ate' a maior (que vem depois)
                    operacao_a_calcular = min(analisar_esta_operacao)
                    #   Decisao continua falsa...
                    decisao = False  
                    
            #   Caso a operacao a ser testada for CENARIOS PQ
            elif codigo_operacoes_hidrologicas[operacao_a_calcular] == 5: # 5 -> CENARIOS PQ
                #   Esta modificacao sera' implementada mais tarde
                #   Investigue a proxima operacao, pois esta nao esta' pronta ainda
                operacao_a_calcular += 1
                #   Decisao continua falsa...
                decisao = False  
    
    #   A partir daqui, o modelo ja' sabe qual operacao calcular, o codigo a seguir e' para executar cada operacao hidrologica.  #
    
    #   retorne as variaveis atualizadas
    return operacao_a_calcular, controle_operacoes_hidrologicas, ordpq, ordp, ordm, ordj
#----------------------------------------------------------------------