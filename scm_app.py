import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from PIL import Image
st.set_page_config(page_title='The cool Westwing SCM automation app', page_icon='./images/westwing_logo.jpeg')

def file_upload():
    prl_input_file = st.session_state["prl_input_file"]
    dataframe = pd.read_excel(prl_input_file)
    st.write("filename:", prl_input_file.name)
    st.write(dataframe)
    # dataframe = pd.read_csv(prl_input_file)
    # st.write(dataframe)
def run():
    st.title("The cool Westwing SCM automation app")
    # image = Image.open('./images/westwing_logo.jpeg')

    # col1, col2, col3 = st.columns([3, 5, 3])
    # with col1:
    #     st.write("")
    # with col2:
    #     st.image(image, use_column_width=False)
    # with col3:
    #     st.write("")
        
    if st.button("PRL PO Placement", type="primary"):
        st.write("Trying to automate PRL PO placement")
        st.session_state.uploaded_file = st.file_uploader("Choose the PRL Input file", accept_multiple_files=False, key="prl_input_file", on_change=file_upload)
        # prl_input_file = st.file_uploader("Choose the PRL Input file", type=['xlsx'])
        
run()

