# -*- coding: latin_1 -*-

import sys
if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *
    
from PIL import Image, ImageTk
import tkMessageBox
import tkFileDialog
#import sys
import os
#import shutil
##import time
#import numpy as np


class InterfaceAjuda:
            
    def fecharJanela(self):
        self.master.destroy()
    
#-----------------------------------------------------------           

    def __init__(self, master):
        
        self.master = master
        
        self.master.resizable(width=False, height=False)
        self.master.title("MODELO HIDROLOGICO ECOTECNOLOGIAS - " + VERSAO + " Ajuda")
        
        primeiroFrame = Frame(self.master)
        primeiroFrame.pack()
        
        segundoFrame = Frame(self.master)
        segundoFrame.pack(pady = 5)
        
        #----------------------------------------------------------------------------------------------------------------#        

            #Bi de ibaaaagens cobandante habilton!
        
        imagemAjuda = ImageTk.PhotoImage(Image.open(DIRETORIO_EXECUTAVEL + "\Ajuda.png"))
        
        ajudaLabel = Label(primeiroFrame, image=imagemAjuda)
        ajudaLabel.pack(fill='both')

        ajudaLabel.image = imagemAjuda

        #----------------------------------------------------------------------------------------------------------------# 

        botaoFecharAjuda = Button(segundoFrame, text = 'Sair', width = 10, command = self.fecharJanela)
        botaoFecharAjuda.pack()

     
##################################################################################################################################################################

VERSAO = str( round( (160929/15000.) - 9,2 ) )  #(ano, mes, dia / 15 000) - 9 = versao com 3 digitos
DIRETORIO_EXECUTAVEL = os.path.dirname(os.path.abspath(sys.argv[0]))