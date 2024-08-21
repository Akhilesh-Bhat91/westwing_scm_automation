import streamlit as st

def run():
    category = ['--Select--', '1', '2', '3']
    cat_op = st.selectbox('Select your Category', category)
    if cat_op == category[0]:
        print('Please select something')
    else:
        print(cat_op)
        
run()
# st.write("Hello World!")
