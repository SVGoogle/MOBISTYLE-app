import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    st.title('Indoor Air Quality Visualization App')
    st.write("""     
    This app explores Indoor Air Quality (IAQ) at several educational office rooms.    
        """)

    # Sidebar layout
    st.sidebar.header('Visualization Features')
    room_name = st.sidebar.selectbox('Select Room', ('1', '2', '3', '4', '5', '6', '7', '8'))

    st.sidebar.subheader('About project')
    st.sidebar.write("""
    - Author: Sandijs Vasilevskis    
    - Project: MOBISTYLE, EU H2020 
    - Period: 2018-2020
    - Deliverable: D6.2
    - Project website: [LINK](https://www.mobistyle-project.eu)
    """)

    if st.button('Correlation Heatmap'):
        pass


if __name__ == '__main__':
    main()