# -*- coding: latin1 -*-
"""
Created on Wed Sep  2 04:31:00 2015

@author: ricardo
"""

#!/usr/bin/env python
# -*- coding: latin1 -*-

import Tkinter

from tkhelper import TkString
from tkhelper import TkPassword
from tkhelper import TkText
from tkhelper import TkOption
from tkhelper import TkButton
from tkhelper import Search

import post
import glb

    
class FPassword:
    def __init__(self, master):
        self.master = master
                                                             
        form_frame = Tkinter.LabelFrame(self.master, text = 'Mudar senha')        
        form_frame.grid(row = 0, column = 5, sticky = Tkinter.N)
        
        #Record frame
        col0 = Tkinter.Frame(form_frame)
        col0.grid(row = 0, column = 0, sticky = Tkinter.N)
        self.username           = TkString(col0, u'Nome',            0, 0, 1, 0, 60)
        self.password           = TkPassword(col0, u'Senha atual',   0, 1, 1, 1, 45)
        
        self.new_password1      = TkPassword(col0, u'Nova senha',    0, 2, 1, 2, 45)
        self.new_password2      = TkPassword(col0, u'Repetir senha', 0, 3, 1, 3, 45)
        
        
        rec_frame = Tkinter.Frame(form_frame)
        rec_frame.grid(row = 28, column = 0, sticky = Tkinter.N)
        self.button_save = TkButton(rec_frame, label="Salvar", col=0, row=0, command=self.save)
        

        self.fields = {}
        self.fields['username'] = self.username
        self.fields['password'] = self.password
        self.fields['new_password1'] = self.new_password1
        self.fields['new_password2'] = self.new_password2
                
        
    def clear_form(self):
        for key in self.fields.keys():
            self.fields[key].set('')
                    
    def save(self):
        params = {}
        params['method'] = 'usuarios.rpc_change_password'
        for key in self.fields.keys():
            params[key] = self.fields[key].get().strip()
            
        ou = glb.username
        op = glb.password
        
        glb.username = self.username.get()
        glb.password = self.password.get()        
        
        if post.call(**params):
            glb.info('Senha modificada')
        else:
            glb.info('Falha')

        glb.usuario_id = ''            
        glb.username = ou
        glb.password = op
        
        self.clear_form()
        self.master.event_generate('<<logoff>>')
