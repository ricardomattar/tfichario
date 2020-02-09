# -*- coding: latin1 -*-
"""
Created on Fri Oct 16 16:15:01 2015

@author: ricardo
"""

import sys
import time
import datetime
import traceback

import dados
import glb
import post

glb.username = 'import'
glb.password = 'skandar'

arquivo = sys.argv[1]

def error(a):
    print a

glb.error = error
    
e = 0
p = 0
pi = 0
s = 0
f = 0


for line in open(arquivo).readlines():
    try:
        record  = line.split('^|^')
        intID                 , \
        blnAtivo              , \
        strCodigo             , \
        blnEmpresa            , \
        strNome               , \
        strTipo               , \
        strCnpjCpf            , \
        datNascimento         , \
        strIeRg               , \
        strDocs               , \
        strEndereco           , \
        strBairro             , \
        strCidade             , \
        strEstado             , \
        strCep                , \
        strTelefones          , \
        strContato            , \
        strEmail              , \
        strSite               , \
        strBanco              , \
        strAgencia            , \
        strConta              , \
        strExtras             = record
        
        intID         =  intID          .strip().strip('"').strip() 
        blnAtivo      =  blnAtivo       .strip().strip('"').strip() 
        strCodigo     =  strCodigo      .strip().strip('"').strip() 
        blnEmpresa    =  blnEmpresa     .strip().strip('"').strip() 
        strNome       =  strNome        .strip().strip('"').strip() 
        strTipo       =  strTipo        .strip().strip('"').strip() 
        strCnpjCpf    =  strCnpjCpf     .strip().strip('"').strip() 
        datNascimento =  datNascimento  .strip().strip('"').strip() 
        strIeRg       =  strIeRg        .strip().strip('"').strip() 
        strDocs       =  strDocs        .strip().strip('"').strip() 
        strEndereco   =  strEndereco    .strip().strip('"').strip() 
        strBairro     =  strBairro      .strip().strip('"').strip()
        strCidade     =  strCidade      .strip().strip('"').strip()
        strEstado     =  strEstado      .strip().strip('"').strip() 
        strCep        =  strCep         .strip().strip('"').strip() 
        strTelefones  =  strTelefones   .strip().strip('"').strip() 
        strContato    =  strContato     .strip().strip('"').strip() 
        strEmail      =  strEmail       .strip().strip('"').strip() 
        strSite       =  strSite        .strip().strip('"').strip() 
        strBanco      =  strBanco       .strip().strip('"').strip() 
        strAgencia    =  strAgencia     .strip().strip('"').strip() 
        strConta      =  strConta       .strip().strip('"').strip() 
        strExtras     =  strExtras      .strip().strip('"').strip()        
        
        cnpjcpf = strCnpjCpf.strip('"')
        if long(intID):
            if dados.cnpj.validate(cnpjcpf):
                e = e + 1
            elif dados.cpf.validate(cnpjcpf):
                p = p + 1
                #print blnEmpresa, strNome, nl
#                print 'intID              ',   intID            
#                print 'blnAtivo           ',   blnAtivo         
#                print 'strCodigo          ',   strCodigo        
#                print 'blnEmpresa         ',   blnEmpresa       
#                print 'strNome            ',   strNome          
#                print 'strTipo            ',   strTipo          
#                print 'strCnpjCpf         ',   strCnpjCpf       
#                print 'datNascimento      ',   datNascimento    
#                print 'strIeRg            ',   strIeRg          
#                print 'strDocs            ',   strDocs          
#                print 'strEndereco        ',   strEndereco      
#                print 'strBairro          ',   strBairro     
#                print 'strCidade          ',   strCidade     
#                print 'strEstado          ',   strEstado        
#                print 'strCep             ',   strCep           
#                print 'strTelefones       ',   strTelefones     
#                print 'strContato         ',   strContato       
#                print 'strEmail           ',   strEmail         
#                print 'strSite            ',   strSite          
#                print 'strBanco           ',   strBanco         
#                print 'strAgencia         ',   strAgencia       
#                print 'strConta           ',   strConta         
#                print 'strExtras          ',   strExtras     
#                print

                params = {}                
                params['method'] = 'hospedes.rpc_new_id'
                uuid = post.call(**params)
                
                params = {}                
                params['mae']            = ''
                params['cpf']            = ''
                params['rg']             = ''
                params['naturalidade']   = ''
                params['nascimento']     = ''
                params['nacionalidade']  = ''
                params['profissao']      = ''
                params['empresa']        = ''
                params['carroplaca']     = ''
                params['procedencia']    = ''
                params['destino']        = ''
                params['endereco']       = ''
                params['bairro']         = ''
                params['cidade']         = ''
                params['estado']         = ''
                params['cep']            = ''
                params['telefones']      = ''
                params['email']          = ''
                params['extras']         = ''
                params['usuario'] = glb.username        
                
                params['uuid'] = uuid
#                params['xxx']          = intID       
#                params['xxx']          = blnAtivo    
#                params['xxx']          = strCodigo   
#                params['xxx']          = blnEmpresa  
                params['nome']         = strNome     
#                params['xxx']          = strTipo     
                params['cpf']          = strCnpjCpf  
                try:
                    do = datetime.datetime.strptime(datNascimento, '%m/%d/%y %H:%M:%S')
                    do = datetime.datetime(do.year - 100, do.month, do.day, do.hour, do.minute, do.second)
                    datanascimento = datetime.datetime.strftime(do, '%d/%m/%Y')
                    
                except:
                    datanascimento = ''
                params['nascimento']   = datanascimento
                params['rg']           = strIeRg     
#                params['xxx']          = strDocs     
                params['endereco']     = strEndereco 
                params['bairro']       = strBairro   
                params['cidade']       = strCidade   
                params['estado']       = strEstado   
                params['cep']          = strCep      
                params['telefones']    = strTelefones
#                params['xxx']          = strContato  
                params['email']        = strEmail    
#                params['xxx']          = strSite     
#                params['xxx']          = strBanco    
#                params['xxx']          = strAgencia  
#                params['xxx']          = strConta    
                params['extras']       = strExtras   
                
                params['method'] = 'hospedes.rpc_save'
                if post.call(**params):
                    s += 1
                else:
                    f += 1

            else:
                pi = pi + 1
        
    except:
        print traceback.format_exc()
        
        
print e, p, pi
print s, f