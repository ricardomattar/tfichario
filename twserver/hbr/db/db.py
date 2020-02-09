# -*- coding: latin1 -*-

import sys
import hashlib

import logging
import logging.handlers
logger = logging.getLogger()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

try:
    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/hotel', pool_size=80, max_overflow=0)
    #engine = create_engine('sqlite:////home/ricardo/Dropbox/spyder/hotel/hbr/db/hotel_devel.db')
    base = models.Base
    
    
    session_maker = sessionmaker()
    session_maker.configure(bind=engine)
except:
    logger.exception('')
    sys.exit(1)

def create_metadata():
    models.Base.metadata.create_all(engine)

def create_admin(password):
    ad = models.Usuario()
    ad.nome='admin'
    ad.classe='admin'
    ad.password = hashlib.sha1(password).hexdigest()
    
    ip = models.Usuario()
    ip.nome='import'
    ip.classe='admin'
    ip.password = hashlib.sha1(password).hexdigest()
    
    
    session = session_maker()
    session.add(ad)
    session.add(ip)
    session.commit()
    
if __name__ == '__main__':
    if sys.argv[1] == 'createdb':
        create_metadata()
        sys.exit(0)
                
    if sys.argv[1] == 'createadmin':
        create_admin(sys.argv[2])
        
        