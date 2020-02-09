# -*- coding: latin1 -*-
"""
Created on Wed Sep  2 05:30:22 2015

@author: ricardo
"""

#import tkinter
#import login
#
#root = tkinter.Tk()
#
#Mbox = login.Mbox
#Mbox.root = root
#
#D = {'user':'Bob'}
#
#b_login = tkinter.Button(root, text='Log in')
#b_login['command'] = lambda: Mbox('Name?', (D, 'user'))
#b_login.pack()
#
#b_loggedin = tkinter.Button(root, text='Current User')
#b_loggedin['command'] = lambda: Mbox(D['user'])
#b_loggedin.pack()
#
#root.mainloop()


import tkinter
from tkinter import ttk
import sys

from tkhelper import TkString
from tkhelper import TkOption
from tkhelper import TkButton
from tkhelper import TkText
from tkhelper import show_modal
from tkhelper import PasswordDialog

import glb
import login
import frm_password
import frm_usuario
import frm_hospede
    
    
class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Hotel')

        self.note = ttk.Notebook(self.master)
        self.note.grid(row=1, column=0)

        self.msg_frame = tkinter.Frame(self.master)
        self.msg_frame.grid(row = 2, column = 0)
        self.info  = TkText(self.msg_frame, u'',   0, 0, 1, 0, 55, 10)
        self.error = TkText(self.msg_frame, u'',   2, 0, 3, 0, 55, 10)
        self.event = TkText(self.msg_frame, u'',   4, 0, 5, 0, 55, 10)
        glb.info = self.info.set
        glb.error = self.error.set
        glb.event = self.event.set
                
        self.login_frame = tkinter.Frame(self.note)               
        self.button_frame = tkinter.LabelFrame(self.login_frame)
        self.button_frame.grid(row=0, column=0)
        self.password_frame = frm_password.FPassword(self.login_frame)
        
        self.button_login = TkButton(self.button_frame, label="Login", col=0, row=0, command=self.logar)
        self.button_logoff = TkButton(self.button_frame, label="Logoff", col=0, row=1, command=self.logar)
        
        self.tab_login = tkinter.Frame(self.note)
        self.note.add(self.login_frame, text="Login")
        
        self.tab_usuarios = tkinter.Frame(self.note)
        self.fusuario=frm_usuario.FUsuario(self.tab_usuarios)
        self.note.add(self.tab_usuarios, text="Usuarios")
        
        self.tab_hospedes = tkinter.Frame(self.note)
        self.fhospede=frm_hospede.FHospede(self.tab_hospedes)
        self.note.add(self.tab_hospedes, text="Hospedes")
        
        self.master.bind('<<logoff>>', self.logar)
        
        if glb.usuario_id == '':
            self.logar()        
                                
        
    def logar(self, *a, **ka):
        glb.usuario_id = ''
        glb.username = ''
        glb.password = ''
        
        if not glb.username:
            login.log_in(self.master)
            
        if not glb.username:
            sys.exit(0)
            
        self.master.title('Hotel ::: %s' % glb.username)            
        glb.info('%s' %(glb.username))
        
        
root = tkinter.Tk()
app = App(root)
root.mainloop()
sys.exit(0)

