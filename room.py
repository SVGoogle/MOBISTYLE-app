import streamlit as st
from statplots import *


def app():
    st.header('Indoor Air Quality Visualization App')
    st.write("""     
    This app explores Indoor Air Quality (IAQ) at several educational office rooms. 
    Main task of this visualization is to compare two monitoring periods - *BASELINE* and *MOBISTYLE*. 
    """)
    st.title('Room Selection')

    # LOAD DATA
    room_lst = ['R3N0808', 'R2N0805', 'K1N0623', 'K3N0605', 'R3N0644', 'K1N0624', 'K3N0618', 'R2N0634']
    room_names = ['Room %d' % i for i in range(1, 9)]
    room_dct = dict(zip(room_names, room_lst))

    room_info = pd.read_excel('./Data/room_info.xlsx', index_col='Room_ID', parse_dates=True).loc[room_lst, ]
    room_info = room_info.rename(index=dict(zip(room_lst, room_names))).replace({pd.np.nan: None})

    hdd = pd.read_excel('./Data/HDDs_SL.xlsx', index_col='Timestamp', parse_dates=True,
                        usecols=[0, 1, 2], nrows=25)
    outdoor_data = pd.read_csv('./Data/outdoor_data.csv', parse_dates=True, index_col='Timestamp')
    outdoor_data = outdoor_data.rename(columns={'RH': 'Outdoor RH', 'Temperature': 'Outdoor Temperature'})
    outdoor_data.loc[BL_start: BL_end, 'Monitoring_Period'] = 'BASELINE'
    outdoor_data.loc[MS_start: MS_end, 'Monitoring_Period'] = 'MOBISTYLE'
    categories = pd.read_excel('./Data/comfort_categories.xlsx', index_col='Category')

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
            usecols=list(
                [f'{room}_OCC', f'{room}_WINDOW', f'{room}_WINDOW_Openings', f'{room}_INAP_co2',
                 f'{room}_INAP_humidity', f'{room}_INAP_voc', f'{room}_TEMP', 'Monitoring_Period', 'HEAT_COOL',
                 'Category_TEMP', 'Category_RH', 'Category_CO2', 'Category_VOC', 'Timestamp'
                 ]),
            dtype=dtypes,
            parse_dates=True,
            index_col='Timestamp').rename(
            columns={'HEAT_COOL': 'Season',
                     f'{room}_OCC': 'Room Status',
                     f'{room}_WINDOW': 'Window State',
                     f'{room}_WINDOW_Openings': 'Window State Change',
                     f'{room}_INAP_co2': 'CO2',
                     f'{room}_INAP_humidity': 'RH',
                     f'{room}_INAP_voc': 'VOC',
                     f'{room}_TEMP': 'Temperature',
                     }) for room in room_lst}
        return data_dct

    room_name = st.selectbox('', room_names)

    # ROOM VISUALIZATION
    if st.checkbox('Room description'):
        st.write("""         
        Dates for giving the MOBISTYLE mobile app to office employees, number of employees, office space area and type,
        window orientation are described in the table below. LED sensors are mounted on the wall. 
        They are signalizing red light when the air quality in the room gets bad, 
        namely carbon dioxide ($CO_2$) concentration levels exceed *1200 ppm*.
        """)
        st.table(room_info.loc[room_name, ])

    st.header('IAQ parameters')

    # Load DataFrame for selected room
    data = get_data()[room_dct[room_name]]

    # Join on Index with outdoor data
    df = data.join(outdoor_data.iloc[:, :-1])
    # Daily data
    df_daily = (df.groupby(['Monitoring_Period', 'Season'])
                  .resample('D').mean().dropna(how='all').reset_index().set_index('Timestamp'))

    option_iaq = st.selectbox('', options=['Temperature', 'RH', 'CO2 levels', 'VOC levels'])
    if option_iaq == 'Temperature':
        st.pyplot(boxplot_monthly_temp(df, room_name))
    if option_iaq == 'RH':
        st.pyplot(boxplot_monthly_rh(df, room_name))
    if option_iaq == 'CO2 levels':
        st.pyplot(boxplot_monthly_co2(df, room_name))
        st.write('Comfort category IV+ corresponds to $CO_2$ concentration levels above *1200 ppm*.')
    if option_iaq == 'VOC levels':
        st.pyplot(boxplot_monthly_voc(df, room_name))
        st.write('Comfort category IV+ corresponds to *VOC* concentration levels above *100 ppb*.')

    st.subheader('Outdoor and indoor air temperature')

    def hexbin(x, y, color, **kwargs):
        """Function to plot Hexbin using FacetGrid."""
        cmap = sns.light_palette(color, as_cmap=True)
        plt.hexbin(x, y, gridsize=20, cmap=cmap, **kwargs)

    # Plot by Monitoring period
    with sns.axes_style("white"):
        g = sns.FacetGrid(df, hue='Monitoring_Period', col='Monitoring_Period', height=4)
        (g.map(hexbin, 'Temperature', 'Outdoor Temperature', extent=[15, 30, -5, 35])
         .set_axis_labels('Office Temperature ($^o$C)', 'Outdoor Temperature ($^o$C)'))
        st.pyplot(g)

    # Plot by Monitoring period and Season
    if st.checkbox('Seasonal comparison'):
        with sns.axes_style("white"):
            g = sns.FacetGrid(df, hue='Monitoring_Period', col='Monitoring_Period', row='Season', height=4)
            (g.map(hexbin, 'Temperature', 'Outdoor Temperature', extent=[15, 30, -5, 35])
             .set_axis_labels('Office Temperature ($^o$C)', 'Outdoor Temperature ($^o$C)'))
            st.pyplot(g)

    st.subheader('Thermal comfort categories')
    st.write("Indoor climate data is binned and categorized into comfort categories for a better visual representation "
             "according to European norm EN 15251:2007.")

    st.pyplot(plot_comfort_cat_temp_rh(df, room_name, 'Temperature'))
    st.pyplot(plot_comfort_cat_temp_rh(df, room_name, 'RH'))

    with st.beta_expander('Comfort category limits'):
        st.table(categories)
        st.write("""
        * CO2 concentration includes 400 ppm of an outdoor air concentration while estimating the category limits
        * DS/EN 15251 with sedentary activity level 1,2 [met]
        * VOC levels are categorized according to Table 1 in this source [LINK](https://iaqscience.lbl.gov/voc-intro)        
        """)

    g = sns.catplot(x='Category_TEMP', hue='Monitoring_Period', col='Season',
                    data=df, kind='count', order=labels_T_RH, legend=False, legend_out=True,
                    height=3.5, aspect=1.5)
    (g.set_axis_labels("Comfort category", "Count")
     .add_legend(loc='upper right', fontsize=14))
    # st.pyplot(g)

    st.subheader('Air quality categories')
    st.pyplot(plot_comfort_cat_co2_voc(df, room_name, 'CO2'))
    st.pyplot(plot_comfort_cat_co2_voc(df, room_name, 'VOC'))

    st.subheader('Open window detection')
    # option_user = st.selectbox('', options=['Window opening count', 'Room occupied time', 'Window open time'])
    st.pyplot(plot_monthly_window(df, room_name))
    st.pyplot(plot_window_temp_out(df_daily, room_name))

    st.subheader('Correlation Heatmap')
    # if st.button('Correlation Heatmap'):

    col1, col2 = st.beta_columns(2)
    with col1:
        st.pyplot(plot_corr_matrix(df_daily, room_name, 'BASELINE'))
    with col2:
        st.pyplot(plot_corr_matrix(df_daily, room_name, 'MOBISTYLE'))

    # OUTDOOR CLIMATE
    with st.beta_expander('Outdoor climate'):
        # st.subheader('Outdoor climate')
        option_out = st.selectbox('', options=['Temperature', 'RH', 'Solar radiation', 'Degree-days'])
        if 'Degree-days' in option_out:
            pass
            # st.pyplot(plot_hdd(hdd))
        elif 'Temperature' in option_out:
            st.pyplot(plot_t_out(outdoor_data, 'Outdoor Temperature'))
        elif 'RH' in option_out:
            st.pyplot(plot_t_out(outdoor_data, 'Outdoor RH'))
        elif 'Solar radiation' in option_out:
            st.pyplot(plot_t_out(outdoor_data, 'Global radiation'))
            st.pyplot(plot_t_out(outdoor_data, 'Diffuse radiation'))
