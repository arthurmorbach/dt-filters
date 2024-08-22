from datetime import datetime
import time
import numpy as np
import math 

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import filters
from create_db import TF, Session, engine


def main():
    st.title("Transfer Function Analysis")

    with st.sidebar:        
        types_of_filters = ("4/4 BPF", "4/8 BPF", "4/8 BPF CC")
        # st.session_state.filter_type = st.selectbox(
        #     label = "Select Filter", 
        #     options = types_of_filters)
        
        st.header("Filter Setup")

        # use the settings from the last reading, if no settings, use standard values
        if local_session.query(TF).all():
            st.session_state.filter_type = st.selectbox(
                label = "Select Filter", 
                options = types_of_filters)
            
            st.session_state.tf_name = st.text_input(
                label = 'TF Name', 
                value = local_session.query(TF).filter(TF.id == local_session.query(TF).order_by(TF.id.desc()).first().id).first().tf_name)

            st.session_state.Cr = st.text_input(label='Rotation Capacitor (F)', value = local_session.query(TF).order_by(TF.id.desc()).first().Cr)
            st.session_state.Ch = st.text_input(label='History Capacitor (F)', value = local_session.query(TF).order_by(TF.id.desc()).first().Ch)
            st.session_state.beta = st.text_input(label='beta (Gain)', value = local_session.query(TF).order_by(TF.id.desc()).first().beta)
            st.session_state.fs = st.text_input(label='Samplig Frequency (Hz)', value = local_session.query(TF).order_by(TF.id.desc()).first().fs)
        else:
            st.session_state.tf_name = st.text_input(label = 'TF Name', value = 'tttt') #f"TF {datetime.utcnow()}")

            st.session_state.filter_type = st.selectbox(
                label = "Select Filter", 
                options = types_of_filters)
            
            st.session_state.Cr = st.text_input(label='Start Frequency (Hz)', value = 75e-15)
            st.session_state.Ch = st.text_input(label='End Frequency (Hz)', value = 20e-12)
            st.session_state.beta = st.text_input(label='beta (Gain)', value = 0)
            st.session_state.fs = st.text_input(label='Sampling Frequency (Hz)', value = 9.6e9)
            
            

    if st.button("Generate"):
        Ch = float(st.session_state.Ch)
        Cr = float(st.session_state.Cr)
        fs = float(st.session_state.fs)
        
        if st.session_state.filter_type == '4/4 BPF':
            H, omega, st.session_state.Zo, st.session_state.fc = filters.BPF44(Ch, Cr, fs)

            frequencies = omega * fs / (2 * np.pi)
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=frequencies,
                y=20 * np.log10(np.abs(H)),
                mode='lines',
                name='Magnitude (dB)'
            ))
            
            fig.update_layout(
                title='Magnitude Response of the 4/4 BPF',
                xaxis_title='Frequency (Hz)',
                yaxis_title='Magnitude (dB)',
                template='plotly_dark'
            )
            
            st.session_state.fig = fig
            st.write(st.session_state.fig)
    else:
        if st.session_state.fig != 0:
            st.write(st.session_state.fig)  
            
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.button("Save Trasfer Function", on_click = save_transfer_function)
    
    
    
    
    
    # table with data selection
 #   transfer_functions = local_session.query(TF).all()
 #   number_of_tfs = len(local_session.query(TF).all())
 #   colu1, colu2, colu3, colu4, colu5 = st.columns(5)
    
    query = 'SELECT * FROM tf'
    
    df_1 = pd.read_sql(query, engine)
   
    # convert the Column type to datetime
    df_1['time'] = pd.to_datetime(df_1['time'])
    
    # organize the information that will be displayed
    # TF Name (df_1) | Cr (F) (df_1) | Ch (F) (df_1) | beta (df_1) | Fs (Hz) (df_1) | Fc (Hz) (df_1) | Zo (Ohms) (df_1) | datetime (df_1)

    df_1.rename(columns = {'id' : 'ID', 
                               'tf_name' : 'TF Name',
                               'Cr' : 'Cr (F)',
                               'Ch' : 'Ch (F)',
                               'beta' : 'beta',
                               'fs' : 'Fs (Hz)',
                               'fc' : 'Fc (Hz)', 
                               'Zo' : 'Zo (Ohms)', 
                               'time' : 'datetime'}, inplace = True)

    # drop unecessary columns for the user
   # df_1.drop(columns = ['columns to drop', 'columns to drop'], inplace = True)

    # add checkbox
    df_1.insert(0, 'Select', [False] * len(df_1))

    # convert "Select" column to boolean type
    df_1['Select'] = df_1['Select'].astype(bool)
    
    edited_df = st.data_editor(
            df_1,
            column_config={
                "Select": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select",
                    default=False,
                ),
                "ID" : None
            },
            disabled=["widgets"],
            hide_index=True,
            )

    st.session_state.selected_tf = edited_df[edited_df['Select'] == True]['ID'].tolist()
    
    print('SELECTED TF: ', st.session_state.selected_tf)
    
    
    
    

def save_transfer_function():
    TF_to_add= TF(tf_name = st.session_state.tf_name, 
                  Cr = str(st.session_state.Cr), 
                  Ch = str(st.session_state.Ch), 
                  beta = str(st.session_state.beta), 
                  fs = str(st.session_state.fs), 
                  fc = str(st.session_state.fc), 
                  Zo = str(st.session_state.Zo),
                  time = datetime.utcnow())

    local_session.add(TF_to_add)
    local_session.commit()
    
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    st.set_page_config(
		page_title = "Transfer Function Test",
		layout = "wide"
	)

    local_session = Session(bind = engine)
    
    if "tf_name" not in st.session_state:
        st.session_state.tf_name = 0
    if "Cr" not in st.session_state:
        st.session_state.Cr = 0.0
    if "Ch" not in st.session_state:
        st.session_state.Ch = 0.0
    if "beta" not in st.session_state:
        st.session_state.beta = 0
    if "fs" not in st.session_state:
        st.session_state.fs = 0
        
    if "filter_type" not in st.session_state:
        st.session_state.filter_type = 0
        
    if "Zo" not in st.session_state:
        st.session_state.Zo = 0
    if "fc" not in st.session_state:
        st.session_state.fc = 0
        
    if "fig" not in st.session_state:
        st.session_state.fig = 0
        
    if "selected_tf" not in st.session_state:
        st.session_state.selected_tf = 0

    main()
