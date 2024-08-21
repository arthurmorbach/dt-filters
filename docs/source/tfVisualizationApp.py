import datetime
import time
import numpy as np
import math 

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import filters
from create_db import TF, TF_Points, Session, engine


def main():
    st.title("Transfer Function Analysis")

    with st.sidebar:
        st.header("Filter Selection")
        
        types_of_filters = ("4/4 BPF", "4/8 BPF", "4/8 BPF CC")
        st.session_state.filter_type = st.selectbox(
            label = "Select Filter", 
            options = types_of_filters)
        

        st.header("Filter Setup")

        # use the settings from the last reading, if no settings, use standard values
        if local_session.query(TF).all():
            st.session_state.tf_name = st.text_input(
                label = 'TF Name', 
                value = local_session.query(TF).filter(TF.id == local_session.query(TF).order_by(TF.id.desc()).first().id).first().tf_name)

            st.session_state.Cr = st.text_input(label='Rotation Capacitor (F)', value = local_session.query(TF).order_by(TF.id.desc()).first().Cr)
            st.session_state.Ch = st.text_input(label='History Capacitor (F)', value = local_session.query(TF).order_by(TF.id.desc()).first().Ch)
            st.session_state.beta = st.text_input(label='beta (Gain)', value = local_session.query(TF).order_by(TF.id.desc()).first().beta)
            st.session_state.fs = st.text_input(label='Samplig Frequency (Hz)', value = local_session.query(TF).order_by(TF.id.desc()).first().fs)
        else:
            st.session_state.tf_name = st.text_input(label = 'Battery Number', value = 1)

            st.session_state.filter_type = st.selectbox(
                label = "Select Filter", 
                options = types_of_filters)
            
            st.session_state.Cr = st.text_input(label='Start Frequency (Hz)', value = 75e-15)
            st.session_state.Ch = st.text_input(label='End Frequency (Hz)', value = 20e-12)
            st.session_state.beta = st.text_input(label='Maximum Current Amplitude (A)', value = -0.3)
            st.session_state.fs = st.text_input(label='Minimum Current Amplitude (A)', value = 9.6e9)

    
if __name__ == "__main__":
    st.set_page_config(
		page_title = "Transfer Function Test",
		layout = "wide"
	)

    local_session = Session(bind = engine)
    
    if "tf_name" not in st.session_state:
        st.session_state.tf_name = 0
    if "Cr" not in st.session_state:
        st.session_state.Cr = 0
    if "Ch" not in st.session_state:
        st.session_state.Ch = 0
    if "beta" not in st.session_state:
        st.session_state.beta = 0
    if "fs" not in st.session_state:
        st.session_state.fs = 0
        
    if "filter_type" not in st.session_state:
        st.session_state.filter_type = 0


    main()
