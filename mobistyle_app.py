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
    room_name = st.sidebar.selectbox('Select Room', ['Room %d' % i for i in range(1, 9)])

    st.sidebar.selectbox('Duration', ('15 minutes', 'Monthly', 'Yearly'))

    about_project = st.sidebar.beta_expander('About project')
    about_project.write("""
    - Author: Sandijs Vasilevskis    
    - Project: MOBISTYLE, EU H2020 
    - Website: [LINK](https://www.mobistyle-project.eu)
    - Period: 2018-2020
    - Deliverable: D6.2
    """)


    expander = st.beta_expander("Room description")
    expander.write("Here you could put in some really, really long explanations...")

    if st.button('Correlation Heatmap'):
        pass
    st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

    with st.beta_expander("See explanation"):
        st.write("""
    ...         The chart above shows some numbers I picked for you.
    ...         I rolled actual dice for these, so they're *guaranteed* to
    ...         be random.
    ...     """)
        st.image("https://static.streamlit.io/examples/dice.jpg")


if __name__ == '__main__':
    main()