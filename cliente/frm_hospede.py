# -*- coding: latin1 -*-
"""
Created on Wed Sep  2 04:31:00 2015

@author: ricardo
"""

#!/usr/bin/env python
# -*- coding: latin1 -*-

import Tkinter

from tkhelper import TkString
from tkhelper import TkText
from tkhelper import TkOption
from tkhelper import TkButton
from tkhelper import Search

import post
import glb

    
class FHospede:
    def __init__(self, master):
        self.master = master
                
        self.search_frame = Search(parent = self.master,
                                     rowspan = 20,
                                     width = 50,
                                     command_search = self.search,
                                     command_listclick = self.record_list_click,
                                     header={'nome': (0, 'Nome', 25),
                                             'cpf':  (1, 'CPF',  12),
                                             'rg':   (2, 'RG',   12),
                                             'uuid': (3, 'ID',   15)})
                                             
        form_frame = Tkinter.LabelFrame(self.master, text = 'Hospede')        
        form_frame.grid(row = 0, column = 5, sticky = Tkinter.N)
        
        #Record frame
        col0 = Tkinter.Frame(form_frame)
        col0.grid(row = 0, column = 0, sticky = Tkinter.N)
        self.uuid           = TkString(col0, u'UUID',           0, 0, 1, 0, 55)
        self.data_cadastro  = TkString(col0, u'Data cadastro',  0, 1, 1, 1, 45)
        
        self.nome           = TkString(col0, u'Nome',           0, 2, 1, 2, 55)
        self.mae            = TkString(col0, u'Mae',            0, 3, 1, 3, 55)
        self.cpf            = TkString(col0, u'Cpf',            0, 4, 1, 4, 20)
        self.rg             = TkString(col0, u'Rg',             0, 5, 1, 5, 20)
        self.naturalidade   = TkString(col0, u'Naturalidade',   0, 6, 1, 6, 55)
        self.nascimento     = TkString(col0, u'Nascimento',     0, 7, 1, 7, 55)
        self.nacionalidade  = TkString(col0, u'Nacionalidade',  0, 8, 1, 8, 55)

        self.profissao      = TkString(col0, u'Profissao',      0, 9, 1, 9, 55)
        self.empresa        = TkString(col0, u'Empresa',        0, 10, 1, 10, 55)

        self.carroplaca     = TkString(col0, u'Placa carro',    0, 11, 1, 11, 55)
        self.procedencia    = TkString(col0, u'Procedencia',    0, 12, 1, 12, 55)
        self.destino        = TkString(col0, u'Destino',        0, 13, 1, 13, 55)

        self.endereco       = TkString(col0, u'Endereco',       0, 14, 1, 14, 55)
        self.bairro         = TkString(col0, u'Bairro',         0, 15, 1, 15, 55)
        self.cidade         = TkString(col0, u'Cidade',         0, 16, 1, 16, 55)
        self.estado         = TkString(col0, u'Estado',         0, 17, 1, 17, 55)
        self.cep            = TkString(col0, u'Cep',            0, 18, 1, 18, 55)
        self.telefones      = TkString(col0, u'Telefones',      0, 19, 1, 19, 55)
        self.email          = TkString(col0, u'Email',          0, 20, 1, 20, 55)
        
        col1 = Tkinter.Frame(form_frame)
        col1.grid(row = 0, column = 1, sticky = Tkinter.N)
        self.extras         = TkText(col1, u'Extras',           0, 0, 0, 1, 35, 20)
        self.usuario        = TkString(col1, u'Operador',       0, 18, 0, 19, 35)
        
        self.uuid.widget.configure(state='readonly', takefocus=0)
        self.data_cadastro.widget.configure(state='readonly', takefocus=0)
        self.usuario.widget.configure(state='readonly', takefocus=0)
        
        rec_frame = Tkinter.LabelFrame(form_frame, text = '')
        rec_frame.grid(row = 28, column = 0, sticky = Tkinter.N)
        self.button_save = TkButton(rec_frame, label="Salvar", col=0, row=0, command=self.save)
        self.button_new = TkButton(rec_frame, label="Nova ficha", col=2, row=0, command=self.new)
        self.button_new.button.grid(padx=100)
        

        self.fields = {}
        self.fields['uuid'] = self.uuid
        self.fields['data_cadastro'] = self.data_cadastro
        self.fields['nome'] = self.nome
        self.fields['mae'] = self.mae
        self.fields['cpf'] = self.cpf
        self.fields['rg'] = self.rg
        self.fields['naturalidade'] = self.naturalidade
        self.fields['nascimento'] = self.nascimento
        self.fields['nacionalidade'] = self.nacionalidade
        self.fields['profissao'] = self.profissao
        self.fields['empresa'] = self.empresa
        self.fields['carroplaca'] = self.carroplaca
        self.fields['procedencia'] = self.procedencia
        self.fields['destino'] = self.destino
        self.fields['endereco'] = self.endereco 
        self.fields['bairro'] = self.bairro
        self.fields['cidade'] = self.cidade
        self.fields['estado'] = self.estado
        self.fields['cep'] = self.cep
        self.fields['telefones'] = self.telefones
        self.fields['email'] = self.email
        self.fields['extras'] = self.extras
        self.fields['usuario'] = self.usuario
                
        
    def clear_form(self):
        for key in self.fields.keys():
            self.fields[key].set('')
                    
    def save(self):
        params = {}
        params['method'] = 'hospedes.rpc_save'
        for key in self.fields.keys():
            params[key] = self.fields[key].get().strip()
                    
        params['usuario'] = glb.username
        
        if post.call(**params):
            self.show_record(self.uuid.get())
    
    def new(self):
        self.clear_form()
        self.uuid.set(post.call(method='hospedes.rpc_new_id'))
        self.nome.widget.focus()
        
    def record_list_click(self, record):
        self.show_record(record['uuid'])
        
    def show_record(self, uuid):
        hospede = post.call(method='hospedes.rpc_get', uuid=uuid)

        for key in self.fields.keys():
            self.fields[key].set(hospede[key].strip())
                        

    def search(self, search_text):
        pesquisa = post.call(username=glb.username, password=glb.password,
                             method='hospedes.rpc_query',
                             query=search_text)
        self.search_frame.set_list(pesquisa)
                