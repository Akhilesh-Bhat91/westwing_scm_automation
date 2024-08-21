import streamlit as st
from PIL import Image
def run():
    st.title("Westwing SCM App: For all the cool automation stuff")
    image = Image.open('./images/westwing_logo.jpeg')

    col1, col2, col3 = st.columns([3, 5, 3])
    with col1:
        st.write("")
    with col2:
        st.image(image, use_column_width=False)
    with col3:
        st.write("")
        
    if st.button("PRL PO Placement", type="primary"):
        st.write("Trying to automate PRL PO placement")
        
run()

