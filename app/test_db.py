from create_db import TF, Session, engine
from datetime import datetime

local_session = Session(bind = engine)

new = TF(tf_name = 'bpf48CC1234', filter_type = 'BPF44', Cr = '75e-12', Ch = '20e-12', beta = '0', fs = '6e6', fc = '3e3', Zo = '4e3',
         time = datetime.utcnow())

local_session.add(new)
local_session.commit()
        
