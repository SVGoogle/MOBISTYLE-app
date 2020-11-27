import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image


def main():
    st.title('Indoor Air Quality Visualization App')
    st.write("""     
    This app explores Indoor Air Quality (IAQ) at several educational office rooms.    
        """)
    with st.beta_expander("Building description"):
        st.write("Describe building type, location, HVAC system...")

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

    # ROOM VISUALIZATION
    st.header(f'{room_name}')
    with st.beta_expander('Description'):
        st.write(f"Number of employees, size, window orientation ...")

    st.subheader('IAQ parameters')
    options_iaq = st.multiselect('Select',
                                 ['Temperature', 'RH', 'CO2 levels', 'VOC levels'],
                                 ['Temperature'])
    for option in options_iaq:
        if option == 'Temperature':
            image = Image.open('./Results/Figures/boxplot_monthly_temp_R3N0808.png')
            st.image(image, use_column_width=True)

    st.subheader('Thermal Comfort categories')

    st.subheader('User behavior')
    options_user = st.multiselect('Select',
                                  ['Window opening count', 'Room occupied time', 'Window open time'],
                                  ['Window opening count'])

    st.subheader('Outdoor climate')
    options_out = st.multiselect('Select',
                                  ['Temperature', 'RH', 'Solar radiation'],
                                  ['Temperature'])

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