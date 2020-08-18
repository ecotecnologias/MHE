# -*- coding: latin_1 -*-

##############################################################################################################
#                                                                                                            #
#        Caro leitor,                                                                                        #
#        -Venho por meio deste avisar-te que este programa trata-se de um modelo academico escrito           #
#    por um estudante de engenharia CIVIL, em sua maioria durante a graduacao.                               #
#        -Infelizmente este codigo nao e' um exemplo de boas praticas de programacao (muito pelo contrario), #
#    contudo, o codigo mostrou-se eficaz em cumprir as funcoes as quais foram designadas;                    #
#                                                                                                            #
#        -Apesar de seu codigo confuso e mal escrito, espero que tenhas uma boa experiencia com o software.  #
#        -Nao exite em reportar bugs ao e-mail "vitorgg_hz@hotmail.com"                                      #
#        -Como disse um grande amigo meu, "Se funciona, nao e' idiota" - Eckhardt, R. B.                     #
#                                                                                                   Vitor G. #
################## GLOSSARIO #################################################################################
#                                                                                                            #
#   nint = numero de intervalos de tempo                                                                     #
#   dt = duracao do intervalo de tempo (segundos)                                                            #
#   nch = numero de chuvas                                                                                   #
#   nintch = numeros de intervalos de tempo de chuva                                                         #
#   nop = numero de operacoes hidrologicas                                                                   #
#   cdoh = codigos operacoes hidrologicas PQ- chuva-vazao, PULS - puls, MKC - muskingun cunge                #
#   ctoh = controle das operacoes hidrologicas; 0 - nao realiada; 1- realizada                               #
#   cdch = codigo das chuvas 1 - IDF, 0 - OBS                                                                #
#   nomesop = nome da operacao, vai no grafico se ativado                                                    #
#   lim_idf = limitacao da intensidade de chuva para as chuvas calculadas a partir de IDF (mintuso)          #
#   tidf = tipo da idf                                                                                       #
#   pp = posicao do pico de chuva                                                                            #
#   dirch = diretorio chuva observada                                                                        #
#   chpq = numero da chuva usada na operacao PQ                                                              #
#   difcot = diferenca de cota - m (kirpich)                                                                 #
#   compcan = comprimento canal MKC                                                                          #
#   ccv = curva cota-volume                                                                                  #
#   estp = estruturas da operacao de PULS                                                                    #
#   cotinp = cota inicial do reservatorio PULS                                                               #
#   hidentp = hidrograma de entrada no PULS                                                                  #
#   largcan = largura do canal MKC                                                                           #
#   nmann = coeficiente n de manning MKC                                                                     #
#   hidentm = hidrograma de entrada de MKC                                                                   #
#   hidentj = hidrogram de entrada JUNCAO                                                                    #
#                                                                                                            #
##############################################################################################################

import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
    
from os import path, listdir
from PIL import Image, ImageTk
from OperacaoPQ import gerarVariaveisSaidaPQ, calcularOperacaoPQ, escreverSaidaPQ
from OperacaoPULS import gerarVariaveisSaidaPULS, preparacaoPULS, calcularOperacaoPULS, escreverSaidaPULS
from OperacaoMKC import gerarVariaveisSaidaMKC, preparacaoMKC, calcularOperacaoMKC, escreverSaidaMKC
from OperacaoJUNCAO import gerarVariaveisSaidaJUNCAO, preparacaoJUNCAO, calcularOperacaoJUNCAO, escreverSaidaJUNCAO
from OrdenarOperacoes import ordenarOperacoes
from Leitura import gerenciarLeitura, lerArquivoEntrada, gerenciarLeituraPasta
import Informacoes
import Auxiliar


class Application(Toplevel):
    """"""
    #----------------------------------------------------------------------   
    def __init__(self, master, versao_do_software, diretorio_do_software):
        """Esta funcao para iniciar a janela principal do modelo."""
        #   Sumir com a janelinha, não gosto dela
        master.withdraw()
        
        #   Necessario(?)
        self.master = master
        self.versao_do_software = versao_do_software
        self.diretorio_do_software = diretorio_do_software
        
        #   Fazer a janela
        Toplevel.__init__(self, bg="#DFF9CA")
        
        #self.iconbitmap(self.diretorio_do_software + "/water.ico")
        
        #   Alguns detalhes
        self.resizable(width=False, height=False)
        self.title("MHE - %5.2f" %(versao_do_software))
        self.protocol("WM_DELETE_WINDOW", self.sair)
        
        #   Criar o frame para inserir os widgets
        primeiroFrame = Frame(self, bg="#DFF9CA")
        primeiroFrame.pack(padx = 20, pady = 10)
        
        #   Iniciar o menu de barras
        menubar = Menu(self)
        
        #   Primeiro menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Escrever arquivo de entrada...", command=lambda: self.escreverArquivoEntrada())
        filemenu.add_separator()
        filemenu.add_command(label="Executar um único arquivo de entrada...", command=lambda: self.executarArquivoEntrada(diretorio_do_software, 0))
        filemenu.add_command(label="Executar todos os arquivos de uma pasta...", command=lambda: self.executarArquivoEntrada(diretorio_do_software, 1))
        filemenu.add_separator()
        filemenu.add_command(label="Fechar", command=self.sair)
        menubar.add_cascade(label="Arquivo", menu=filemenu)
        #   Segundo menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Ajuda", foreground="#A9A9A9", activeforeground="#A9A9A9")#, command = self.abrirAjuda)
        helpmenu.add_command(label="Sobre...", command=lambda: self.abrirAbout())
        menubar.add_cascade(label="Informações", menu=helpmenu)
        #   Mostre o menu
        self.config(menu=menubar)   
    
        #   Nome e versao
        cabecalho = Label(primeiroFrame, text = ("MHE  -  Versão: %5.2f" %versao_do_software), bd = 1, relief = "sunken" , anchor = "w", padx = 75)
        cabecalho.grid(row = 0, column = 0, columnspan = 4, pady = 10, padx = 0, ipady = 10, ipadx = 5)
        
        #   Cria a variavel que controla os botoes
        self.plotar_graficos = IntVar()
        self.plotar_graficos.set(0)
        
        #   Cria os botoes pra clicar
        boxPlotar = Checkbutton(primeiroFrame, bg="#DFF9CA", activebackground="#DFF9CA", text = "Plotar resultados", variable = self.plotar_graficos, onvalue = 1, offvalue = 0)
        boxPlotar.grid(row = 1, column = 0, columnspan = 4, sticky = 'n', ipady = 5, ipadx = 69)
    
        #    Bi de ibaaaagens cobandante habilton!
        imagemLogo = ImageTk.PhotoImage(Image.open(diretorio_do_software + "\Logo.png"))
        imagemLabel = Label(primeiroFrame, image=imagemLogo, bg="#DFF9CA")
        imagemLabel.grid(row = 2, column = 0, columnspan = 4, pady = 0, padx = 0)
        imagemLabel.image = imagemLogo
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #----------------------------------------------------------------------
    def centralizar(self, win):
        """
        centraliza uma janela tkinter
        parametro win : root ou Toplevel que sera' centralizada
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = int(win.winfo_screenheight()*0.85) // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
    #----------------------------------------------------------------------
    def sair(self):
        """Sai do software sem dar pau..."""
        self.destroy()
        sys.exit()
    #----------------------------------------------------------------------
    def escreverArquivoEntrada(self):
        """Esta funcao serve pra abrir a entrada do passo-a-passo em uma nova janela."""
        #   Pode fechar a janela principal, sera' reiniciada depois
        self.destroy()
        
        #   Abrir a segunda Janela
        Auxiliar.InterfaceAuxiliar(self.master, self.versao_do_software, self.diretorio_do_software)
        #----------------------------------------------------------------------
    def abrirAbout(self):
        """Esta funcao serve pra abrir a entrada do passo-a-passo em uma nova janela."""
        #   Pode fechar a janela principal, sera' reiniciada depois
        self.destroy()
        
        #   Abrir a segunda Janela
        Informacoes.InterfaceInformacoes(self.master, self.versao_do_software, self.diretorio_do_software)
    #----------------------------------------------------------------------
    def progressBar(self, n, nmax):
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
    def executarArquivoEntrada(self, diretorio_do_software, isFolder):
        """Esta funcao serve para chamar as funcoes da logica do programa (processamento dos dados)."""
        #   Esconder a janelinha, afinal ela fica congelada mesmo.
        self.withdraw()
        
        #   Testar se e' um arquivo ou uma pasta como entrada...
        if isFolder == 0:
            #   Lendo arquivo de entrada ---> diretorio_saida == diretorio de entrada
            diretorios_arquivos_entrada, diretorio_saida = gerenciarLeitura(diretorio_do_software)

        #   Trata-se de uma pasta...
        else:
            #   Ja retorna a lista
            diretorio_pasta_entrada, arquivos_da_pasta = gerenciarLeituraPasta(diretorio_do_software)
            #   Pasta de saida igual da entrada
            diretorio_saida = diretorio_pasta_entrada # ---> diretorio_saida == diretorio de entrada
            #   Corrigir erro
            if not diretorio_pasta_entrada == None:
                #   Criar a lista dos diretorios dos arquivos.
                diretorios_arquivos_entrada = [str(diretorio_pasta_entrada + "/" + arquivos_da_pasta[i]) for i in xrange(len(arquivos_da_pasta))]
            #   Corrigir ero
            else: diretorios_arquivos_entrada = [None]
        
        #   Ver se e' um arquivo mesmo
        if not diretorios_arquivos_entrada[0] == None:
            #   Loop de arquivos
            for arquivo in xrange(len(diretorios_arquivos_entrada)):
                #   Ver se e' um arquivo mesmo
                if not diretorios_arquivos_entrada[arquivo] == None:
                    #   Selecionar ultimo nome
                    nome_arquivo = diretorios_arquivos_entrada[arquivo].split("/")[-1]
                    #   Separar o nome do arquivo
                    nome_arquivo = nome_arquivo.split(".")[0]
                    #   Avisar usuario
                    print "\n\t----------------------------------------------------\n\tArquivo (%d / %d)\n\tNome: %s." %((arquivo+1), (len(diretorios_arquivos_entrada)), (nome_arquivo))
                    
                    #   Pegar as variaveis de entrada... sao muitas, eu sei.... ¯\_(ツ)_/¯... eu abreveiei o maximo que pude..
                    nint, dt, nch, nintch, nop, cdoh, ctoh, cdch, nomesop, a, b, c, d, lim_idf, tidf, pp, tr, dirch, cn, area, tc, chpq, difcot, compcan, ccv, estp, cotinp, hidentp, largcan, nmann, hidentm, hidentj = lerArquivoEntrada(diretorios_arquivos_entrada[arquivo])
                    
                    #   Armazena a ordem que as operacoes sao calculadas: Ajudar na selecao dos hidrogramas para gerar os arquivos de saida
                    #ordop = [None for i in xrange(nop)]
                    ordpq = [] #    Ordem de execucao das operacoes PQ
                    ordp  = [] #    Ordem de execucao das operacoes PULS
                    ordm  = [] #    Ordem de execucao das operacoes MKC
                    ordj  = [] #    Ordem de execucao das operacoes JUNC
                    
                    #   Para operacoes PQ
                    if 1 in cdoh:
                        #   Criar as variaveis de saida
                        hidsaipq, chordpq, chefpq = gerarVariaveisSaidaPQ(cdch, cdoh, nint, chpq, nch, nintch, dt, a, b, c, d, lim_idf, pp, tr, dirch)
                    #   Se nao houver, criar a variavel vazia
                    else:
                        #   Cria as variaveis vazias
                        hidsaipq = chordpq = chefpq = []
                        
                    #   Para operacoes PULS
                    if 2 in cdoh:
                        #   Declarar das variaveis de hidrogramas de PULS
                        hidsaip = gerarVariaveisSaidaPULS(cdoh, nint)
                    #   Se nao houver, criar a variavel vazia
                    else:
                        #   Cria a variavel vazia
                        hidsaip = []
                        
                    #   Para operacoes MKC
                    if 3 in cdoh:
                        #   Declarar das variaveis de hidrogramas de MKC
                        hidsaim = gerarVariaveisSaidaMKC(cdoh, nint)
                    #   Se nao houver, criar a variavel vazia
                    else:
                        #   Cria a variavel vazia
                        hidsaim = []
                        
                    #   Para operacoes JUNCAO
                    if 4 in cdoh:
                        #   Declarar das variaveis de hidrogramas de JUNCAO
                        hidsaij = gerarVariaveisSaidaJUNCAO(cdoh, nint)
                    #   Se nao houver, criar a variavel vazia
                    else:
                        #   Cria a variavel vazia
                        hidsaij = []
        
                    ##   Para operacoes CENARIOS
                    #if 5 in cdoh:
                    #    #   Loop das chuvas de CENARIOS
                    #    #....
                    #    #   Loop das operacoes
                    
                    #   Contadoras de operacoes
                    npq = 0 #   Chuva-Vazao
                    np  = 0 #   Puls
                    nm  = 0 #   Muskingun-Cunge
                    nj  = 0 #   Juncoes
                    nc  = 0 #   Cenarios chuva-vazao
                    
                    print "\n\tCalculando operacoes hidrologicas."
                    
                    #   Inicializar barra: Pra inicializar precisa dar +1 no limite
                    self.progressBar(0, nop+1)
                    
                    #   Loop para rodar operacoes.... selecionar a que deve ser calculada antes e meter bala.
                    for operacao in xrange(nop): #aqui eu coloco a barra de progresso para processos
                        
                        #   Qual operacao e' a proxima?
                        #   Essa funcao e' rodada a cada nova operacao para saber qual deve ser calculada nessa iteracao do for operacao
                        #   A funcao retorna todas as listas, sempre atualizando elas uma a uma
                        #   Poderia ser feito separadamente, mas resultaria em um "for" a mais desnecessario
                        operacao_a_calcular, ctoh, ordpq, ordp, ordm, ordj = ordenarOperacoes(nop, cdoh, ctoh, hidentp, hidentm, hidentj, ordpq, ordp, ordm, ordj)
                        
                        #   Para PQ
                        if cdoh[operacao_a_calcular] == 1:
                            #   Qual precipitacao ordenada utilizar?
                            indice_chuva = chpq[operacao_a_calcular]
                            #   Calcular o hidrograma de saida 
                            hidsaipq[npq], chefpq[npq] = calcularOperacaoPQ(nint, dt, nintch, nomesop[operacao_a_calcular], cn[operacao_a_calcular], area[operacao_a_calcular], tc[operacao_a_calcular],  chordpq[indice_chuva], (operacao_a_calcular+1), diretorio_saida, int(self.plotar_graficos.get()))
                            #   Contar 1 operacao
                            npq += 1
                            
                        #   Para Puls
                        elif cdoh[operacao_a_calcular] == 2:
                            #   Pegar o hidrograma de entrada
                            hidusadop = preparacaoPULS(nint, hidentp, operacao_a_calcular, ordpq, ordp, ordm, ordj, hidsaipq, hidsaip, hidsaim, hidsaij)
                            #   Calcule a operacao de Puls
                            hidsaip[np] = calcularOperacaoPULS(hidusadop, cotinp[operacao_a_calcular], estp[operacao_a_calcular], ccv[operacao_a_calcular], dt, nint, nomesop[operacao_a_calcular], (operacao_a_calcular+1), diretorio_saida, int(self.plotar_graficos.get()))
                            #   Contar 1 operacao
                            np += 1
                            
                        #   Para MKC
                        elif cdoh[operacao_a_calcular] == 3:
                            #   Pegar o hidrograma de entrada
                            hidusadom = preparacaoMKC(nint, hidentm, operacao_a_calcular, ordpq, ordp, ordm, ordj, hidsaipq, hidsaip, hidsaim, hidsaij)
                            #   Calcule a operacao de MKC
                            hidsaim[nm] = calcularOperacaoMKC(hidusadom, dt, nint, difcot[operacao_a_calcular], compcan[operacao_a_calcular], largcan[operacao_a_calcular], nmann[operacao_a_calcular], nomesop[operacao_a_calcular], (operacao_a_calcular+1), diretorio_saida, int(self.plotar_graficos.get()))
                            #   Contar 1 operacao
                            nm += 1
                            
                        #   Para JUNCAO
                        elif cdoh[operacao_a_calcular] == 4:
                            #   Pegar os hidrogramas de entrada utilizados
                            hidusadosj = preparacaoJUNCAO(nint, hidentj[operacao_a_calcular], ordpq, ordp, ordm, ordj, hidsaipq, hidsaip, hidsaim, hidsaij)
                            #   Calcular a operacao de JUNCAO
                            hidsaij[nj] = calcularOperacaoJUNCAO(hidusadosj, nint)
                            #   Contar 1 operacao
                            nj += 1
                            
                        #   Para CENARIOS
                        elif cdoh[operacao_a_calcular] == 5:
                            #   Contar 1 operacao
                            nc += 1
                        
                        #   Barra de progresso
                        self.progressBar(operacao, nop)
                        
                        
                    #   Loop para escrever os arquivos de saida
                    #   Para PQ
                    if cdoh[operacao_a_calcular] == 1:
                        #   Gerar arquivo de saida...
                        escreverSaidaPQ(nint, dt, nintch, nop, cdoh, cn, area, tc, chpq, chordpq, hidsaipq, chefpq, diretorio_saida, nome_arquivo, nomesop)
                        
                    #   Para PULS
                    elif cdoh[operacao_a_calcular] == 2:
                        #   Gerar arquivo de saida...
                        escreverSaidaPULS(nint, dt, nop, cdoh, hidentp, hidsaipq, hidsaip, ordpq, ordp, ordm, ordj, diretorio_saida, nome_arquivo, nomesop)
                    
                    #   Para MKC
                    elif cdoh[operacao_a_calcular] == 3:
                        #   Gerar arquivo de saida...
                        escreverSaidaMKC(nint, dt, nop, cdoh, hidentm, hidsaipq, hidsaip, hidsaim, ordpq, ordp, ordm, ordj, diretorio_saida, nome_arquivo, nomesop)
        
                    #   Para JUNCOES
                    elif cdoh[operacao_a_calcular] == 4:
                        #   Gerar arquivo de saida...
                        escreverSaidaJUNCAO(nint, dt, nop, cdoh, hidentj, hidsaipq, hidsaip, hidsaim, hidsaij, ordp, ordm, ordj, diretorio_saida, nome_arquivo, nomesop)
                    
                    ##   Para CENARIOS
                    #elif cdoh[operacao_a_calcular] == 5:
                    #    #   Gerar arquivo de saida...
                    #    escreverSaidaCEN(nint, dt, nintch, nop, cdoh, chpq, chordpq, hidsaipq)
                    
                    #   Avisar usuario
                    print "\tArquivo %s executado com sucesso!\n\t----------------------------------------------------\n" %(nome_arquivo)
                    
        #   Atualizar a interface
        self.update()
        #   Mostrar interface
        self.deiconify()
    #---------------------------------------------------------------------

#-----------------------------------------------------------
if __name__ == '__main__':
    #   (ano, mes, dia / 19000) - 9 = versao com 3 digitos
    versao_do_software = float( round( ((200123.)/20000) - 9, 2 ) )
    #   Pegar o diretorio do software
    diretorio_do_software = path.dirname(path.abspath(sys.argv[0]))
    
    print """
     ------------------ MODELO HIDROLOGICO ECOTECNOLOGIAS ----------------- 
    |Autores:                                                              |
    |- Vitor Gustavo Geller - vitorgg_hz@hotmail.com                       |
    |- Lucas Camargo da Silva Tassinari - lucascst@hotmail.com             |
    |- Daniel Gustavo Allasia P. - dallasia@gmail.com                      |
    |                                                                      |
    |VERSAO: %5.2f                                                         |
    |                                                                      |
    |------------------------- INSTRUCOES DE USO --------------------------|
    |                                                                      |
    |-> Caso voce nao possua um arquivo de entrada, voce pode cria-lo uti- |
    |lizando o ambiente auxiliar localizado na opcao "Escrever arquivo de  |
    |entrada..." dentro do menu "Arquivo".                                 |
    |                                                                      |
    |-> Se voce ja' possui um arquivo de entrada, voce pode executa-lo cli-|
    |cando na opcao "Executar arquivo de entrada..." dentro do menu        |
    |"Arquivo".                                                            |
     ---------------------------------------------------------------------- 
    """ %(versao_do_software)
    
    #   Rodar o software
    root = Tk()
    
    app = Application(root, versao_do_software, diretorio_do_software)
    
    #app.iconbitmap(diretorio_do_software + "/water.ico")
    app.mainloop()