# -*- coding: latin_1 -*-

import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
    
import ScrolledText as tkst
import Modelo_Hidrologico_Ecotecnologias


class InterfaceInformacoes(Toplevel):
    """"""
    info_gerais = ""
    aux = "->     Este é um software acadêmico gratuito e de código aberto.\n\n"; info_gerais += aux
    aux = "->     Este modelo pode ser usado livremente em trabalhos acadêmicos e profissionais desde que devidamente citado.\n\n"; info_gerais += aux
    aux = "->     Recomenda-se criticidade na análise dos resultados pois os desenvolvedores deste programa não se responsabilizam por quaisquer consequências oriundas de erros de qualquer natureza.\n\n"; info_gerais += aux
    aux = "->     Manuais estão em processo de confecção e serão disponibilizados assim que finalizados.\n\n"; info_gerais += aux
    aux = "->     Não hesite em reportar bugs aos desenvolvedores.\n\n"; info_gerais += aux
    aux = "Desenvolvedores:\n"; info_gerais += aux
    aux = "     Vitor Gustavo Geller - vitorgg_hz@hotmail.com\n"; info_gerais += aux
    aux = "     Lucas Camargo da Silva Tassinari - lucascst@hotmail.com\n"; info_gerais += aux
    aux = "     Daniel Gustavo Allasia P. - dallasia@gmail.com\n\n"; info_gerais += aux
    aux = "Citar como: Geller, V.G.; Tassinari, L.C.S.; Allasia, D.G., Modelo Hidrológico Ecotecnologias, versão 1. Santa Maria/RS.\n\n"; info_gerais += aux
    aux = "Boas simulações!"; info_gerais += aux
    #----------------------------------------------------------------------
    def __init__(self, master, versao_do_software, diretorio_do_software):
        self.master = master
        self.versao_do_software = versao_do_software
        self.diretorio_do_software = diretorio_do_software
    
        #   Cria a janela
        Toplevel.__init__(self, bg="#DFF9CA")
        #   Configurar a janela
        self.resizable(width=False, height=False)
        self.title("MHE - Sobre" )
        self.protocol("WM_DELETE_WINDOW", self.fecharJanelaAbout)
        #   Introduzir o frame
        primeiroFrame = Frame(self, bg="#DFF9CA")
        primeiroFrame.pack(padx = 10, pady = 10)
        
        #   Titulo
        Label(primeiroFrame, text = "Modelo Hidrológico Ecotecnologias", bg="#DFF9CA").grid(row = 0, column = 0, columnspan = 2, sticky = 'n', padx = 10, pady = 5)

        #   Text Box
        self.cxTexto = tkst.ScrolledText(primeiroFrame, height = 0, width = 0, wrap=WORD)
        #   Posicionar
        self.cxTexto.grid(row = 1, column = 0, columnspan = 2, rowspan = 1, sticky = 'n', padx = 15, pady = 0, ipadx=400, ipady=240) #ipadx=227, ipady=120
        
        #   Quero editar
        self.cxTexto.insert(END, self.info_gerais)
        self.cxTexto.configure(state="disabled", font=(10))
        
        self.cxTexto.focus()
        
        Label(primeiroFrame, text = "23 de janeiro de 2020.", bg="#DFF9CA").grid(row = 2, column = 0, columnspan = 2, sticky = 'w', padx = 10, pady = 5)
        
        Button(primeiroFrame, text = "Fechar", width = 10, command=lambda: self.fecharJanelaAbout()).grid(row = 2, column = 1, columnspan = 1, sticky = 'e', padx = 15, pady = 5)
        
        #   Centralizar a janela do programa no monitor
        self.centralizar(self)
    #----------------------------------------------------------------------
    def fecharJanelaAbout(self):
        #   Fechar a janela
        self.destroy()
        
        #   Reinicio a janela principal
        Modelo_Hidrologico_Ecotecnologias.Application(self.master, self.versao_do_software, self.diretorio_do_software)
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