# -*- coding: latin1 -*-
"""
Created on Wed Sep  2 04:31:00 2015

@author: ricardo
"""

#!/usr/bin/env python
# -*- coding: latin1 -*-

import Tkinter

from tkhelper import TkString
from tkhelper import TkOption
from tkhelper import TkButton

import post
import glb

    
class FUsuario:
    def __init__(self, master):
        self.master = master
                        
        form_frame = Tkinter.LabelFrame(self.master, text = 'Usuario')
        rec_frame = Tkinter.LabelFrame(form_frame, text = '')
        search_frame = Tkinter.LabelFrame(self.master, text = 'Procura')
        
        form_frame.grid(row = 0, column = 5, sticky = Tkinter.N)
        rec_frame.grid(row = 28, column = 0, sticky = Tkinter.N)
        
        search_frame.grid(row = 0, column = 0, sticky = Tkinter.N)
                
        #user frame
        status_list = ("ativo", "inativo")
        self.usuario_id    = TkString(form_frame, u'UUID',            0, 0, 1, 0, 64)
        self.nome          = TkString(form_frame, u'Nome',            0, 1, 1, 1, 80)
        self.status        = TkOption(form_frame, u'Situação',        0, 2, 1, 2, 20, status_list)
        self.classe        = TkString(form_frame, u'Classe',          0, 3, 1, 3, 20)
        self.email         = TkString(form_frame, u'E-Mail',          0, 4, 1, 4, 80)
        self.last_login    = TkString(form_frame, u'Ultimo login',    0, 5, 1, 5, 45)
        self.data_cadastro = TkString(form_frame, u'Data cadastro',   0, 6, 1, 6, 45)
        self.senha         = TkString(form_frame, u'Senha',           0, 7, 1, 7, 45)
        
        self.usuario_id.widget.configure(state='readonly', takefocus=0)
        self.last_login.widget.configure(state='readonly', takefocus=0)
        self.data_cadastro.widget.configure(state='readonly', takefocus=0)
        
        self.button_save = TkButton(rec_frame, label="Salvar", col=0, row=1, command=self.save)
        self.button_new = TkButton(rec_frame, label="Novo usuario", col=0, row=0, command=self.new)
        
        
        self.yScroll  =  Tkinter.Scrollbar ( search_frame, orient=Tkinter.VERTICAL )
        self.yScroll.grid ( row=0, column=1, rowspan=20, sticky=Tkinter.N+Tkinter.S )
        
        self.uservar = Tkinter.StringVar()
        self.userlist = Tkinter.Listbox(search_frame, listvariable = self.uservar, \
            selectmode = Tkinter.SINGLE, yscrollcommand=self.yScroll.set, height = 20)
        self.userlist.config(width=40)
        self.userlist.grid(row=0, column=0, rowspan=20, sticky = Tkinter.W)
        self.uservar.set('')
        self.yScroll["command"]  =  self.userlist.yview
        
        self.userlist.bind ( "<ButtonRelease-1>", self.userlist_click )
        
        Tkinter.Label(search_frame, text="Procurar").grid(column = 0, row=29, sticky=Tkinter.W)
        self.text_search = TkString(search_frame, u'Procurar',   0, 29, 0, 30, 40, command=self.search)
                
        
    def clear_form(self):
        self.usuario_id    .set('')
        self.nome          .set('')
        self.status        .set('')
        self.classe        .set('')
        self.email         .set('')
        self.last_login    .set('')
        self.data_cadastro .set('')
        self.senha         .set('')
        
    def save(self):
        if post.call(method='usuarios.rpc_save',
                  usuario_id=self.usuario_id.get(),
                  nome= self.nome.get(),
                  status=self.status.get(),
                  classe=self.classe.get(),
                  email=self.email.get(),
                  password=self.senha.get()):
            self.mostrar_usuario(self.usuario_id.get())
    
    def new(self):
        self.clear_form()
        self.status.set('Ativo')
        self.usuario_id.set(post.call(method='usuarios.rpc_new_id'))
        self.nome.widget.focus()
        
    def userlist_click(self, event):
        user = self.userlist.get(self.userlist.curselection()[0])
        nome, classe, usuario_id = user.split(' | ')
        self.mostrar_usuario(usuario_id)
        
    def mostrar_usuario(self, usuario_id):
        self.usuario_corrent = usuario_id
        usuario = post.call(method='usuarios.rpc_get', usuario_id=usuario_id)
        
        self.usuario_id    .set(usuario['usuario_id'])
        self.nome          .set(usuario['nome'])
        self.status        .set(usuario['status'])
        self.classe        .set(usuario['classe'])
        self.email         .set(usuario['email'])
        self.last_login    .set(usuario['last_login'])
        self.data_cadastro .set(usuario['cadastro_data'])
        self.senha         .set(usuario['password'])
        

    def search(self, event):
        pesquisa = post.call(username=glb.username, password=glb.password,
                             method='usuarios.rpc_query',
                             nome=self.text_search.get())
        self.userlist.delete(0, Tkinter.END)
        lst = [ '%s | %s | %s' % (i['nome'], i['classe'], i['usuario_id']) for i in pesquisa]
        sl = sorted(lst, key=lambda s: s.lower())
        for item in sl:
            self.userlist.insert(Tkinter.END, item )
        
        