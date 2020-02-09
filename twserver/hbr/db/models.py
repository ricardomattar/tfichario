# -*- coding: latin1 -*-
"""
Created on Wed Jul 29 03:10:17 2015

@author: ricardo
"""

import uuid
import datetime
import time
import json

from sqlalchemy import Column
from sqlalchemy import BigInteger
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Date
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.ext.declarative import declarative_base

#from sqlalchemy import create_engine
#engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/hotel')
#engine = create_engine('sqlite:///hotel_devel.db')

Base = declarative_base()

def suuid():
    return '%s-%s-%s' % (
        str(uuid.uuid4()),
        str(time.time()),
        str(hex(uuid.getnode()))[2:-1])

class Usuario(Base):
    __tablename__ = 'usuarios'
    usuario_id           = Column(String(64)    , primary_key = True, default = suuid)
    nome                 = Column(String(100)   , nullable = False, unique = True)
    password             = Column(String(128)   , nullable = False)
    email                = Column(String(100))
    cadastro_data        = Column(DateTime      , nullable = False, default = datetime.datetime.now)
    last_login           = Column(DateTime      , nullable = False, default = datetime.datetime.now)
    status               = Column(String(20)    , nullable = False, default = 'ativo')
    classe               = Column(String(20)    , nullable = False, default = 'operador')

    def __repr__(self):
        return "%s %s" % (self.usuario_id, self.nome)


class Hospede(Base):
    __tablename__ = 'hospedes'
    uuid          = Column(String(64)    , primary_key = True, default=suuid)
    data_cadastro = Column(DateTime      , nullable = False, default=datetime.datetime.now)

    nome          = Column(String(100)   , nullable = False)
    nomesoundex   = Column(String(100))
    mae           = Column(String(100))
    cpf           = Column(String(40))
    rg            = Column(String(40))
    naturalidade  = Column(String(100))
    nascimento    = Column(Date)
    nacionalidade = Column(String(100))
    
    profissao     = Column(String(100))
    empresa       = Column(String(100))
    
    carroplaca    = Column(String(40))
    procedencia   = Column(String(100))
    destino       = Column(String(100))
    
    endereco      = Column(String(100))
    bairro        = Column(String(100))
    cidade        = Column(String(100))
    estado        = Column(String(100))
    cep           = Column(String(40))
    telefones     = Column(String(100))
    email         = Column(String(100))
    extras        = Column(String())
    imagens       = Column(String())
    
    status        = Column(String(50))
    usuario       = Column(String(64))

#class Hospede(Base):
#    __tablename__ = 'hospedes'
#    uuid          = Column(String(64)    , primary_key = True, default=suuid)
#    data_cadastro = Column(DateTime      , nullable = False, default=datetime.datetime.now)
#
#    Nome          = Column(String(100)   , nullable = False)
#    NomeSoundex   = Column(String(100))
#    Cpf           = Column(String(40))
#    Rg            = Column(String(40))
#    Naturalidade  = Column(String(100))
#    Nascimento    = Column(Date)
#    Nacionalidade = Column(String(100))
#    
#    Profissao     = Column(String(100))
#    Empresa       = Column(String(100))
#    
#    CarroPlaca    = Column(String(40))
#    Procedencia   = Column(String(100))
#    Destino       = Column(String(100))
#    
#    Endereco      = Column(String(100))
#    Bairro        = Column(String(100))
#    Cidade        = Column(String(100))
#    Estado        = Column(String(100))
#    Cep           = Column(String(40))
#    Telefones     = Column(String(100))
#    Email         = Column(String(100))
#    Extras        = Column(String())
#    
#    Status        = Column(String(50))
#    Usuario       = Column(String(64))

class HospedeAlteracoes(Base):
    __tablename__ = 'hospedes_alteracoes'
    pkey          = Column(String(64) , primary_key = True, default=suuid)
    uuid          = Column(String(64), ForeignKey('hospedes.uuid'))
    data          = Column(DateTime, default=datetime.datetime.now)
    registro      = Column(String())


class Hospedagem(Base):
    __tablename__ = 'hospedagens'
    uuid          = Column(String(64)    , primary_key = True, default=suuid)
    entrada       = Column(DateTime)
    saida         = Column(DateTime)
    apto          = Column(String(64))
    fichas        = Column(String(400))
    adultos       = Column(BigInteger)
    criancas      = Column(BigInteger)
    valor_diaria  = Column(Numeric(precision=14, scale=2))
    procedencia   = Column(String(100))
    destino       = Column(String(100))
    conta        = Column(String(64))


class CategoriaApartamento(Base):
    __tablename__ = 'categorias_apartamentos'
    uuid         = Column(String(64)    , primary_key = True, default=suuid)
    categoria    = Column(String(100))
    precos       = Column(String())


class Apartamento(Base):
    __tablename__ = 'apartamentos'
    uuid         = Column(String(64)    , primary_key = True, default=suuid)
    numero       = Column(String(64))
    capacidade   = Column(BigInteger)
    configuracao = Column(String(100))
    categoria    = Column(String(64))
    status       = Column(String(50))

    
class Empresa(Base):
    __tablename__ = 'empresas'
    uuid         = Column(String(64)    , primary_key = True, default=suuid)
    nomefantasia = Column(String(100))
    razaosocial  = Column(String(100))
    cnpj         = Column(String(100))
    iest         = Column(String(100))

    #reservas
    reserva_contato   = Column(String(100))
    reserva_telefone  = Column(String(100))
    reserva_email     = Column(String(100))
    reserva_endereco  = Column(String(100))
    reserva_bairro    = Column(String(100))
    reserva_cidade    = Column(String(100))
    reserva_estado    = Column(String(100))
    reserva_cep       = Column(String(40))
    reserva_extras    = Column(String())
    
    #cobranca
    cobranca_contato   = Column(String(100))
    cobranca_telefone  = Column(String(100))
    cobranca_email     = Column(String(100))
    cobranca_endereco  = Column(String(100))
    cobranca_bairro    = Column(String(100))
    cobranca_cidade    = Column(String(100))
    cobranca_estado    = Column(String(100))
    cobranca_cep       = Column(String(40))
    cobranca_extras    = Column(String())
    
    #fiscal
    fiscal_contato   = Column(String(100))
    fiscal_telefone  = Column(String(100))
    fiscal_email     = Column(String(100))
    fiscal_endereco  = Column(String(100))
    fiscal_bairro    = Column(String(100))
    fiscal_cidade    = Column(String(100))
    fiscal_estado    = Column(String(100))
    fiscal_cep       = Column(String(40))
    fiscal_extras    = Column(String())
    
    
class Agencia(Base):
    __tablename__ = 'agencias'
    uuid         = Column(String(64)    , primary_key = True, default=suuid)
    nomefantasia = Column(String(100))
    razaosocial  = Column(String(100))
    cnpj         = Column(String(100))
    iest         = Column(String(100))
        
    taxa          = Column(Numeric(precision=5, scale=2))
    
    #reservas
    reserva_contato   = Column(String(100))
    reserva_telefone  = Column(String(100))
    reserva_email     = Column(String(100))
    reserva_endereco  = Column(String(100))
    reserva_bairro    = Column(String(100))
    reserva_cidade    = Column(String(100))
    reserva_estado    = Column(String(100))
    reserva_cep       = Column(String(40))
    reserva_extras    = Column(String())
    
    #cobranca
    cobranca_contato   = Column(String(100))
    cobranca_telefone  = Column(String(100))
    cobranca_email     = Column(String(100))
    cobranca_endereco  = Column(String(100))
    cobranca_bairro    = Column(String(100))
    cobranca_cidade    = Column(String(100))
    cobranca_estado    = Column(String(100))
    cobranca_cep       = Column(String(40))
    cobranca_extras    = Column(String())
    
    #fiscal
    fiscal_contato   = Column(String(100))
    fiscal_telefone  = Column(String(100))
    fiscal_email     = Column(String(100))
    fiscal_endereco  = Column(String(100))
    fiscal_bairro    = Column(String(100))
    fiscal_cidade    = Column(String(100))
    fiscal_estado    = Column(String(100))
    fiscal_cep       = Column(String(40))
    fiscal_extras    = Column(String())
        
class Reserva(Base):
    __tablename__ = 'reservas'
    uuid         = Column(String(64)    , primary_key = True, default=suuid)

    #reponsavel
    agencia           = Column(String(64))
    empresa           = Column(String(64))
    hospede           = Column(String(64))
                      
    operador          = Column(String(64))
    dataconfirmacao   = Column(DateTime())
                      
    hospede           = Column(String(64))
    apartamento       = Column(String(64))
    categoria         = Column(String(64))
    
    formapagamento    = Column(String(64)) #( faturado, balcao )
    pagarcomissao     = Column(Boolean())#  valor net ou comissionado
    valorvoucher      = Column(Numeric(precision=14, scale=2))#   (negociado)
    garantianoshow    = Column(Boolean())
    
    entrada_prevista  = Column(DateTime())
    saida_prevista    = Column(DateTime())
    
    valorpago         = Column(Numeric(precision=14, scale=2))
    confirmada        = Column(Boolean())
    cancelada         = Column(Boolean())
    datacancelada     = Column(DateTime())
    #pagar extras?

class MapaReservas(Base):
    __tablename__ = 'mapa_reservas'
    uuid         = Column(String(64)    , primary_key = True, default=suuid)
    
    apartamento  = Column(String(64))
    data         = Column(Date())
    
    
if __name__ == '__main__':
    print('done')
    
