from datetime import datetime
import numpy as np
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
        
        st.session_state.standalone_or_bank = st.selectbox(
            label='Standalone or Cap Bank',
            options=['Standalone', 'Cap Bank'])
        if st.session_state.standalone_or_bank == 'Standalone':
            # use the settings from the last reading, if no settings, use standard values
            if local_session.query(TF).all():
                filter_type = st.selectbox(
                    label = "Select Filter", 
                    options = types_of_filters)
                if filter_type == types_of_filters[0]: st.session_state.filter_type = 'BPF44'
                elif filter_type == types_of_filters[1]: st.session_state.filter_type = 'BPF48'
                elif filter_type == types_of_filters[2]: st.session_state.filter_type = 'BPF48CC'
                
                st.session_state.tf_name = st.text_input(
                    label = 'TF Name', 
                    value = local_session.query(TF).filter(TF.id == local_session.query(TF).order_by(TF.id.desc()).first().id).first().tf_name)

                st.session_state.Cr = st.text_input(label='Rotation Capacitor (F)', value = local_session.query(TF).order_by(TF.id.desc()).first().Cr)
                st.session_state.Ch = st.text_input(label='History Capacitor (F)', value = local_session.query(TF).order_by(TF.id.desc()).first().Ch)
                st.session_state.beta = st.text_input(label='beta (Gain)', value = local_session.query(TF).order_by(TF.id.desc()).first().beta)
                st.session_state.fs = st.text_input(label='Samplig Frequency (Hz)', value = local_session.query(TF).order_by(TF.id.desc()).first().fs)
                st.session_state.f_mask_start = st.text_input(label='Start Frequency (Hz)', value = -50e6)
                st.session_state.f_mask_end = st.text_input(label='End Frequency (Hz)', value = 50e6)
            else:
                st.session_state.tf_name = st.text_input(label = 'TF Name', value = 'tttt') #f"TF {datetime.utcnow()}")

                filter_type = st.selectbox(
                    label = "Select Filter", 
                    options = types_of_filters)
                if filter_type == types_of_filters[0]: st.session_state.filter_type = 'BPF44'
                elif filter_type == types_of_filters[1]: st.session_state.filter_type = 'BPF48'
                elif filter_type == types_of_filters[2]: st.session_state.filter_type = 'BPF48CC'
                
                st.session_state.Cr = st.text_input(label='Rotation Capacitor (F)', value = 75e-15)
                st.session_state.Ch = st.text_input(label='History Capacitor (F)', value = 20e-12)
                st.session_state.beta = st.text_input(label='beta (Gain)', value = 0)
                st.session_state.fs = st.text_input(label='Sampling Frequency (Hz)', value = 9.6e9)
                
                st.session_state.f_mask_start = st.text_input(label='Start Frequency (Hz)', value = -50e6)
                st.session_state.f_mask_end = st.text_input(label='End Frequency (Hz)', value = 50e6)
            
        elif st.session_state.standalone_or_bank == 'Cap Bank':
            filter_type = st.selectbox(
                    label = "Select Filter", 
                    options = types_of_filters)
            if filter_type == types_of_filters[0]: st.session_state.filter_type = 'BPF44'
            elif filter_type == types_of_filters[1]: st.session_state.filter_type = 'BPF48'
            elif filter_type == types_of_filters[2]: st.session_state.filter_type = 'BPF48CC'
            
            st.session_state.tf_name = st.text_input(label = 'Cap Bank Name', value = 'CapBank0')
            
            st.session_state.Cr_cb_unity = st.text_input(label='Rotation Capacitor Bank Unity (F)', value = 10.9e-15)
            st.session_state.Cr_cb_bits = st.text_input(label='Rotation Capacitor Bank Bits', value = 5)
            st.session_state.Ch_cb_unity = st.text_input(label='History Capacitor Bank Unity (F)', value = 72.7e-15)
            st.session_state.Ch_cb_bits = st.text_input(label='History Capacitor Bank Bits', value = 5)
            st.session_state.beta = st.text_input(label='beta (Gain)', value = 0)
            st.session_state.fs = st.text_input(label='Sampling Frequency (Hz)', value = 600e6)
            
            st.session_state.f_mask_start = st.text_input(label='Start Frequency (Hz)', value = -50e6)
            st.session_state.f_mask_end = st.text_input(label='End Frequency (Hz)', value = 50e6)
            
            st.session_state.n_plots = st.text_input(label='Number of Plots (4, 9, 16, 25)', value = 9)

            
    if st.button("Generate"):
        if st.session_state.standalone_or_bank == 'Standalone':
            Ch = float(st.session_state.Ch)
            Cr = float(st.session_state.Cr)
            fs = float(st.session_state.fs)
            beta = float(st.session_state.beta)
            
            H, omega, st.session_state.Zo, st.session_state.fc = filters.DFTF(st.session_state.filter_type, Ch, Cr, fs, beta)

            frequencies = omega * fs / (2 * np.pi)
            
            # Apply the frequency range filter
            mask = (frequencies >= float(st.session_state.f_mask_start)) & (frequencies <= float(st.session_state.f_mask_end))

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=frequencies[mask],
                y=20 * np.log10(np.abs(H[mask])),
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
            
        elif st.session_state.standalone_or_bank == 'Cap Bank':
            # Variables
            Ch_array = filters.cap_bank(bits=int(st.session_state.Ch_cb_bits), unity_cap=float(st.session_state.Ch_cb_unity))
            Cr_array = filters.cap_bank(bits=int(st.session_state.Cr_cb_bits), unity_cap=float(st.session_state.Cr_cb_unity))
            fs = float(st.session_state.fs)
            beta = float(st.session_state.beta)

            # Select the desired capacitance values
            st.session_state.Ch_array = np.linspace(min(Ch_array), max(Ch_array), int(np.sqrt(float(st.session_state.n_plots))))
            st.session_state.Cr_array = np.linspace(min(Cr_array), max(Cr_array), int(np.sqrt(float(st.session_state.n_plots))))

            # Initialize 2D arrays for the selected values
            H = np.zeros((len(st.session_state.Ch_array), len(st.session_state.Cr_array)), dtype=object)
            st.session_state.Zo_array = np.zeros((len(st.session_state.Ch_array), len(st.session_state.Cr_array)))
            st.session_state.fc_array = np.zeros((len(st.session_state.Ch_array), len(st.session_state.Cr_array)))
            
            for j in range(len(st.session_state.Ch_array)):
                for i in range(len(st.session_state.Cr_array)):
                    H[j][i], omega, st.session_state.Zo_array[j][i], st.session_state.fc_array[j][i] = filters.DFTF(st.session_state.filter_type, st.session_state.Ch_array[j], st.session_state.Cr_array[i], fs, beta)
                    
                    
            
            frequencies = omega * fs / (2 * np.pi)
            
            # Apply the frequency range filter
            mask = (frequencies >= float(st.session_state.f_mask_start)) & (frequencies <= float(st.session_state.f_mask_end))

            fig = go.Figure()
            for j in range(len(st.session_state.Ch_array)):
                for i in range(len(st.session_state.Cr_array)):
                    fig.add_trace(go.Scatter(
                        x=frequencies[mask],
                        y=20 * np.log10(np.abs(H[j][i][mask])),
                        mode='lines',
                        name=f'Ch={round(st.session_state.Ch_array[j]*1e15, 2)} fF, Cr={round(st.session_state.Cr_array[i]*1e15, 2)} fF, Zo={st.session_state.Zo_array[j][i]}, Fc={round(st.session_state.fc_array[j][i]*1e-6, 2)} MHz'

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
    with col2:
        st.button("Delete from DB", on_click = delete_from_db)
    with col3:
        st.button("Plot Selected TFs", on_click = plot_selected)

    # table with data selection
    query = 'SELECT * FROM tf'
    
    df_1 = pd.read_sql(query, engine)
   
    # convert the Column type to datetime
    df_1['time'] = pd.to_datetime(df_1['time'])
    
    # organize the information that will be displayed
    # TF Name (df_1) | Cr (F) (df_1) | Ch (F) (df_1) | beta (df_1) | Fs (Hz) (df_1) | Fc (Hz) (df_1) | Zo (Ohms) (df_1) | datetime (df_1)

    df_1.rename(columns = {'id' : 'ID', 
                        'tf_name' : 'TF Name',
                        'filter_type' : 'Filter Type',
                        'Cr' : 'Cr (F)',
                        'Ch' : 'Ch (F)',
                        'beta' : 'beta',
                        'fs' : 'Fs (Hz)',
                        'fc' : 'Fc (Hz)', 
                        'Zo' : 'Zo (Ohms)',
                        'time' : 'datetime'}, inplace = True)

    # drop unecessary columns for the user
    df_1.drop(columns = ['cap_bank'], inplace = True)

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
    if st.session_state.standalone_or_bank == 'Standalone':
        TF_to_add= TF(tf_name = st.session_state.tf_name, 
                    filter_type = st.session_state.filter_type,
                    Cr = str(st.session_state.Cr), 
                    Ch = str(st.session_state.Ch), 
                    beta = str(st.session_state.beta), 
                    fs = str(st.session_state.fs), 
                    fc = str(st.session_state.fc), 
                    Zo = str(st.session_state.Zo),
                    cap_bank = False,
                    time = datetime.utcnow())

        local_session.add(TF_to_add)
        local_session.commit()
    elif st.session_state.standalone_or_bank == 'Cap Bank':
        for j in range(len(st.session_state.Ch_array)):
            for i in range(len(st.session_state.Cr_array)):
                TF_to_add= TF(
                    tf_name = st.session_state.tf_name, 
                    filter_type = st.session_state.filter_type,
                    Cr = str(st.session_state.Cr_array[i]), 
                    Ch = str(st.session_state.Ch_array[j]), 
                    beta = str(st.session_state.beta), 
                    fs = str(st.session_state.fs), 
                    fc = str(st.session_state.fc_array[j][i]), 
                    Zo = str(st.session_state.Zo_array[j][i]),
                    cap_bank = True,
                    time = datetime.utcnow())
            local_session.add(TF_to_add)
        local_session.commit()
            
    
    
def delete_from_db():
    if len(st.session_state.selected_tf):
        local_session.query(TF).filter(TF.id.in_(st.session_state.selected_tf)).delete()
        local_session.commit()

        local_session.close()
    else:
        pass
    
    
def plot_selected():
    selected_tfs = st.session_state.selected_tf
    
    if not selected_tfs:
        st.warning("No transfer functions selected.")
        return

    fig = go.Figure()

    for tf_id in selected_tfs:
        # Retrieve the transfer function parameters from the database
        tf = local_session.query(TF).filter(TF.id == tf_id).first()

        if tf:
            Ch = float(tf.Ch)
            Cr = float(tf.Cr)
            fs = float(tf.fs)
            beta = float(tf.beta)
            
            # Calculate the transfer function
            H, omega, Zo, fc = filters.DFTF(tf.filter_type, Ch, Cr, fs, beta)

            frequencies = omega * fs / (2 * np.pi)
            
            # Apply the frequency range filter
            mask = (frequencies >= float(st.session_state.f_mask_start)) & (frequencies <= float(st.session_state.f_mask_end))

            # Add the transfer function to the plot
            fig.add_trace(go.Scatter(
                x=frequencies[mask],
                y=20 * np.log10(np.abs(H[mask])),
                mode='lines',
                name=tf.tf_name
            ))
    
    # Update the layout of the plot
    fig.update_layout(
        title='Selected Transfer Functions',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Magnitude (dB)',
        template='plotly_dark'
    )
    
    # Save and display the plot
    st.session_state.fig = fig

    
    
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
        
    if "Cr_cb_unity" not in st.session_state:
        st.session_state.Cr_cb_unity = 0
    if "Cr_cb_bits" not in st.session_state:
        st.session_state.Cr_cb_bits = 0
    if "Ch_cb_unity" not in st.session_state:
        st.session_state.Ch_cb_unity = 0
    if "Ch_cb_bits" not in st.session_state:
        st.session_state.Ch_cb_bits = 0
    if "Ch_array" not in st.session_state:
        st.session_state.Ch_array = 0
    if "Cr_array" not in st.session_state:
        st.session_state.Cr_array = 0
    if "Zo_array" not in st.session_state:
        st.session_state.Zo_array = 0
    if "fc_array" not in st.session_state:
        st.session_state.fc_array = 0
        
    if "standalone_or_bank" not in st.session_state:
        st.session_state.standalone_or_bank = 'Standalone'
        
    if "fs" not in st.session_state:
        st.session_state.fs = 0
    if "f_mask_start" not in st.session_state:
        st.session_state.f_mask_start = 0
    if "f_mask_end" not in st.session_state:
        st.session_state.f_mask_end = 0
        
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
    
    if "n_plots" not in st.session_state:
        st.session_state.n_plots = 0
    
    
    main()
