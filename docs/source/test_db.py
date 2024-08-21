from create_db import TF, TF_Points, Session, engine
from datetime import datetime

local_session = Session(bind = engine)

new = TF(tf_name = 'bpf441234', Cr = 15e-12, Ch = 10e-12, beta = 0, fs = 9.6e9, fc = 3e3, Zo = 4e3,
         time = datetime.utcnow())

local_session.add(new)
local_session.commit()
        
