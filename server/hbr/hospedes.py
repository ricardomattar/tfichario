# -*- coding: latin1 -*-
"""
Created on Wed Sep 30 06:17:47 2015

@author: ricardo
"""

import datetime
import json
import traceback

import logging
import logging.handlers
logger = logging.getLogger()

from sqlalchemy import or_
from . import db

from . import helpers

def gerar_alerta_alteracao(**kwargs):
    pass

def rpc_authenticate(params):
    return 200, True
    
def rpc_new_id(params):
    return (200, db.models.suuid())
    
def rpc_get(params):
    try:
        uuid = params['uuid']
        session = db.db.session_maker()
        query = session.query(db.models.Hospede).filter(db.models.Hospede.uuid==uuid)
        result = (200, db.helper.row2dict(query.first()))
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())
        
    finally:
        session.close()
        
    return result
                    
def rpc_query(params):
    if len(params['query']) < 2:
        return (200, {})
    try:
        qs = params['query'].strip()
        session = db.db.session_maker()
        q = session.query(db.models.Hospede)         \
            .order_by(db.models.Hospede.nome)        \
            .filter(or_                              \
            (db.models.Hospede.nome.ilike(qs + '%'), \
             db.models.Hospede.cpf.ilike(qs + '%'),  \
             db.models.Hospede.rg.ilike(qs + '%'))).all()
                    
        result_list = []
        for r in q:
            result_list.append(db.helper.row2dict(r))
            
        result = (200, result_list)
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())

    finally:
        session.close()
        
    return result
    
def rpc_save(params):
    try:        
        session = db.db.session_maker()
        uuid = params['uuid']
        if uuid == '':
            result = (500, 'Sem ID')
            raise Exception('Sem ID')
            
        hospede = session.query(db.models.Hospede).filter(db.models.Hospede.uuid==uuid).first()
        if len(params['nome']) < 3:
            result = (500, 'Nome curto demais')
            raise Exception('Nome curto demais')
            
        if params['cpf'] == '':
            params['cpf'] == None
            
        else:
            params['cpf'] = helpers.dados.somente_numeros(params['cpf'])
            if helpers.cpf.validate(params['cpf']):
                h = session.query(db.models.Hospede).filter(db.models.Hospede.cpf==params['cpf']).first() 
                if h and h.uuid != uuid:
                    result = (500, 'CPF duplicado')
                    raise Exception('CPF duplicado')
                    
            else:
                result = (500, 'CPF invalido')
                raise Exception('CPF invalido')
            
        if params['rg'] == '':
            params['rg'] == None
        else:
            #params['rg'] = helpers.dados.somente_numeros(params['rg'])
            h = session.query(db.models.Hospede).filter(db.models.Hospede.rg==params['rg']).first() 
            if h and h.uuid != uuid:
                result = (500, 'RG duplicado')
                raise Exception('RG duplicado')
            
        if params['nascimento'] == '':
            params['nascimento'] = None
            
        if params['nascimento'] != None:            
            try:
                datetime.datetime.strptime(params['nascimento'], "%d/%m/%Y")
                
            except:
                result = (500, 'Data de nascimento incorreta')
                raise Exception('Data de nascimento invalida')
            
        if hospede:
            update(params)
        else:
            insert(params)
            
        result = (200, True)
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())
        
    finally:
        session.close()
        
    return result
        
def insert(params):
    try:
        session = db.db.session_maker()
        hospede = db.models.Hospede()
        
        hospede.uuid          = params['uuid'] #(String(64)    , primary_key = True, default=suuid)
        #hospede.data_cadastro = params['data_cadastro'] #(DateTime      , nullable = False, default=datetime.datetime.utcnow)
    
        nome = params['nome'].upper()
        nomesa = helpers.dados.remove_acentuacao(nome)
        nomesa = nomesa.upper()
        nome_soundex = helpers.dados.soundex(nome)
                
        hospede.nome          = nomesa
        hospede.nomesoundex   = nome_soundex
        hospede.mae           = params['mae']
        hospede.cpf           = params['cpf'] #(String(40)   , nullable = False)
        hospede.rg            = params['rg'] #(String(40)   , nullable = False)
        hospede.naturalidade  = params['naturalidade'] #(String(100))
        hospede.nascimento    = params['nascimento'] #(DateTime)
        hospede.nacionalidade = params['nacionalidade'] #(String(100))
        
        hospede.profissao     = params['profissao'] #(String(100))
        hospede.empresa       = params['empresa'] #(String(100))
        
        hospede.carroplaca    = params['carroplaca'] #(String(40))
        hospede.procedencia   = params['procedencia'] #(String(100))
        hospede.destino       = params['destino'] #(String(100))
        
        hospede.endereco      = params['endereco'] #(String(100))
        hospede.bairro        = params['bairro'] #(String(100))
        hospede.cidade        = params['cidade'] #(String(100))
        hospede.estado        = params['estado'] #(String(100))
        hospede.cep           = params['cep'] #(String(100))
        hospede.telefones     = params['telefones'] #(String(100))
        hospede.email         = params['email'] #(String(100))
        hospede.extras        = params['extras'] #(String(100))        
        hospede.usuario       = params['usuario'] #(String(100))        
        
        session.add(hospede)
        session.commit()
        
    except:
        logger.exception('')
        session.rollback()
        session.close()
        raise
        
    finally:
        session.close()
        
def update(params):
    try:
        session = db.db.session_maker()
        uuid = params['uuid']
        hospede = session.query(db.models.Hospede).filter(db.models.Hospede.uuid==uuid).first()
        
        nome = params['nome']
        nomesa = helpers.dados.remove_acentuacao(nome)
        nomesa = nomesa.upper()
        nome_soundex = helpers.dados.soundex(nome)        
        
        alterado = False        
        if hospede.nome          != nomesa:
            gerar_alerta_alteracao(tabela='hospedes', registro=uuid)
            alterado = True
            
        if hospede.nomesoundex   != nome_soundex: alterado = True
        if hospede.mae           != params['mae']: alterado = True
        if hospede.cpf           != params['cpf']:
            gerar_alerta_alteracao(tabela='hospedes cpf', registro=uuid)
            alterado = True
            
        if hospede.rg            != params['rg']:
            gerar_alerta_alteracao(tabela='hospedes rg', registro=uuid)
            alterado = True
            
        if hospede.naturalidade  != params['naturalidade']: alterado = True
        if hospede.nascimento    != params['nascimento']: alterado = True
        if hospede.nacionalidade != params['nacionalidade']: alterado = True
        
        if hospede.profissao     != params['profissao']: alterado = True
        if hospede.empresa       != params['empresa']: alterado = True
        
        if hospede.carroplaca    != params['carroplaca']: alterado = True
        if hospede.procedencia   != params['procedencia']: alterado = True
        if hospede.destino       != params['destino']: alterado = True
        
        if hospede.endereco      != params['endereco']: alterado = True
        if hospede.bairro        != params['bairro']: alterado = True
        if hospede.cidade        != params['cidade']: alterado = True
        if hospede.estado        != params['estado']: alterado = True
        if hospede.cep           != params['cep']: alterado = True
        if hospede.telefones     != params['telefones']: alterado = True
        if hospede.email         != params['email']: alterado = True
        if hospede.extras        != params['extras']: alterado = True

        if alterado:
            registro = db.helper.row2dict(hospede)
            data = str(datetime.datetime.now())
            registro_alteracao = {}
            registro_alteracao['registro'] = registro
            registro_alteracao['data'] = data
            
            registro = db.models.HospedeAlteracoes()
            registro.uuid = uuid
            registro.registro = json.dumps(registro_alteracao)
            session.add(registro)
            
        
        hospede.Nome          = nomesa
        hospede.NomeSoundex   = nome_soundex
        hospede.mae           = params['mae']
        hospede.cpf           = params['cpf'] #(String(40)   , nullable = False)
        hospede.rg            = params['rg'] #(String(40)   , nullable = False)
        hospede.naturalidade  = params['naturalidade'] #(String(100))
        hospede.nascimento    = params['nascimento'] #(DateTime)
        hospede.nacionalidade = params['nacionalidade'] #(String(100))
        
        hospede.profissao     = params['profissao'] #(String(100))
        hospede.empresa       = params['empresa'] #(String(100))
        
        hospede.carroplaca    = params['carroplaca'] #(String(40))
        hospede.procedencia   = params['procedencia'] #(String(100))
        hospede.destino       = params['destino'] #(String(100))
        
        hospede.endereco      = params['endereco'] #(String(100))
        hospede.bairro        = params['bairro'] #(String(100))
        hospede.cidade        = params['cidade'] #(String(100))
        hospede.estado        = params['estado'] #(String(100))
        hospede.cep           = params['cep'] #(String(100))
        hospede.telefones     = params['telefones'] #(String(100))
        hospede.email         = params['email'] #(String(100))
        hospede.extras        = params['extras'] #(String(100))        
        hospede.usuario       = params['usuario'] #(String(100))        
        
        session.commit()
        
    except:
        logger.exception('')
        session.rollback()
        session.close()
        raise

    finally:
        session.close()
        