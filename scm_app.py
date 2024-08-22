import streamlit as st
import pandas as pd
# from PIL import Image
st.set_page_config(page_title='The cool Westwing SCM automation app', page_icon='./images/westwing_logo.jpeg')
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
        prl_input_file = st.file_uploader("Choose the PRL Input file", type=['xlsx'])
        st.write("hello1")
        if prl_input_file is not None:
            st.write("hello")
            dataframe = pd.read_excel(prl_input_file)
            st.write("filename:", prl_input_file.name)
            st.write(dataframe)
            # dataframe = pd.read_csv(prl_input_file)
            # st.write(dataframe)
run()

