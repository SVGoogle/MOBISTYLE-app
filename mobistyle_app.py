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

    # LOAD DATA
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
    @st.cache(show_spinner=False)
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

    with st.beta_expander("Building description"):
        st.write("Describe building type, location, HVAC system...")
        st.table(room_info)

    # SIDEBAR
    st.sidebar.header('Visualization Features')
    room_name = st.sidebar.selectbox('Select Room', room_names)

    #duration = st.sidebar.select_slider('Duration', options=['15 min', '1 month', '1 year'])

    about_project = st.sidebar.beta_expander('About project')
    about_project.write("""
    - Author: Sandijs Vasilevskis    
    - Project: MOBISTYLE, EU H2020 
    - Website: [LINK](https://www.mobistyle-project.eu)
    - Period: 2018-2020
    - Deliverable: D6.2
    """)

    # OUTDOOR CLIMATE
    with st.beta_expander('Outdoor climate'):
        # st.subheader('Outdoor climate')
        option_out = st.selectbox('', options=['Temperature', 'RH', 'Solar radiation', 'Degree-days'])
        if 'Degree-days' in option_out:
            st.pyplot(plot_hdd(hdd))
        elif 'Temperature' in option_out:
            st.pyplot(plot_t_out(outdoor_data, 'Temperature'))
        elif 'RH' in option_out:
            st.pyplot(plot_t_out(outdoor_data, 'RH'))
        elif 'Solar radiation' in option_out:
            st.pyplot(plot_t_out(outdoor_data, 'Global radiation'))
            st.pyplot(plot_t_out(outdoor_data, 'Diffuse radiation'))

    # ROOM VISUALIZATION
    st.header('IAQ parameters')
    with st.beta_expander(f'Description - {room_name}'):
        st.write("""         
        Dates for giving the MOBISTYLE mobile app to office employees, number of employees, office space area and type,
        window orientation are described in the table below. LED sensors are mounted on the wall. 
        They are signalizing red light when the air quality in the room gets bad, 
        namely carbon dioxide ($CO_2$) concentration levels exceed *1200 ppm*.
        """)
        st.table(room_info.loc[room_name, ])

    # Load DatFrame for selected room
    df = get_data()[room_dct[room_name]]
    df = df.rename(columns={'HEAT_COOL': 'Season'})

    #st.table(df.astype('object'))

    option_iaq = st.selectbox('', options=['Temperature', 'RH', 'CO2 levels', 'VOC levels'])
    if option_iaq == 'Temperature':
        st.pyplot(boxplot_monthly_temp(df, room_dct[room_name]))
    if option_iaq == 'RH':
        st.pyplot(boxplot_monthly_rh(df, room_dct[room_name]))
    if option_iaq == 'CO2 levels':
        st.pyplot(boxplot_monthly_co2(df, room_dct[room_name]))
        st.write('Comfort category IV+ corresponds to $CO_2$ concentration levels above *1200 ppm*.')
    if option_iaq == 'VOC levels':
        st.pyplot(boxplot_monthly_voc(df, room_dct[room_name]))
        st.write('Comfort category IV+ corresponds to *VOC* concentration levels above *100 ppb*.')

    st.subheader('Thermal Comfort categories')

    #st.pyplot(plot_comfort_cat_temp(df, room_dct[room_name]))

    g = sns.catplot(x='Category_TEMP', hue='Monitoring_Period', col='Season',
                    data=df, kind='count', order=labels_T_RH, legend=False, legend_out=True,
                    height=3.5, aspect=1.5)
    (g.set_axis_labels("Comfort category", "Count")
     .add_legend(loc='upper right', fontsize=14))
    st.pyplot(g)

    st.subheader('User behavior')
    option_user = st.selectbox('', options=['Window opening count', 'Room occupied time', 'Window open time'])

    if st.button('Correlation Heatmap'):
        pass


if __name__ == '__main__':
    main()