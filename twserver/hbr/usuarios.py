# -*- coding: latin1 -*-
"""
Created on Mon Aug  3 12:33:22 2015

@author: ricardo
"""

import hashlib
import traceback

import logging
import logging.handlers
logger = logging.getLogger()

import db

def require(profile_list):
    def wrapper(func):
        def check_profile(params):
            if params['__classe__'] in profile_list:
                return func(params)
            else:
                return (401, 'Unauthorized')
        return check_profile
    return wrapper
    
def rpc_new_id(params):
    return (200, db.models.suuid())

def rpc_authenticate(params):
    return 200, True
    
@require(['admin', 'gerente'])
def rpc_get(params):
    try:
        usuario_id = params['usuario_id']
        session = db.session_maker()
        query = session.query(db.models.Usuario).filter(db.models.Usuario.usuario_id==usuario_id)
        result = (200, db.helper.row2dict(query.first()))
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())
        
    finally:
        session.close()
        
    return result

#@require(['admin', 'gerente'])
#def rpc_find(params):
#    return find(params)

def find(params):
    try:
        nome = params['nome']
        session = db.session_maker()
        query = session.query(db.models.Usuario).filter(db.models.Usuario.nome==nome)
        result = (200, db.helper.row2dict(query.first()))
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())
        
    finally:
        session.close()
    return result
            
#@require(['admin', 'gerente'])
#def rpc_findbyid(params):
#    usuario_id = params['usuario_id']
#    session = db.session_maker()
#    query = session.query(db.models.Usuario).filter(db.models.Usuario.usuario_id==usuario_id)
#    return query.first()

@require(['admin', 'gerente'])
def rpc_query(params):
    try:
        nome = params['nome']
        session = db.session_maker()
        q = session.query(db.models.Usuario).filter(db.models.Usuario.nome.ilike(nome + '%'))
        result_list = []
        for r in q:
            result_list.append(db.helper.row2dict(r))
            
        result = (200, result_list)
    except:
        logger.exception()
        result = (500, traceback.format_exc())
        
    finally:
        session.close()
        
    return result

@require(['admin', 'gerente'])
def rpc_save(params):
    try:
        session = db.session_maker()
        usuario_id = params['usuario_id']
        usuario = session.query(db.models.Usuario).filter(db.models.Usuario.usuario_id==usuario_id).first() 
        if usuario:
            res = update(params)
        else:
            res = insert(params)
            
        result = (200, res)
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())
        
    finally:
        session.close()
        
    return result
    
def insert(params):
    try:
        if params['password'].strip() == '':
            raise Exception('Senha vazia')
            
        session = db.session_maker()
        novo_usuario = db.models.Usuario()
        novo_usuario.usuario_id              = params['usuario_id']
        #novo_usuario.cadastro_data           = Column(DateTime   , nullable = False, default=datetime.datetime.utcnow)
        #novo_usuario.last_login              = Column(DateTime   , nullable = False, default=datetime.datetime.utcnow)
        novo_usuario.email                   = params['email']
        novo_usuario.status                  = params['status']
        if params['classe'] != '':
            novo_usuario.classe              = params['classe']
        novo_usuario.nome                    = params['nome']
        novo_usuario.password                = hashlib.sha1(params['password']).hexdigest()
        session.add(novo_usuario)
        session.commit()
        result = True
        
    except:
        logger.exception('')
        result = False

    finally:
        session.close()
        
    return result
        
def update(params):
    try:
        session = db.session_maker()
        usuario_id = params['usuario_id']
        usuario = session.query(db.models.Usuario).filter(db.models.Usuario.usuario_id==usuario_id).first() 
        #novo_usuario.usuario_id              = Column(String(32)       , primary_key = True, default=suuid)
        #novo_usuario.cadastro_data           = Column(DateTime   , nullable = False, default=datetime.datetime.utcnow)
        #novo_usuario.last_login              = Column(DateTime   , nullable = False, default=datetime.datetime.utcnow)
        usuario.email                   = params['email']
        usuario.status                  = params['status']
        usuario.classe                  = params['classe']
        usuario.nome                    = params['nome']
        usuario.password                = hashlib.sha1(params['password']).hexdigest()
        session.commit()
        result = True
        
    except:
        logger.exception('')
        result = False        
        
    finally:
        session.close()
        
    return result
    
def rpc_change_password(params):
    try:
        if params['new_password1'] != params['new_password2']:
            raise Exception('Senha incorreta')
            
        session = db.session_maker()
        usuario = session.query(db.models.Usuario).filter(db.models.Usuario.nome==params['username']).first()
        usuario.password = hashlib.sha1(params['new_password1']).hexdigest()
        session.commit()
        result = (200, True)
        
    except:
        logger.exception('')
        result = (500, traceback.format_exc())  

    finally:
        session.close()
        
    return result
    
