import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from statplots import *


def main():
    st.title('Indoor Air Quality Visualization App')
    st.write("""     
    This app explores Indoor Air Quality (IAQ) at several educational office rooms.    
        """)

    room_lst = ['R3N0808', 'R2N0805', 'K1N0623', 'K3N0605', 'R3N0644', 'K1N0624', 'K3N0618', 'R2N0634']
    room_names = ['Room %d' % i for i in range(1, 9)]
    room_dct = dict(zip(room_names, room_lst))

    room_info = pd.read_excel('./Data/room_info.xlsx', index_col='Room_ID', parse_dates=True).loc[room_lst, ]
    room_info = room_info.rename(index=dict(zip(room_lst, room_names)))

    hdd = pd.read_excel('./Data/HDDs_SL.xlsx', index_col='Timestamp', parse_dates=True,
                        usecols=[0, 1, 2], nrows=25)
    outdoor_data = pd.read_csv('./Data/outdoor_data.csv', parse_dates=True, index_col='Timestamp')
    BL_start, BL_end = '2018-02-1', '2019-02-1'
    MS_start, MS_end = '2019-02-1', '2020-02-1'
    outdoor_data.loc[BL_start: BL_end, 'Monitoring_Period'] = 'BASELINE'
    outdoor_data.loc[MS_start: MS_end, 'Monitoring_Period'] = 'MOBISTYLE'

    # suppress_st_warning=True
    @st.cache()
    def get_data():
        dtypes = {
            'LED': 'category',
            'App': 'category',
            'Monitoring_Period': 'category',
            'HEAT_COOL': 'category',
            'Category_TEMP': 'category',
            'Category_RH': 'category',
            'Category_CO2': 'category',
            'Category_VOC': 'category'
        }
        data_dct = {room:  pd.read_csv(
            f'./Data/Data_{room}.csv',
            dtype=dtypes,
            parse_dates=True,
            index_col='Timestamp') for room in room_lst}
        return data_dct

    df = get_data()

    with st.beta_expander("Building description"):
        st.write("Describe building type, location, HVAC system...")
        st.write(room_info)

    # SIDEBAR
    st.sidebar.header('Visualization Features')
    room_name = st.sidebar.selectbox('Select Room', room_names)

    duration = st.sidebar.select_slider('Duration', options=['15 min', '1 month', '1 year'])

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
        st.write(room_info.loc[room_name, ])

    # OUTDOOR CLIMATE
    st.subheader('Outdoor climate')
    options_out = st.multiselect('Select',
                                  ['Temperature', 'RH', 'Solar radiation', 'Degree-days'],
                                  ['Temperature'])

    if 'Degree-days' in options_out:
        st.pyplot(plot_hdd(hdd))
    elif 'Temperature' in options_out:
        st.pyplot(plot_t_out(outdoor_data, 'Temperature'))
    elif 'RH' in options_out:
        st.pyplot(plot_t_out(outdoor_data, 'RH'))
    elif 'Solar radiation' in options_out:
        st.pyplot(plot_t_out(outdoor_data, 'Global radiation'))
        st.pyplot(plot_t_out(outdoor_data, 'Diffuse radiation'))

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