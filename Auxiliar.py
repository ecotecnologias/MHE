# -*- coding: latin_1 -*-

import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
    
from os import path, remove, makedirs
#from Modelo_Hidrologico_Ecotecnologias import Application
from PIL import Image, ImageTk
from tkMessageBox import showinfo, showerror#, askquestion
import ScrolledText as tkst
import tkFileDialog
import errno
import Modelo_Hidrologico_Ecotecnologias


class InterfaceAuxiliar(Toplevel):
    """"""
    info_gerais_fornecidas = False
    strings_entrada = []
    strings_estruturas_puls = []
    nch = 1
    nop = 1
    dir_arq_cotavolume = ''
    dir_arq_hidpuls = ''
    dir_arq_hidmkc = ''
    #----------------------------------------------------------------------
    def __init__(self, master, versao_do_software, diretorio_do_software):
        master.withdraw()
        self.master = master
        #self.master.withdraw()
        self.versao_do_software = versao_do_software
        self.diretorio_do_software = diretorio_do_software
    
        #   Cria a janela
        Toplevel.__init__(self, bg="#DFF9CA")
        
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Criar Arquivo de Entrada" )
        self.protocol("WM_DELETE_WINDOW", self.esvaziarStringsEntrada)
        #   Introduzir o frame
        primeiroFrame = Frame(self, bg="#DFF9CA")
        primeiroFrame.pack(padx = 10, pady = 10)
        
        #   Criar barra horizontal
        xscrollbar = Scrollbar(primeiroFrame, orient="horizontal")
        
        #   Text Box
        self.cxTexto = tkst.ScrolledText(primeiroFrame, height = 0, width = 0, wrap=NONE, xscrollcommand=xscrollbar.set) #, height = 15, width = 42
        #   Posicionar
        self.cxTexto.grid(row = 1, column = 2, columnspan = 2, rowspan = 7, sticky = 'e', padx = 15, pady = 0, ipadx=227, ipady=120)
        
        #   Configurar barra horizontal
        xscrollbar.grid(row = 8, column = 2, columnspan = 2, rowspan = 1, sticky = 'n', padx = 15, pady = 0, ipadx=213) #ipadx = 188
        xscrollbar.config(command=self.cxTexto.xview)
        
        #   Quero editar
        self.cxTexto.configure(state="disabled", font=(10))
        
        #   Chamo a funcao para modificar a textbox
        self.strings_entrada = self.modificarTextbox(self.cxTexto, self.strings_entrada)
        
        self.cxTexto.focus()
        
        #   Serao 2 interfaces
        if self.info_gerais_fornecidas == False:
            Label(primeiroFrame, text = "Visualização", bg="#DFF9CA").grid(row = 0, column = 2, columnspan = 2, sticky = 'n', padx = 15, pady = 5)
            Button(primeiroFrame, text = "Informaçoes Gerais", width = 26, command=lambda: self.inserirInformacoesGerais()).grid(row = 1, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            Button(primeiroFrame, text = "Inserir Chuvas", width = 26, fg="#A9A9A9").grid(row = 2, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 2)
            Button(primeiroFrame, text = "Op. Chuva-Vazão", width = 26, fg="#A9A9A9").grid(row = 3, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            Button(primeiroFrame, text = "Op. PULS", width = 26, fg="#A9A9A9").grid(row = 4, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 2)
            Button(primeiroFrame, text = "Op. Muskingun-Cunge", width = 26, fg="#A9A9A9").grid(row = 5, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            Button(primeiroFrame, text = "Op. Junção", width = 26, fg="#A9A9A9").grid(row = 6, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 2)
            Button(primeiroFrame, text = "Op. Cenários chuva-vazão", width = 26, fg="#A9A9A9").grid(row = 7, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            #   Botao para salvar o conteudo criado pelo usuario
            Button(primeiroFrame, text = "Salvar", width = 10, fg="#A9A9A9").grid(row = 9, column = 3, columnspan = 1, sticky = 'e', padx = 15, pady = 2)
            
        elif self.info_gerais_fornecidas == True:
            Label(primeiroFrame, text = "Visualização", bg="#DFF9CA").grid(row = 0, column = 2, columnspan = 2, sticky = 'n', padx = 15, pady = 5)
            Button(primeiroFrame, text = "Informaçoes Gerais", width = 26, fg="#A9A9A9").grid(row = 1, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            Button(primeiroFrame, text = "Inserir Chuvas", width = 26, command=lambda: self.inserirChuvas()).grid(row = 2, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 2)
            Button(primeiroFrame, text = "Op. Chuva-Vazão", width = 26, command=lambda: self.inserirPQ()).grid(row = 3, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            Button(primeiroFrame, text = "Op. PULS", width = 26, command=lambda: self.inserirPULS()).grid(row = 4, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 2)
            Button(primeiroFrame, text = "Op. Muskingun-Cunge", width = 26, command=lambda: self.inserirMKC()).grid(row = 5, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            Button(primeiroFrame, text = "Op. Junção", width = 26, fg="#A9A9A9").grid(row = 6, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 2)
            Button(primeiroFrame, text = "Op. Cenários chuva-vazão", width = 26, fg="#A9A9A9").grid(row = 7, column = 0, columnspan = 2, sticky = 'n', padx = 15, pady = 0)
            #   Botao para salvar o conteudo criado pelo usuario
            Button(primeiroFrame, text = "Salvar", width = 10, fg="#000000", command=lambda: self.salvarArquivo()).grid(row = 9, column = 3, columnspan = 1, sticky = 'e', padx = 15, pady = 2)
        
        #   Botao para fechar/desfazer alteracoes
        if self.info_gerais_fornecidas == False:
            Button(primeiroFrame, text = "Fechar", width = 10, command=lambda: self.esvaziarStringsEntrada()).grid(row = 9, column = 2, columnspan = 1, sticky = 'w', padx = 15, pady = 5)
        elif self.info_gerais_fornecidas == True:
            Button(primeiroFrame, text = "Desfazer", width = 10, command=lambda: self.desfazerAlteracoes()).grid(row = 9, column = 2, columnspan = 1, sticky = 'w', padx = 15, pady = 5)
        
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
    def validar_float(self, novo_texto):
        """"""
        if not novo_texto: # o campo esta limpo
            return True
        try:
            if len(novo_texto) < 9:
                float(novo_texto)
                return True
                if "-" in novo_texto:
                    raise ValueError
                else:
                    return True
            else:
                raise ValueError
        except ValueError: #forcar erro
            return False #falso para nao digitar  
    #----------------------------------------------------------------------
    def validar_int(self, novo_texto):
        """"""
        if not novo_texto: # o campo esta sendo limpo
            return True
        #poder digitar somente 6 digitos
        try:
            if len(novo_texto) < 7: 
                int(novo_texto)
                if "-" in novo_texto:
                    raise ValueError
                return True
            else:
                raise ValueError
        except ValueError: #forcar erro
            return False #falso para nao digitar
    #----------------------------------------------------------------------
    def validar_int_pospico(self, novo_texto):
        """"""
        if not novo_texto: # o campo esta sendo limpo
            return True
        #poder digitar somente 3 digitos
        try:
            if len(novo_texto) < 4:
                int(novo_texto)
                if "-" in novo_texto:
                    raise ValueError
                elif int(novo_texto) > 100:
                    raise ValueError
                else:
                    return True
            else:
                raise ValueError
        except ValueError: #forcar erro
            return False #falso para nao digitar
    #----------------------------------------------------------------------
    def desfazerAlteracoes(self):
        """"""
        if len(self.strings_entrada) > 0:
            #   Ver o que foi deletado
            ultima_string = self.strings_entrada[-1]
            
            #   Se for a primeira linha...
            if ultima_string.split(";")[0] == "INICIO":
                #   Volte a estaca zero
                self.info_gerais_fornecidas = False
                self.nch = 1
                self.nop = 1
            #   Se for CHuva
            if ultima_string.split(";")[0] == "CHUVA":
                #   Reduza um nch
                self.nch -= 1
            #   Se for Operacao
            if ultima_string.split(";")[0] == "OPERACAO":
                #   Reduza um nch
                self.nop -= 1            
            
            #   Delete a ultima coisa 
            del self.strings_entrada[-1]
            
            #   Modifique o texto da textbox
            self.strings_entrada = self.modificarTextbox(self.cxTexto, self.strings_entrada)
            
            #   Fechar a janela
            self.destroy()
            
            #   Reinicie a janela principal da visualizacao do arquivo de saida
            self.__init__(self.master, self.versao_do_software, self.diretorio_do_software)
    #----------------------------------------------------------------------
    def procurarArquivo(self, caso):
        """"""
        #   Abra-!
        self.withdraw()
        
        #   Informacao de curva cota-volume
        if caso == 1:
            #   Modificar o botao
            self.buttonCotaVolume.configure(fg="#000000", text = "Procurar arquivo")
            #   Resetar diretorio
            self.dir_arq_cotavolume = ''
        
        #   Informacao de hidrograma de entrada do Puls
        elif caso == 2:
            #   Modificar o botao
            self.buttonHidOpPULS.configure(fg="#000000", text = "Procurar arquivo")
            #   Resetar diretorio
            self.dir_arq_hidpuls = ''
            
        #   Informacao de hidrograma de entrada do MKC
        elif caso == 3:
            #   Modificar o botao
            self.buttonHidOpMKC.configure(fg="#000000", text = "Procurar arquivo")
            #   Resetar diretorio
            self.dir_arq_hidmkc = ''
        
        #   Procure o arquivo...
        root2   = Tk()
        entrada = tkFileDialog.askopenfile(mode='r') 
        root2.destroy()
        
        #   Verificar se algo foi selecionado
        if (not entrada == None):
            #   Verificar se o arquivo existe
            if (path.isfile(entrada.name) == True):
                #   Armazenar extensao do arquivo
                extensao_arquivo = entrada.name.split("/")[-1]
                extensao_arquivo = extensao_arquivo.split(".")[-1]
                #   Verificar se a extensao dele e' txt
                if ((extensao_arquivo == "txt") or (extensao_arquivo == "TXT")):
                    #   Testar qual variavel deve ser modificada
                    
                    #   Informacao de chuva observada
                    if caso == 0:
                        #   Pegue o diretorio dele
                        #   Armazenar
                        self.dir_arq_chuva = str(entrada.name)
                        #   But here's my NUMBER ONEE! (HEY!!!)
                        self.strings_entrada.append("CHUVA; " + str(self.nch) + "; " + self.chuva_local + "OBS; " + str(self.dir_arq_chuva) + ";\n")
                        #   Resetar
                        self.dir_arq_chuva = ''
                        #   Resetar
                        self.chuva_local = '\n'
                        #   Somar uma chuva
                        self.nch += 1
                        #   Fechar arquivo
                        entrada.close()
                        #   Kadabra!
                        self.deiconify()
                        #   Sumir com a janela antiga
                        self.fecharJanelaSecundaria() 
                    
                    #   Informacao de curva cota-volume
                    elif caso == 1:
                        #   Pegue o diretorio dele
                        #   Armazenar
                        self.dir_arq_cotavolume = str(entrada.name)
                        #   Fechar arquivo
                        entrada.close()
                        #   Kadabra!
                        self.deiconify()
                        #   Modificar o botao
                        self.buttonCotaVolume.configure(fg="#00B400", text = "Arq. encontrado")
                    
                    #   Informacao de hidrograma de entrada do Puls
                    elif caso == 2:
                        #   Pegue o diretorio dele
                        #   Armazenar
                        self.dir_arq_hidpuls = str(entrada.name)
                        #   Fechar arquivo
                        entrada.close()
                        #   Kadabra!
                        self.deiconify()
                        #   Modificar o botao
                        self.buttonHidOpPULS.configure(fg="#00B400", text = "Arq. encontrado")
                    
                    
                    #   Informacao de hidrograma de entrada do MKC
                    elif caso == 3:
                        #   Pegue o diretorio dele
                        #   Armazenar
                        self.dir_arq_hidmkc = str(entrada.name)
                        #   Fechar arquivo
                        entrada.close()
                        #   Kadabra!
                        self.deiconify()
                        #   Modificar o botao
                        self.buttonHidOpMKC.configure(fg="#00B400", text = "Arq. encontrado")
                    
                    #   Deu erro, só feche o arquivo
                    else:
                        #   Fechar arquivo
                        entrada.close()
                        #   Kadabra!
                        self.deiconify()
                        #   Sumir com a janela antiga
                        self.fecharJanelaSecundaria() 
                
                #   Nao e' arquivo txt
                else:
                    showerror("Verifique os dados de entrada!", "Selecione um arquivo de texto (formato: *.txt).") 
                    #   SE o aruqivo estiver aberto somehow, feche-o
                    if entrada.closed == False:
                        entrada.close()
                    #   Kadabra!
                    self.deiconify()
            #   O arquivo nao existe
            else:
                showerror("Verifique os dados de entrada!", "O modelo não conseguiu localizar o arquivo selecionado.") 
                #   SE o aruqivo estiver aberto somehow, feche-o
                if entrada.closed == False:
                    entrada.close()
                #   Kadabra!
                self.deiconify()
        #   Selecione algum aquivo de entrada
        else:
            showinfo("Verifique os dados de entrada!", "Arquivo de entrada não selecionado.\n\nTente novamente.") 
            #   Kadabra!
            self.deiconify()
    #----------------------------------------------------------------------
    def modificarTextbox(self, textBOX, string_conteudo):
        #   Desbloquear
        textBOX.configure(state="normal", font=(10))
        
        #   Delete o que tem
        textBOX.delete(1.0, END)
        
        #   Escrever a string na textbox
        for i in xrange(len(string_conteudo)):
            #   Escreva linha em linha
            textBOX.insert(END, string_conteudo[i])
        
        #   Bloquear novamente
        textBOX.configure(state="disabled", font=(10))
        
        #   Retorne a string atualizada
        return string_conteudo
    #----------------------------------------------------------------------
    def esvaziarStringsEntrada(self):
        #   Loop para esvaziar a string
        for i in xrange(len(self.strings_entrada)):
            #   Delete
            del self.strings_entrada[0]

        #   Chamo a funcao para modificar a textbox
        self.strings_entrada = self.modificarTextbox(self.cxTexto, self.strings_entrada)
        
        #   Fechar a janela
        self.destroy()
        
        #   Reinicio a janela principal
        Modelo_Hidrologico_Ecotecnologias.Application(self.master, self.versao_do_software, self.diretorio_do_software)
    #----------------------------------------------------------------------
    def fecharJanelaSecundaria(self):
        #   Destrua o conteudo da janela
        for widget in self.winfo_children():
            widget.destroy()
        #   Reinicie a janela principal da visualizacao do arquivo de saida
        self.__init__(self.master, self.versao_do_software, self.diretorio_do_software)
    #----------------------------------------------------------------------
    def manipularInformacaoGeral(self):
        #   checar erros basicos:
        auxERROS = ''
        ERROS = '' #string que armazena os erros dos dados de entrada.
        focus = 0
        
        #   Testar numero operacoes hidrologicas
        if self.entryOphidro.get() == '':
            auxERROS = ERROS
            ERROS = "Informe o número de operações hidrológicas.\n\n"
            ERROS += auxERROS
            focus = 4
        #   Testar numero intervalos de tempo com chuva
        if self.entryNint_tempo_chuva.get() == '':
            auxERROS = ERROS
            ERROS = "Informe o número de intervalos de tempo com chuva.\n\n"
            ERROS += auxERROS
            focus = 3
        #   Testar numero de chuvas
        if self.entryNchuvas.get() == '':
            auxERROS = ERROS
            ERROS = "Informe o número postos de chuva.\n\n"
            ERROS += auxERROS
            focus = 2
        #   Testar o intervalo de tempo
        if self.entryDt.get() == '':
            auxERROS = ERROS
            ERROS = "Informe a duração do intervalo de tempo (segundos).\n\n"
            ERROS += auxERROS
            focus = 1
        #   Testar numero de intervalos de tempo
        if self.entryNint_tempo.get() == '':
            auxERROS = ERROS
            ERROS = "Informe o número de intervalos de tempo.\n\n"
            ERROS += auxERROS
            focus = 0
            
        #   checar se foram encontrados erros:
        if not (ERROS == ''):
            #   remover os enters excessivos no final da string
            ERROS = ERROS[0:-2]
            #   Avise o usuario do problema
            showerror("Verifique os dados de entrada!", str(ERROS)) 
            #   Focus na entry correta
            if focus == 0:
                self.entryNint_tempo.focus()
            elif focus == 1:
                self.entryDt.focus()
            elif focus == 2:
                self.entryNchuvas.focus()
            elif focus == 3:
                self.entryNint_tempo_chuva.focus()
            else: 
                self.entryOphidro.focus()
                
        #   Sem erros aparentes...Continue o PROGRAMA 
        else: 
            #   But here's my NUMBER ONEE! (HEY!!!)
            self.strings_entrada.append("INICIO; "+ self.entryNint_tempo.get() + "; " + self.entryDt.get() + "; " + self.entryNchuvas.get() + "; " + self.entryNint_tempo_chuva.get() + "; " + self.entryOphidro.get() + ";\n")
            
            #   Entrar com informacoes iniciais somente uma vez
            self.info_gerais_fornecidas = True
            
            #   Sumir com a janela antiga
            self.fecharJanelaSecundaria()
    #----------------------------------------------------------------------
    def inserirInformacoesGerais(self):
        """"""
        #   Sumir com a janela antiga
        self.destroy()
        
        #   Criar janela nova
        Toplevel.__init__(self, bg="#DFF9CA")
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Informações Gerais" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaSecundaria)
        #   Criar o frame
        segundoFrame = Frame(self, bg="#DFF9CA")
        segundoFrame.pack(padx = 10, pady = 10)

        #   TITULO:
        Label(segundoFrame, font=(10), text= "INFORMAÇÕES GERAIS DA SIMULAÇÃO", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 4, sticky = 'n', padx = 15, pady = 5 )

        #   Numero de intervalos de tempo
        Label(segundoFrame,text= "Numero de intervalos de tempo:", bg="#DFF9CA").grid(row = 1, column = 0, columnspan = 2, sticky = 'e', padx = 0, pady = 3)
        #   Caixa de dialogo para entrar com nint_tempo
        nint_tempo = self.register(self.validar_int)
        self.entryNint_tempo = Entry(segundoFrame, validate="key", width=15, validatecommand=(nint_tempo, '%P'))
        self.entryNint_tempo.grid(row = 1, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3)
        
        #   Duracao do intervalo de tempo
        Label(segundoFrame, text= "Duração do intervalo de tempo (segundos):", bg="#DFF9CA").grid(row = 2, column = 0, columnspan = 2, sticky = 'e', padx = 0, pady = 0 )
        #   Caixa de dialogo para entrar com dt
        dt = self.register(self.validar_int)
        self.entryDt = Entry(segundoFrame, validate="key", width=15, validatecommand=(dt, '%P'))
        self.entryDt.grid(row = 2, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0)
        
        #   Numero de chuvas
        Label(segundoFrame, text= "Numero de postos de chuva:", bg="#DFF9CA").grid(row = 3, column = 0, columnspan = 2, sticky = 'e', padx = 0, pady = 3 )
        #   Caixa de dialogo para entrar com numero de chuvas
        nchuvas = self.register(self.validar_int)
        self.entryNchuvas = Entry(segundoFrame, validate="key", width=15, validatecommand=(nchuvas, '%P'))
        self.entryNchuvas.grid(row = 3, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3)
        
        #   Numero de intervalos de tempo com chuva
        Label(segundoFrame, text= "Numero de intervalos de tempo com chuva:", bg="#DFF9CA").grid(row = 4, column = 0, columnspan = 2, sticky = 'e', padx = 0, pady = 0 )
        #   Caixa de dialogo para entrar com nint_tempo_chuva
        nint_tempo_chuva = self.register(self.validar_int)
        self.entryNint_tempo_chuva = Entry(segundoFrame, validate="key", width=15, validatecommand=(nint_tempo_chuva, '%P'))
        self.entryNint_tempo_chuva.grid(row = 4, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0)
        
        #   Numero de operacoes hidrologicas
        Label(segundoFrame, text= "Numero de operações hidrológicas:", bg="#DFF9CA").grid(row = 5, column = 0, columnspan = 2, sticky = 'e', padx = 0, pady = 3 )
        #   Caixa de dialogo para entrar com numero de operacoes hidrologicas
        ophidro = self.register(self.validar_int)
        self.entryOphidro = Entry(segundoFrame, validate="key", width=15, validatecommand=(ophidro, '%P'))
        self.entryOphidro.grid(row = 5, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3)

        #   botao proximo
        Button(segundoFrame, text = 'Próximo', width = 14, command=lambda: self.manipularInformacaoGeral()).grid(row = 6, column = 2, columnspan = 2, sticky = 'e', padx = 5, pady = 5 )
        #   botao voltar
        Button(segundoFrame, text = 'Voltar', width = 14, command=lambda: self.fecharJanelaSecundaria()).grid(row = 6, column = 0, columnspan = 2, sticky = 'w', padx = 5, pady = 5 )
        
        self.entryNint_tempo.focus()
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #----------------------------------------------------------------------
    def manipularInserirChuva(self, tipo_chuva):
        """"""
        #   Preguica de fazer uma funcao nova so' para isso....
        if not len(self.entryChuvaLocal.get()) == 0:
            self.chuva_local = (self.entryChuvaLocal.get() + ";\n")
        else:
            self.chuva_local = "\n"
            
        #   Se for chuva observada...
        if tipo_chuva == 0:
            #   Procurar arquivo
            self.procurarArquivo(0)
        #   Se for chuva de IDF
        elif tipo_chuva == 1:
            #   Chamar funcao da janela IDF
            self.inserirIDF()
    #----------------------------------------------------------------------
    def inserirChuvas(self):
        """"""
        #   Sumir com a janela antiga
        self.destroy()
        
        #   Criar janela nova
        Toplevel.__init__(self, bg="#DFF9CA")
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Informação Pluvial" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaSecundaria)
        #   Criar o frame
        segundoFrame = Frame(self, bg="#DFF9CA")
        segundoFrame.pack(padx = 10, pady = 10)

        #   TITULO:
        Label(segundoFrame, font=(10), text= "INSERIR CHUVA À SIMULAÇÃO", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 4, sticky = 'n', padx = 15, pady = 5 )
        
        #   Nome/local da chuva
        Label(segundoFrame,text= "Local de origem:", bg="#DFF9CA").grid(row = 1, column = 0, columnspan = 1, sticky = 'e', padx = 0, pady = 3 )
        #   Caixa do comentario
        self.entryChuvaLocal = Entry(segundoFrame, width = 18)
        self.entryChuvaLocal.grid(row = 1, column = 2, columnspan = 3, sticky = 'w', padx = 5, pady = 3)
        
        #   botao IDF
        Button(segundoFrame, text = 'Gerar chuva a partir de uma IDF', width = 34, command=lambda: self.manipularInserirChuva(1)).grid(row = 2, column = 0, columnspan = 4, sticky = 'n', padx = 5, pady = 3 )
        #   botao OBS
        Button(segundoFrame, text = 'Inserir chuva de um arquivo (txt)', width = 34, command=lambda: self.manipularInserirChuva(0)).grid(row = 3, column = 0, columnspan = 4, sticky = 'n', padx = 5, pady = 3 )
        #   botao sair
        Button(segundoFrame, text = 'Voltar', width = 34, command=lambda: self.fecharJanelaSecundaria()).grid(row = 4, column = 0, columnspan = 4, sticky = 'n', padx = 5, pady = 3 )
        
        #   Focus
        self.entryChuvaLocal.focus()
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #----------------------------------------------------------------------
    def manipularInserirIDF(self):
        """"""
        #   checar erros basicos:
        auxERROS = ''
        ERROS = '' #string que armazena os erros dos dados de entrada.
        focus = 0
        
        #   Testar D
        if self.entryParametroD.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o parâmetro D da equação IDF.\n\n")
            ERROS += auxERROS
            focus = 6
        #   Testar C
        if self.entryParametroC.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o parâmetro C da equação IDF.\n\n")
            ERROS += auxERROS
            focus = 5
        #   Testar B
        if self.entryParametroB.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o parâmetro B da equação IDF.\n\n")
            ERROS += auxERROS
            focus = 4
        #   Testar A
        if self.entryParametroA.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o parâmetro A da equação IDF.\n\n")
            ERROS += auxERROS
            focus = 3
        #   Testar TR
        if self.entryTemporetorno.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o tempo de recorrência da chuva (anos).\n\n")
            ERROS += auxERROS
            focus = 2
        #   Testar PP
        if self.entryPospico.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o valor de pospico (entre 0 e 100).\n\n")
            ERROS += auxERROS
            focus = 1
            
        if self.entryLimite.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o valor limite de intensidade para os primeiros intervalos de tempo de chuva (minutos).\n\nDica: Utilize zero para desabilitar esta opção.\n\n")
            ERROS += auxERROS
            focus = 0
            
        #   checar se foram encontrados erros:
        if not (ERROS == ''):
            #   remover os enters excessivos no final da string
            ERROS = ERROS[0:-2]
            #   Avise o usuario do problema
            showerror("Verifique os dados de entrada!", str(ERROS)) 
            #   Focus na entry correta
            if focus == 0:
                self.entryLimite.focus()
            elif focus == 1:
                self.entryPospico.focus()
            elif focus == 2:
                self.entryTemporetorno.focus()
            elif focus == 3:
                self.entryParametroA.focus()
            elif focus == 4:
                self.entryParametroB.focus()
            elif focus == 5:
                self.entryParametroC.focus()
            else: 
                self.entryParametroD.focus()

        #   Sem erros aparentes...Continue o PROGRAMA 
        else: 
            #   But here's my NUMBER ONEE! (HEY!!!)
            self.strings_entrada.append("CHUVA; " + str(self.nch) + "; " + self.chuva_local + "IDF; " +  str(self.valorTipoIDF.get()) + "; " + str(int(self.entryPospico.get())/100.) + "; " + self.entryTemporetorno.get() + "; " + self.entryParametroA.get() + "; " + self.entryParametroB.get() + "; " + self.entryParametroC.get() + "; " + self.entryParametroD.get() + "; " + self.entryLimite.get() + ";\n")
            
            #   Somar uma chuva
            self.nch += 1
            
            #   Sumir com a janela antiga
            self.fecharJanelaSecundaria()        
    #----------------------------------------------------------------------    
    def cancelarChuvaIDF(self):
        """"""
        self.chuva_local = '\n'
        self.fecharJanelaSecundaria()
    #----------------------------------------------------------------------
    def inserirIDF(self):
        """"""
        #   Sumir com a janela antiga
        self.destroy()
        
        #   Criar janela nova
        Toplevel.__init__(self, bg="#DFF9CA")
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Chuva de IDF" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaSecundaria)
        #   Criar o frame
        segundoFrame = Frame(self, bg="#DFF9CA")
        segundoFrame.pack(padx = 10, pady = 10)

        #   TITULO:
        Label(segundoFrame, font=(10), text= "INFORMAÇÕES DA IDF", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 4, sticky = 'n', padx = 15, pady = 5 )
    
        #   Tipo da IDF : So' ha' uma ate' a versao atual
        Label(segundoFrame,text= "Tipo da IDF:", bg="#DFF9CA").grid(row = 1, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0 )
        #   Cria a variavel que controla os botoes
        self.valorTipoIDF = IntVar()
        self.valorTipoIDF.set(1)
        #   Cria os botoes pra clicar
        Checkbutton(segundoFrame, text = "Tipo 1", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.valorTipoIDF, onvalue = 1, offvalue = 1).grid(row = 1, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3 )
        
        #   Pospico
        Label(segundoFrame,text= "Posição do pico (%):", bg="#DFF9CA").grid(row = 2, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3 )
        #   Caixa de dialogo para entrar com nint_tempo
        pospico = self.register(self.validar_int_pospico)
        self.entryPospico = Entry(segundoFrame, validate="key", width=10, validatecommand=(pospico, '%P'))
        self.entryPospico.grid(row = 2, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3, ipadx=6)
        
        #   TR
        Label(segundoFrame,text= "Tempo de retorno da chuva:", bg="#DFF9CA").grid(row = 3, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0 )
        #   Caixa de dialogo para entrar TR
        temporetorno = self.register(self.validar_int)
        self.entryTemporetorno = Entry(segundoFrame, validate="key", width=10, validatecommand=(temporetorno, '%P'))
        self.entryTemporetorno.grid(row = 3, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=6)
        
        #   Parametro A
        Label(segundoFrame,text= "Parâmetro a da IDF:", bg="#DFF9CA").grid(row = 4, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3 )
        #   Caixa de dialogo para parametro a
        parametroA = self.register(self.validar_float)
        self.entryParametroA = Entry(segundoFrame, validate="key", width=10, validatecommand=(parametroA, '%P'))
        self.entryParametroA.grid(row = 4, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3, ipadx=6)
        
        #   Parametro B
        Label(segundoFrame,text= "Parâmetro b da IDF:", bg="#DFF9CA").grid(row = 5, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0)
        #   Caixa de dialogo para parametro b
        parametroB = self.register(self.validar_float)
        self.entryParametroB = Entry(segundoFrame, validate="key", width=10, validatecommand=(parametroB, '%P'))
        self.entryParametroB.grid(row = 5, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=6)
        
        #   Parametro C
        Label(segundoFrame,text= "Parâmetro c da IDF:", bg="#DFF9CA").grid(row = 6, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3 )
        #   Caixa de dialogo para parametro c
        parametroC = self.register(self.validar_float)
        self.entryParametroC = Entry(segundoFrame, validate="key", width=10, validatecommand=(parametroC, '%P'))
        self.entryParametroC.grid(row = 6, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3, ipadx=6)
        
        #   Parametro D
        Label(segundoFrame,text= "Parâmetro d da IDF:", bg="#DFF9CA").grid(row = 7, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0)
        #   Caixa de dialogo para parametro d
        parametroD = self.register(self.validar_float)
        self.entryParametroD = Entry(segundoFrame, validate="key", width=10, validatecommand=(parametroD, '%P'))
        self.entryParametroD.grid(row = 7, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=6)
        
        #   Limite de intensidades self.entryLimite.get()
        Label(segundoFrame,text= "Limite de intensidade (minutos):", bg="#DFF9CA").grid(row = 8, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0)
        #   Caixa de dialogo para parametro d
        limiteIDF = self.register(self.validar_int)
        self.entryLimite = Entry(segundoFrame, validate="key", width=10, validatecommand=(limiteIDF, '%P'))
        self.entryLimite.grid(row = 8, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=6)
        
        #   botao proximo
        Button(segundoFrame, text = 'Próximo', command=lambda: self.manipularInserirIDF()).grid(row = 9, column = 2, columnspan = 2, sticky = 'e', padx = 5, pady = 3, ipadx=14)
        #   botao sair
        Button(segundoFrame, text = 'Sair', command=lambda: self.cancelarChuvaIDF()).grid(row = 9, column = 0, columnspan = 2, sticky = 'w', padx = 5, pady = 3, ipadx=18)
        
        #   Foco
        self.entryPospico.focus()
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #----------------------------------------------------------------------
    def habilitaEntryTC(self):
        """"""
        #   Habilite
        self.entryTC.configure(state="normal")
        #   Delete o que esta' escrito
        self.entryTCDifCota.delete(0, END)
        self.entryTCCompCanal.delete(0, END)
        #   Desabilite
        self.entryTCDifCota.configure(state="disabled")
        self.entryTCCompCanal.configure(state="disabled")
#----------------------------------------------------------------------
    def habilitaEntryKirpich(self):
        """"""
        #   Delete o que esta' escrito
        self.entryTC.delete(0, END)
        #   Desabilite
        self.entryTC.configure(state="disabled")
        #   Habilite
        self.entryTCDifCota.configure(state="normal")
        self.entryTCCompCanal.configure(state="normal")
    #----------------------------------------------------------------------
    def manipularInserirPQ(self):
        """"""
        #   checar erros basicos:
        auxERROS = ''
        ERROS = '' #string que armazena os erros dos dados de entrada.
        focus = 0
        
        #   Preguica de fazer uma funcao nova so' para isso....
        if not len(self.entryNomeOperacao.get()) == 0:
            local_operacao = (self.entryNomeOperacao.get() + ";\n")
        else:
            local_operacao = "\n"
        
        #   Testar TC: Se for horas
        if int((self.valorTempoConcentracao.get()) == 1):
            #   Trata-se de valor informado em horas!
            if self.entryTC.get() == '':
                auxERROS = ERROS
                ERROS = ("Informe o tempo de concentração (horas).\n\n")
                ERROS += auxERROS
                focus = 3
        #   Testar TC: Se for Kirpich
        elif int((self.valorTempoConcentracao.get()) == 2):
            #   Trata-se de TC calculado por Kirpich
            #   Testar o comprimento do canal
            if self.entryTCCompCanal.get() == '':
                auxERROS = ERROS
                ERROS = ("Informe o comprimento do principal curso d'água da bacia (km).\n\n")
                ERROS += auxERROS
                focus = 5
            #   Testar Diferenca de cota
            if self.entryTCDifCota.get() == '':
                auxERROS = ERROS
                ERROS = ("Informe a diferença de cota ao longo do curso d'água (m).\n\n")
                ERROS += auxERROS
                focus = 4
        
        #   Testar AREA
        if self.entryArea.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe a área de bacia (km²).\n\n")
            ERROS += auxERROS
            focus = 2
        #   Testar CN
        if self.entryCN.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o coeficiente adimensional CN utilizado no método.\n\n")
            ERROS += auxERROS
            focus = 1
        #   Testar Numero de CHuva
        if self.entryChuvaPQ.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o número da chuva que será utilizada no método.\n\n")
            ERROS += auxERROS
            focus = 0

        #   checar se foram encontrados erros:
        if not (ERROS == ''):
            #   remover os enters excessivos no final da string
            ERROS = ERROS[0:-2]
            #   Avise o usuario do problema
            showerror("Verifique os dados de entrada!", str(ERROS)) 
            #   Focus na entry correta
            if focus == 0:
                self.entryChuvaPQ.focus()
            elif focus == 1:
                self.entryCN.focus()
            elif focus == 2:
                self.entryArea.focus()
            elif focus == 3:
                self.entryTC.focus()
            elif focus == 4:
                self.entryTCDifCota.focus()
            else: 
                self.entryTCCompCanal.focus()

        #   Sem erros aparentes...Continue o PROGRAMA 
        else: 

            #   Testar TC: Se for horas
            if int((self.valorTempoConcentracao.get()) == 1):
                #   Com TC em horas:
                self.strings_entrada.append("OPERACAO; " + str(self.nop) + "; " + local_operacao + "PQ; " + self.entryChuvaPQ.get() + ";\nCN; " + self.entryCN.get() + ";\nHUT; " + self.entryArea.get() + "; " + self.entryTC.get() + ";\n")
                #   Acrescer numero de operacoes
                self.nop += 1
            #   Se TC de Kirpich
            elif int((self.valorTempoConcentracao.get()) == 2):
                #   Com TC calculado por kirpich
                self.strings_entrada.append("OPERACAO; " + str(self.nop) + "; " + local_operacao + "PQ; " + self.entryChuvaPQ.get() + ";\nCN; " + self.entryCN.get() + ";\nHUT; " + self.entryArea.get() + "; KIRPICH; " + self.entryTCDifCota.get() + "; " + self.entryTCCompCanal.get() + ";\n")
                #   Acrescer numero de operacoes
                self.nop += 1
            
            #   Sumir com a janela antiga
            self.fecharJanelaSecundaria()    
    #----------------------------------------------------------------------
    def inserirPQ(self):
        """"""
        #   Sumir com a janela antiga
        self.destroy()
        
        #   Criar janela nova
        Toplevel.__init__(self, bg="#DFF9CA")
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Operação Chuva-Vazão" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaSecundaria)
        #   Criar o frame
        segundoFrame = Frame(self, bg="#DFF9CA")
        segundoFrame.pack(padx = 10, pady = 10)

        #   TITULO:
        Label(segundoFrame, font=(10), text= "INFORMAÇÕES CHUVA-VAZÃO", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 4, sticky = 'n', padx = 15, pady = 10)
    
        #   Label local
        Label(segundoFrame, text= "Nome/local da operação:", bg="#DFF9CA").grid(row = 1, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0)
        #   Caixa de dialogo para entrar local
        self.entryNomeOperacao = Entry(segundoFrame, width = 10)
        self.entryNomeOperacao.grid(row = 1, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=10)
    
        #   Chuva numero
        Label(segundoFrame,text= "Número da chuva utilizada:", bg="#DFF9CA").grid(row = 2, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3  )
        #   Caixa de dialogo para entrar com qual chuva esta operacao deve usar
        chuvadapq = self.register(self.validar_int)
        self.entryChuvaPQ = Entry(segundoFrame, validate="key", width=10, validatecommand=(chuvadapq, '%P'))
        self.entryChuvaPQ.grid(row = 2, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3, ipadx=10)

        #   CN
        Label(segundoFrame,text= "Valor estimado do coeficiente CN:", bg="#DFF9CA").grid(row = 3, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 0)
        #   Caixa de dialogo para entrar com CN
        coefCN = self.register(self.validar_float)
        self.entryCN = Entry(segundoFrame, validate="key", width=10, validatecommand=(coefCN, '%P'))
        self.entryCN.grid(row = 3, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=10)
        
        #   Area
        Label(segundoFrame,text= "Área estimada da bacia (km²):", bg="#DFF9CA").grid(row = 4, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3  )
        #   Caixa de dialogo para entrar com area
        areaBacia = self.register(self.validar_float)
        self.entryArea = Entry(segundoFrame, validate="key", width=10, validatecommand=(areaBacia, '%P'))
        self.entryArea.grid(row = 4, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 3, ipadx=10)
        
        #-------------------
        #   TC
        self.tcGroup = LabelFrame(segundoFrame, text="Tempo de Concentração", bg="#DFF9CA")
        self.tcGroup.grid(row = 5, column = 0, columnspan = 4, sticky = 'e', padx = 5, pady = 3)
        #   cria a variavel que controla os botoes
        self.valorTempoConcentracao = IntVar()
        self.valorTempoConcentracao.set(1)
        #   Primeira linha da groupbox
        Checkbutton(self.tcGroup, text = "Informar valor (horas):", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.valorTempoConcentracao, onvalue = 1, offvalue = 1, command=lambda: self.habilitaEntryTC())                   .grid(row = 0, column = 0, columnspan = 2, sticky = 'w', padx = 5, pady = 3)
        Checkbutton(self.tcGroup, text = "Calcular utilizando a eq. de Kirpich:", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.valorTempoConcentracao, onvalue = 2, offvalue = 2, command=lambda: self.habilitaEntryKirpich()).grid(row = 1, column = 0, columnspan = 4, sticky = 'w', padx = 5, pady = 0)
        #   Variaveis das entries
        TC          = self.register(self.validar_float)
        TTCDifCota  = self.register(self.validar_float)
        TCCompCanal = self.register(self.validar_float)
        #   Criar entries
        self.entryTC          = Entry(self.tcGroup, validate="key", width=10, validatecommand=(TC, '%P'))
        self.entryTCDifCota   = Entry(self.tcGroup, validate="key", width=10, validatecommand=(TTCDifCota, '%P'))
        self.entryTCCompCanal = Entry(self.tcGroup, validate="key", width=10, validatecommand=(TCCompCanal, '%P'))
        #   Posicionar Entries
        self.entryTC         .grid(row = 0, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0)
        self.entryTCDifCota  .grid(row = 2, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 0)
        self.entryTCCompCanal.grid(row = 3, column = 2, columnspan = 2, sticky = 'w', padx = 5, pady = 6)
        #   Labels
        Label(self.tcGroup,text= "Diferença de cota (m):", bg="#DFF9CA").grid(row = 2, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3  )
        Label(self.tcGroup,text= "Comprimento do canal (km):", bg="#DFF9CA").grid(row = 3, column = 0, columnspan = 2, sticky = 'e', padx = 5, pady = 3  )

        #   Desabilite-as
        self.entryTCDifCota.configure(state="disabled")
        self.entryTCCompCanal.configure(state="disabled")
        
        #   botao proximo
        Button(segundoFrame, text = 'Próximo', command=lambda: self.manipularInserirPQ()).grid(row = 8, column = 2, columnspan = 2, sticky = 'e', padx = 10, pady = 3, ipadx=14)
        #   botao sair
        Button(segundoFrame, text = ' Sair ', command=lambda: self.fecharJanelaSecundaria()).grid(row = 8, column = 0, columnspan = 2, sticky = 'w', padx = 10, pady = 3, ipadx=16)
        
        #   Foco
        self.entryNomeOperacao.focus()
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #----------------------------------------------------------------------
    def manipularInserirPULS(self):
        """"""
        #   checar erros basicos:
        auxERROS = ''
        ERROS = '' #string que armazena os erros dos dados de entrada.
        focus = 0
        
        #   Preguica de fazer uma funcao nova so' para isso....
        if not len(self.entryNomeOperacao.get()) == 0:
            local_operacao = (self.entryNomeOperacao.get() + ";\n")
        else:
            local_operacao = "\n"
        
        #   Testar estruturas de extravasao
        if len(self.strings_estruturas_puls) == 0:
            auxERROS = ERROS
            ERROS = ("É necessário pelo menos uma estrutura de extravasão.\n\n")
            ERROS += auxERROS
        
        #   Testar Hidrograma de Entrada
        if int((self.hidEntPuls.get()) == 1):
            #   Testar a entry
            if self.entryHidOpPULS.get() == '':
                auxERROS = ERROS
                ERROS = ("Informe o número da operação hidrológica utilizada para o hidrograma de entrada.\n\n")
                ERROS += auxERROS
                focus = 2
        #   Hidrograma de arquivo de texto
        elif int((self.hidEntPuls.get()) == 2):
            #   Se o diretorio dele ta vazio
            if self.dir_arq_hidpuls == '':
                auxERROS = ERROS
                ERROS = ("Selecione o arquivo do hidrograma de entrada.\n\n")
                ERROS += auxERROS

        #   Se o diretorio dele ta vazio
        if self.dir_arq_cotavolume == '':
            auxERROS = ERROS
            ERROS = ("Selecione o arquivo do da curva cota-volume.\n\n")
            ERROS += auxERROS
    
        #   Testar cota inicial do reservatório
        if self.entryCotaReservatorio.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe a cota inicial do reservatório (metros).\n\n")
            ERROS += auxERROS
            focus = 1
        
        #   checar se foram encontrados erros:
        if not (ERROS == ''):
            #   remover os enters excessivos no final da string
            ERROS = ERROS[0:-2]
            #   Avise o usuario do problema
            showerror("Verifique os dados de entrada!", str(ERROS)) 
            #   Focus na entry correta
            if focus == 1:
                self.entryCotaReservatorio.focus()
            elif focus == 2:
                self.entryHidOpPULS.focus()

        #   Sem erros aparentes...Continue o PROGRAMA 
        else: 
            #   Sera' usada a seguir
            estruturas = ''
            #   "recortar" as estruturas
            for i in xrange(len(self.strings_estruturas_puls)):
                #   Adicione
                estruturas += self.strings_estruturas_puls[i]
            
            #   Testar Hidrograma de Entrada
            if int((self.hidEntPuls.get()) == 1):
                #   Com hidrograma de outra operacao:
                self.strings_entrada.append("OPERACAO; " + str(self.nop) + "; " + local_operacao + "PULS; " + self.entryHidOpPULS.get() + "; " + self.entryCotaReservatorio.get() + "; " + str(len(self.strings_estruturas_puls)) + ";\n" + estruturas + self.dir_arq_cotavolume + ";\n")
                #   Acrescer numero de operacoes
                self.nop += 1
            #   Hidrograma de arquivo de texto
            elif int((self.hidEntPuls.get()) == 2):
                #   Com TC calculado por kirpich
                self.strings_entrada.append("OPERACAO; " + str(self.nop) + "; " + local_operacao + "PULS; " + self.dir_arq_hidpuls + "; " + self.entryCotaReservatorio.get() + "; " + str(len(self.strings_estruturas_puls)) + ";\n" + estruturas + self.dir_arq_cotavolume + ";\n")
                #   Acrescer numero de operacoes
                self.nop += 1

            #   Resetar
            self.strings_estruturas_puls = []
            self.dir_arq_cotavolume = ''
            self.dir_arq_hidpuls = ''
            
            #   Sumir com a janela antiga
            self.fecharJanelaSecundaria()
    #----------------------------------------------------------------------
    def habilitaEntryHidOpPULS(self):
        """"""
        #   Habilite
        self.entryHidOpPULS.configure(state="normal")
        
        #   Desabilite o botao
        self.buttonHidOpPULS.configure(fg="#A9A9A9", text = "Procurar arquivo", command=lambda: self.disableButton())

        #   Resetar diretorio
        self.dir_arq_hidpuls = ''
    #-----------------------------------------------------------------------
    def habilitaButtonHidOpPULS(self):
        """"""
        #   Habilite o botao
        self.buttonHidOpPULS.configure(fg="#000000", command=lambda: self.procurarArquivo(2))
        
        #   Delete o que esta' escrito
        self.entryHidOpPULS.delete(0, END)

        #   Desabilite
        self.entryHidOpPULS.configure(state="disabled")
    #-----------------------------------------------------------------------
    def disableButton(self):
        """"""
        #   Essa funcao e' assim mesmo, ela nao faz nada... e' para desabilitar um botao.
    #-----------------------------------------------------------------------
    def removerUltimaEstPULS(self):
        """"""
        if not len(self.strings_estruturas_puls) == 0:
            del self.strings_estruturas_puls[-1]
        
        #   Chamo a funcao para modificar a textbox
        self.strings_estruturas_puls = self.modificarTextbox(self.cxTextoPULS, self.strings_estruturas_puls)
    #-----------------------------------------------------------------------
    def adicionarVertedor(self):
        """"""
        #   Testar as entries
        if not (self.entryCoeficienteVertedor.get() == ''):
            if not (self.entryComprimentoSoleira.get() == ''):
                if not (self.entryCotaSoleira.get() == ''):
                    if not (self.entryCotaMaxVertedor.get() == ''):
                        #   adicionar
                        self.strings_estruturas_puls.append("VERTEDOR; " + self.entryCoeficienteVertedor.get() + "; " + self.entryComprimentoSoleira.get() + "; " + self.entryCotaSoleira.get() + "; " + self.entryCotaMaxVertedor.get() + ";\n")
                        
                        #   Chamo a funcao para modificar a textbox
                        self.strings_estruturas_puls = self.modificarTextbox(self.cxTextoPULS, self.strings_estruturas_puls)
                        
                        #   Foco
                        self.entryCoeficienteVertedor.focus()
    #-----------------------------------------------------------------------
    def adicionarOrificio(self):
        """"""
        #   Testar as entries
        if not (self.entryCoeficienteOrificio.get() == ''):
            if not (self.entryAreaOrificio.get() == ''):
                if not (self.entryAlturaOrificio.get() == ''):
                    if not (self.entryCotaOrificio.get() == ''):
                        #   adicionar
                        self.strings_estruturas_puls.append("ORIFICIO; " + self.entryCoeficienteOrificio.get() + "; " + self.entryAreaOrificio.get() + "; " + self.entryAlturaOrificio.get() + "; " + self.entryCotaOrificio.get() + ";\n")
                        
                        #   Chamo a funcao para modificar a textbox
                        self.strings_estruturas_puls = self.modificarTextbox(self.cxTextoPULS, self.strings_estruturas_puls)
                        
                        #   Foco
                        self.entryCoeficienteOrificio.focus()
    #----------------------------------------------------------------------
    def inserirPULS(self):
        """"""
        #   Sumir com a janela antiga
        self.destroy()
        
        #   Criar janela nova
        Toplevel.__init__(self, bg="#DFF9CA")
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Operação PULS" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaSecundaria)
        #   Criar o frame
        segundoFrame = Frame(self, bg="#DFF9CA")
        segundoFrame.pack(padx = 10, pady = 10)

        #   TITULO:
        Label(segundoFrame, font=(10), text= "INFORMAÇÕES PULS", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 4, sticky = 'n', padx = 15, pady = 5 )
    
        #   Label local
        Label(segundoFrame, text= "Nome/local da operação:", bg="#DFF9CA").grid(row = 1, column = 1, columnspan = 1, sticky = 'e', padx = 0, pady = 3 )
        #   Caixa de dialogo para entrar local
        self.entryNomeOperacao = Entry(segundoFrame, width = 20)
        self.entryNomeOperacao.grid(row = 1, column = 2, columnspan = 2, sticky = 'n', padx = 10, pady = 3)
        
        #   Cota inicial
        Label(segundoFrame, text= "Cota inicial do reservatório (m):", bg="#DFF9CA").grid(row = 2, column = 1, columnspan = 1, sticky = 'e', padx = 0, pady = 0)
        #   Caixa de dialogo para entrar com cota
        CotaReservatorio = self.register(self.validar_float)
        self.entryCotaReservatorio = Entry(segundoFrame, validate="key", width=20, validatecommand=(CotaReservatorio, '%P'))
        self.entryCotaReservatorio.grid (row = 2, column = 2, columnspan = 2, sticky = 'n', padx = 10, pady = 0)
        
        #   Curva cota volume
        Label(segundoFrame, text= "Selecione o arquivo da cota-volume:", bg="#DFF9CA").grid(row = 3, column = 1, columnspan = 1, sticky = 'e', padx = 0, pady = 3 )
        #   Caixa de dialogo para entrar com cota
        self.buttonCotaVolume = Button(segundoFrame, text = 'Procurar arquivo', command=lambda: self.procurarArquivo(1))
        self.buttonCotaVolume.grid(row = 3, column = 2, columnspan = 2, sticky = 'w', padx = 10, pady = 3, ipadx=22)

        #-------------------
        #   Primeira groupbox
        self.hidGroup = LabelFrame(segundoFrame, text="Hidrograma de entrada", bg="#DFF9CA")
        self.hidGroup.grid(row = 4, column = 0, columnspan = 4, sticky = 'e', padx = 5, pady = 3, ipadx = 0, ipady=5)
        #   cria a variavel que controla os botoes
        self.hidEntPuls = IntVar()
        self.hidEntPuls.set(1)
        
        #   Entrar com numero para o hidrograma de entrada
        Checkbutton(self.hidGroup, text = "Oriundo de uma operação hidrológica", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.hidEntPuls, onvalue = 1, offvalue = 1, command=lambda: self.habilitaEntryHidOpPULS()).grid(row = 0, column = 2, columnspan = 1, sticky = 'w', padx = 5, pady = 0, ipadx=22)
        #   Entrar com arquivo de texto para o hidrograma
        Checkbutton(self.hidGroup, text = "Oriundo de um arquivo de texto", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.hidEntPuls, onvalue = 2, offvalue = 2, command=lambda: self.habilitaButtonHidOpPULS()).grid(row = 2, column = 2, columnspan = 1, sticky = 'w', padx = 5, pady = 6, ipadx=22)
        
        #   Caixa de dialogo para entrar com o numero do hidrograma
        Label(self.hidGroup,text= "Número da operação:", bg="#DFF9CA").grid(row = 1, column = 2, columnspan = 1, sticky = 'e', padx = 0, pady = 0)
        hidNumero = self.register(self.validar_int)
        self.entryHidOpPULS = Entry(self.hidGroup, validate="key", width= 20, validatecommand=(hidNumero, '%P'))
        self.entryHidOpPULS.grid(row = 1, column = 3, columnspan = 1, sticky = 'e', padx = 15, pady = 0)

        #   botao procurar arquivo
        self.buttonHidOpPULS = Button(self.hidGroup, text = 'Procurar arquivo', fg="#A9A9A9")
        self.buttonHidOpPULS.grid(row = 2, column = 3, columnspan = 1, sticky = 'e', padx = 15, pady = 6, ipadx=22)
        
        #-------------------
        #   Segunda groupbox
        self.estrGroup = LabelFrame(segundoFrame, text="Estruturas de extravasão", bg="#DFF9CA")
        self.estrGroup.grid(row = 5, column = 0, columnspan = 4, sticky = 'n', padx = 5, pady = 3, ipady=5)

        Label(self.estrGroup,text= "Vertedor", bg="#DFF9CA").grid(row = 1, column = 0, columnspan = 2, sticky = 'n', padx = 5, pady = 0)
        Label(self.estrGroup,text= "Orifício", bg="#DFF9CA").grid(row = 1, column = 2, columnspan = 2, sticky = 'n', padx = 5, pady = 0)
        
        #   Para o vertedor
        Label(self.estrGroup,text= "Coef. de descarga:", bg="#DFF9CA").grid(row = 2, column = 0, columnspan = 1, sticky = 'e', padx = 5, pady = 3  )
        Label(self.estrGroup,text= "Largura da soleira (m):", bg="#DFF9CA").grid(row = 3, column = 0, columnspan = 1, sticky = 'e', padx = 5, pady = 0)
        Label(self.estrGroup,text= "Cota da soleira (m):", bg="#DFF9CA").grid(row = 4, column = 0, columnspan = 1, sticky = 'e', padx = 5, pady = 3  )
        Label(self.estrGroup,text= "Cota máxima (m):", bg="#DFF9CA").grid(row = 5, column = 0, columnspan = 1, sticky = 'e', padx = 5, pady = 0)
        CoeficienteVertedor = self.register(self.validar_float)
        ComprimentoSoleira  = self.register(self.validar_float)
        CotaSoleira         = self.register(self.validar_float)
        AlturaVertedor      = self.register(self.validar_float)
        self.entryCoeficienteVertedor = Entry(self.estrGroup, validate="key", width=6, validatecommand=(CoeficienteVertedor, '%P'))
        self.entryComprimentoSoleira  = Entry(self.estrGroup, validate="key", width=6, validatecommand=(ComprimentoSoleira, '%P'))
        self.entryCotaSoleira         = Entry(self.estrGroup, validate="key", width=6, validatecommand=(CotaSoleira, '%P'))
        self.entryCotaMaxVertedor     = Entry(self.estrGroup, validate="key", width=6, validatecommand=(AlturaVertedor, '%P'))
        self.entryCoeficienteVertedor.grid(row = 2, column = 1, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        self.entryComprimentoSoleira .grid(row = 3, column = 1, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        self.entryCotaSoleira        .grid(row = 4, column = 1, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        self.entryCotaMaxVertedor    .grid(row = 5, column = 1, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        #   botao adicionar
        Button(self.estrGroup, text = 'Adicionar Vertedor', command=lambda: self.adicionarVertedor()).grid(row = 6, column = 0, columnspan = 2, sticky = 'n', padx = 5, pady = 3, ipadx = 51)
        
        #   Para o vertedor
        Label(self.estrGroup,text= "Coef. de descarga:", bg="#DFF9CA").grid(row = 2, column = 2, columnspan = 1, sticky = 'e', padx = 5, pady = 3  )
        Label(self.estrGroup,text= "Área (m²):", bg="#DFF9CA").grid(row = 3, column = 2, columnspan = 1, sticky = 'e', padx = 5, pady = 0)
        Label(self.estrGroup,text= "Altura/diâmetro (m):", bg="#DFF9CA").grid(row = 4, column = 2, columnspan = 1, sticky = 'e', padx = 5, pady = 3  )
        Label(self.estrGroup,text= "Cota do centro (m):", bg="#DFF9CA").grid(row = 5, column = 2, columnspan = 1, sticky = 'e', padx = 5, pady = 0)
        CoeficienteOrificio = self.register(self.validar_float)
        AreaOrificio        = self.register(self.validar_float)
        AlturaOrificio      = self.register(self.validar_float)
        CotaOrificio        = self.register(self.validar_float)
        self.entryCoeficienteOrificio = Entry(self.estrGroup, validate="key", width=6, validatecommand=(CoeficienteOrificio, '%P'))
        self.entryAreaOrificio        = Entry(self.estrGroup, validate="key", width=6, validatecommand=(AreaOrificio, '%P'))
        self.entryAlturaOrificio      = Entry(self.estrGroup, validate="key", width=6, validatecommand=(AlturaOrificio, '%P'))
        self.entryCotaOrificio        = Entry(self.estrGroup, validate="key", width=6, validatecommand=(CotaOrificio, '%P'))
        self.entryCoeficienteOrificio.grid(row = 2, column = 3, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        self.entryAreaOrificio       .grid(row = 3, column = 3, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        self.entryAlturaOrificio     .grid(row = 4, column = 3, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        self.entryCotaOrificio       .grid(row = 5, column = 3, columnspan = 1, sticky = 'n', padx = 5, pady = 3 )
        #   botao adicionar orificio
        Button(self.estrGroup, text = 'Adicionar Orifício', command=lambda: self.adicionarOrificio()).grid(row = 6, column = 2, columnspan = 2, sticky = 'n', padx = 5, pady = 3, ipadx= 50)
        
        #   botao remover ultima estrutura adiciona
        Button(self.estrGroup, text = 'Remover última estrutura adicionada', command=lambda: self.removerUltimaEstPULS()).grid(row = 7, column = 0, columnspan = 4, sticky = 'n', padx = 16, pady = 0, ipadx=122)
        
        #   Text Box
        self.cxTextoPULS = tkst.ScrolledText(self.estrGroup, height = 0, width = 0)
        #   Posicionar
        self.cxTextoPULS.grid(row = 8, column = 0, columnspan = 4, rowspan = 1, sticky = 'n', padx = 5, pady = 6, ipadx = 233, ipady = 30)
        #   Quero editar
        self.cxTextoPULS.configure(state="disabled", font=(10))
        
        #   Chamo a funcao para modificar a textbox
        self.strings_estruturas_puls = self.modificarTextbox(self.cxTextoPULS, self.strings_estruturas_puls)
        
        #   botao proximo
        Button(segundoFrame, text = 'Próximo', width = 10, command=lambda: self.manipularInserirPULS()).grid(row = 6, column = 2, columnspan = 2, sticky = 'e', padx = 5, pady = 3 )
        #   botao sair
        Button(segundoFrame, text = 'Sair', width = 10, command=lambda: self.fecharJanelaSecundaria()).grid(row = 6, column = 0, columnspan = 2, sticky = 'w', padx = 5, pady = 3 )
        
        #   Foco
        self.entryNomeOperacao.focus()
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #-----------------------------------------------------------------------
    def manipularInserirMKC(self):
        """"""
        #   checar erros basicos:
        auxERROS = ''
        ERROS = '' #string que armazena os erros dos dados de entrada.
        focus = 0
        
        #   Preguica de fazer uma funcao nova so' para isso....
        if not len(self.entryNomeOperacao.get()) == 0:
            local_operacao = (self.entryNomeOperacao.get() + ";\n")
        else:
            local_operacao = "\n"
        
        #   Testar 
        if self.entryCoeficienteRugosidade.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o coeficiente de rugosidade médio.\n\n")
            ERROS += auxERROS
            focus = 5
        
        #   Testar 
        if self.entryLarguraCanalM.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe a largura média do canal (metros).\n\n")
            ERROS += auxERROS
            focus = 4
            
        #   Testar 
        if self.entryComprimentoCanalKM.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe o comprimento do canal (quilômetros).\n\n")
            ERROS += auxERROS
            focus = 3
            
        #   Testar 
        if self.entryDiferencaCotaM.get() == '':
            auxERROS = ERROS
            ERROS = ("Informe a diferença de cota do canal (metros).\n\n")
            ERROS += auxERROS
            focus = 2
        
        #   Testar Hidrograma de Entrada
        if int((self.hidEntMKC.get()) == 1):
            #   Testar a entry
            if self.entryHidOpMKC.get() == '':
                auxERROS = ERROS
                ERROS = ("Informe o número da operação hidrológica utilizada para o hidrograma de entrada.\n\n")
                ERROS += auxERROS
                focus = 1
        #   Hidrograma de arquivo de texto
        elif int((self.hidEntMKC.get()) == 2):
            #   Se o diretorio dele ta vazio
            if self.dir_arq_hidmkc == '':
                auxERROS = ERROS
                ERROS = ("Selecione o arquivo do hidrograma de entrada.\n\n")
                ERROS += auxERROS

        #   checar se foram encontrados erros:
        if not (ERROS == ''):
            #   remover os enters excessivos no final da string
            ERROS = ERROS[0:-2]
            #   Avise o usuario do problema
            showerror("Verifique os dados de entrada!", str(ERROS)) 
            #   Focus na entry correta
            if focus == 1:
                self.entryHidOpMKC.focus()
            elif focus == 2:
                self.entryDiferencaCotaM.focus()
            elif focus == 3:
                self.entryComprimentoCanalKM.focus()
            elif focus == 4:
                self.entryLarguraCanalM.focus()
            elif focus == 5:
                self.self.entryCoeficienteRugosidade.focus()

        #   Sem erros aparentes...Continue o PROGRAMA 
        else: 
            #   Testar Hidrograma de Entrada
            if int((self.hidEntMKC.get()) == 1):
                #   Com hidrograma de outra operacao:
                self.strings_entrada.append("OPERACAO; " + str(self.nop) + "; " + local_operacao + "MKC; " + self.entryHidOpMKC.get() + "; " + self.entryDiferencaCotaM.get() + "; " + self.entryComprimentoCanalKM.get() + "; " + self.entryLarguraCanalM.get() + "; " + self.entryCoeficienteRugosidade.get() + ";\n")
                #   Acrescer numero de operacoes
                self.nop += 1
            #   Hidrograma de arquivo de texto
            elif int((self.hidEntMKC.get()) == 2):
                #   Com TC calculado por kirpich
                self.strings_entrada.append("OPERACAO; " + str(self.nop) + "; " + local_operacao + "MKC; " + self.dir_arq_hidmkc + "; " + self.entryDiferencaCotaM.get() + "; " + self.entryComprimentoCanalKM.get() + "; " + self.entryLarguraCanalM.get() + "; " + self.entryCoeficienteRugosidade.get() + ";\n")
                #   Acrescer numero de operacoes
                self.nop += 1

            #   Resetar
            self.dir_arq_hidmkc = ''
            
            #   Sumir com a janela antiga
            self.fecharJanelaSecundaria()
    #-----------------------------------------------------------------------
    def habilitaEntryHidOpMKC(self):
        """"""
        #   Habilite
        self.entryHidOpMKC.configure(state="normal")
        
        #   Desabilite o botao
        self.buttonHidOpMKC.configure(fg="#A9A9A9", text = "Procurar arquivo", command=lambda: self.disableButton())
        
        #   Resetar diretorio
        self.dir_arq_hidmkc = ''
    #-----------------------------------------------------------------------
    def habilitaButtonHidOpMKC(self):
        """"""
        #   Habilite o botao
        self.buttonHidOpMKC.configure(fg="#000000", command=lambda: self.procurarArquivo(3))
        
        #   Delete o que esta' escrito
        self.entryHidOpMKC.delete(0, END)

        #   Desabilite
        self.entryHidOpMKC.configure(state="disabled")
    #-----------------------------------------------------------------------
    def inserirMKC(self):
        """"""
        #   Sumir com a janela antiga
        self.destroy()
        
        #   Criar janela nova
        Toplevel.__init__(self, bg="#DFF9CA")
        #self.iconbitmap(diretorio_do_software + "/water.ico")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Operação MKC" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaSecundaria)
        #   Criar o frame
        segundoFrame = Frame(self, bg="#DFF9CA")
        segundoFrame.pack(padx = 10, pady = 10)

        #   TITULO:
        Label(segundoFrame, font=(10), text= "INFORMAÇÕES MUSKINGUN-CUNGE", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 4, sticky = 'n', padx = 15, pady = 5 )
    
        #   Label local
        Label(segundoFrame, text= "Nome/local da operação:", bg="#DFF9CA").grid(row = 1, column = 2, columnspan = 1, sticky = 'e', padx = 0, pady = 3, ipadx=0)
        #, column = 1, columnspan = 1, sticky = 'e', padx = 0, pady = 3)
        #   Caixa de dialogo para entrar local
        self.entryNomeOperacao = Entry(segundoFrame, width = 1)
        self.entryNomeOperacao.grid(row = 1, column = 3, columnspan = 1, sticky = 'e', padx = 10, pady = 3, ipadx=80)
        #, column = 2, columnspan = 2, sticky = 'e', padx = 10, pady = 3, ipadx=100)

        #-------------------
        #   Primeira groupbox
        self.hidGroup = LabelFrame(segundoFrame, text="Hidrograma de entrada", bg="#DFF9CA")
        self.hidGroup.grid(row = 2, column = 0, columnspan = 4, sticky = 'e', padx = 10, pady = 3, ipadx = 0, ipady=5)
        #   cria a variavel que controla os botoes
        self.hidEntMKC = IntVar()
        self.hidEntMKC.set(1)
        
        #   Entrar com numero para o hidrograma de entrada
        Checkbutton(self.hidGroup, text = "Oriundo de uma operação hidrológica", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.hidEntMKC, onvalue = 1, offvalue = 1, command=lambda: self.habilitaEntryHidOpMKC()).grid(row = 0, column = 0, columnspan = 2, sticky = 'w', padx = 5, pady = 0, ipadx=0)
        #   Entrar com arquivo de texto para o hidrograma
        Checkbutton(self.hidGroup, text = "Oriundo de um arquivo de texto", bg="#DFF9CA", activebackground="#DFF9CA", variable = self.hidEntMKC, onvalue = 2, offvalue = 2, command=lambda: self.habilitaButtonHidOpMKC()).grid(row = 2, column = 0, columnspan = 2, sticky = 'w', padx = 5, pady = 6, ipadx=0)
        
        #   Caixa de dialogo para entrar com o numero do hidrograma
        Label(self.hidGroup,text= "Número da operação:", bg="#DFF9CA").grid(row = 1, column = 0, columnspan = 2, sticky = 'e', padx = 0, pady = 0, ipadx=0)
        hidNumero = self.register(self.validar_int)
        self.entryHidOpMKC = Entry(self.hidGroup, validate="key", width= 1, validatecommand=(hidNumero, '%P'))
        self.entryHidOpMKC.grid(row = 1, column = 2, columnspan = 2, sticky = 'e', padx = 15, pady = 0, ipadx=76)

        #   botao procurar arquivo
        self.buttonHidOpMKC = Button(self.hidGroup, text = 'Procurar arquivo', fg="#A9A9A9")
        self.buttonHidOpMKC.grid(row = 2, column = 2, columnspan = 2, sticky = 'e', padx = 15, pady = 6, ipadx=22)
        #-----------------
        #   Labels
        Label(segundoFrame,text= "Diferença de cota (m):", bg="#DFF9CA")        .grid(row = 3, column = 2, columnspan = 1, sticky = 'e', padx = 0, pady = 3, ipadx=0)
        Label(segundoFrame,text= "Comprimento do canal (km):", bg="#DFF9CA")    .grid(row = 4, column = 2, columnspan = 1, sticky = 'e', padx = 0, pady = 0, ipadx=0)
        Label(segundoFrame,text= "Largura do canal (m):", bg="#DFF9CA")         .grid(row = 5, column = 2, columnspan = 1, sticky = 'e', padx = 0, pady = 3, ipadx=0)
        Label(segundoFrame,text= "Coeficiente de rugosidade (-):", bg="#DFF9CA").grid(row = 6, column = 2, columnspan = 1, sticky = 'e', padx = 0, pady = 0, ipadx=0)
        #   Entries
        DiferencaCotaM        = self.register(self.validar_float)
        ComprimentoCanalKM    = self.register(self.validar_float)
        LarguraCanalM         = self.register(self.validar_float)
        CoeficienteRugosidade = self.register(self.validar_float)
        self.entryDiferencaCotaM        = Entry(segundoFrame, validate="key", width=1, validatecommand=(DiferencaCotaM, '%P'))
        self.entryComprimentoCanalKM    = Entry(segundoFrame, validate="key", width=1, validatecommand=(ComprimentoCanalKM, '%P'))
        self.entryLarguraCanalM         = Entry(segundoFrame, validate="key", width=1, validatecommand=(LarguraCanalM, '%P'))
        self.entryCoeficienteRugosidade = Entry(segundoFrame, validate="key", width=1, validatecommand=(CoeficienteRugosidade, '%P'))
        self.entryDiferencaCotaM       .grid(row = 3, column = 3, columnspan = 1, sticky = 'e', padx = 10, pady = 3, ipadx=80)
        self.entryComprimentoCanalKM   .grid(row = 4, column = 3, columnspan = 1, sticky = 'e', padx = 10, pady = 3, ipadx=80)
        self.entryLarguraCanalM        .grid(row = 5, column = 3, columnspan = 1, sticky = 'e', padx = 10, pady = 3, ipadx=80)
        self.entryCoeficienteRugosidade.grid(row = 6, column = 3, columnspan = 1, sticky = 'e', padx = 10, pady = 3, ipadx=80)
        
        #   botao proximo
        Button(segundoFrame, text = 'Próximo', command=lambda: self.manipularInserirMKC()).grid(row = 7, column = 3, columnspan = 1, sticky = 'e', padx = 10, pady = 3, ipadx=53 )
        #   botao sair
        Button(segundoFrame, text = 'Sair', command=lambda: self.fecharJanelaSecundaria()).grid(row = 7, column = 0, columnspan = 2, sticky = 'w', padx = 10, pady = 3, ipadx=30)
        
        #   Foco
        self.entryNomeOperacao.focus()
        
        #   Centralizar o programa na tela
        self.centralizar(self)
    #-----------------------------------------------------------------------
    def make_sure_path_exists(self, path):
        """"""
        try:
            #   Faca a pasta
            makedirs(path)
        #   Errou!
        except OSError as exception:
            #   Mostrar apenas se o erro for diferente de "ja existe"
            if exception.errno != errno.EEXIST:
                #   Mostre
                raise
    #-----------------------------------------------------------------------
    def salvarArquivo(self):
        """"""
        #   Criar a pasta para salvar arquivo de entrada
        self.make_sure_path_exists(self.diretorio_do_software + "/Entrada")
        
        #   Verificar se o arquivo existe
        if (path.isfile(self.diretorio_do_software + "/Entrada/Arquivo_entrada.hyd") == True):
            #   Tente deletar o arquivo
            try:
                #   Delete o arquivo antigo
                remove(self.diretorio_do_software + "/Entrada/Arquivo_entrada.hyd")
                #   flag
                arq_deletado = True

            #   Ocorreu um erro...
            except:
                #   flag
                arq_deletado = False
                #   Avise o usuario que o arquivo antigo NAO foi deletado
                showerror("Arquivo de entrada.", "Ocorreu um erro ao tentar deletar o arquivo de entrada antigo.\n\nTente copiar o conteúdo da caixa de texto e criar um arquivo de texto manualmente.")
        
            #   Escrever aquivo novo
            if arq_deletado == True:
                #    preparo arquivo de saida
                SaidaMHEAuxiliar, fileExtension = path.splitext(self.diretorio_do_software + "/Entrada/Arquivo_entrada")
                SaidaMHEAuxiliar               += ".hyd"
                SaidaMHEAuxiliar                = open( SaidaMHEAuxiliar, 'w', buffering = 0 )
                
                #   Escrever strings
                for i in xrange(len(self.strings_entrada)):
                    SaidaMHEAuxiliar.write(self.strings_entrada[i])
                #   Feche
                SaidaMHEAuxiliar.close()
                showinfo("Arquivo de entrada.", "Arquivo de entrada gerado com sucesso.\nVerifique o diretório do modelo.\n\nLembrete: É possível criar arquivos de entrada manualmente.")

        #   Tem o que escrever e nao tem arquivo
        else:
            #    preparo arquivo de saida
            SaidaMHEAuxiliar, fileExtension = path.splitext(self.diretorio_do_software + "/Entrada/Arquivo_entrada")
            SaidaMHEAuxiliar               += ".hyd"
            SaidaMHEAuxiliar                = open( SaidaMHEAuxiliar, 'w', buffering = 0 )
            
            #   Escrever strings
            for i in xrange(len(self.strings_entrada)):
                SaidaMHEAuxiliar.write(self.strings_entrada[i])
            #   Feche
            SaidaMHEAuxiliar.close()
            showinfo("Arquivo de entrada.", "Arquivo de entrada gerado com sucesso.\nVerifique o diretório do modelo.\n\nLembrete: É possível criar arquivos de entrada manualmente.")
    #-----------------------------------------------------------------------