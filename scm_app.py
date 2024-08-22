import streamlit as st
import pandas as pd
import prl_data_push as prl
# from PIL import Image
st.set_page_config(page_title='The cool Westwing SCM automation app', page_icon='./images/westwing_logo.jpeg')

def file_upload():
    prl_input_file = st.session_state["prl_input_file"]
    dataframe = pd.read_excel(prl_input_file)
    #st.write("filename:", prl_input_file.name)
    #st.write(dataframe)
    prl.po_placement(dataframe)
def run():
    st.title("The cool Westwing SCM automation app")
    # image = Image.open('./images/westwing_logo.jpeg')
      
    if st.button("PRL PO Placement", type="primary"):
        st.session_state.uploaded_file = st.file_uploader("Choose the PRL Input file", accept_multiple_files=False, key="prl_input_file", on_change=file_upload)
        # prl_input_file = st.file_uploader("Choose the PRL Input file", type=['xlsx'])
        
run()

