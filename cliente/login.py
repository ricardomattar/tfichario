# -*- coding: latin1 -*-
"""
Created on Wed Sep  2 05:30:22 2015

@author: ricardo
"""


import Tkinter
import sys

from tkhelper import TkString
from tkhelper import TkPassword
from tkhelper import TkOption
from tkhelper import TkButton

import post
import glb

class User(object):
    username = None
    password = None
    
class Login:
    def __init__(self, master, user):
        self.master = master
        self.master.title('Login')
                
        self.frame = Tkinter.Frame(master, borderwidth=2)
        self.frame.pack()
        
        form_frame = Tkinter.LabelFrame(self.frame, text = 'Login')
        
        form_frame.grid(row = 0, column = 5, sticky = Tkinter.N)
        
        self.nome          = TkString(form_frame, u'Nome',        0, 1, 1, 1, 45)
        self.senha         = TkPassword(form_frame, u'Senha',     0, 7, 1, 7, 45)
        self.button_login = TkButton(form_frame, label="Login", col=0, row=10, command=self.login)
        
        self.nome.widget.focus()
        self.master.bind('<Return>', self.login)
        self.master.bind('<Escape>', self.quit)
                

    def login(self, *ev):
        glb.username = self.nome.get().strip()
        glb.password = self.senha.get().strip()
        try:
            if not post.call(method='usuarios.rpc_authenticate'):
                glb.username = None
                glb.password = None
        except:
            glb.username = None
            glb.password = None
                
        self.master.destroy()
        
    def quit(self, *ev):
        self.master.quit()
    
    def usuarios(self):
        pass
        
def log_in(master):
       window = Tkinter.Toplevel()
       window.focus_set()
       window.grab_set()
       window.transient(master)
       
       user = User()
       l = Login(window, user)
       window.wait_window(window)
       return (user.username, user.password)