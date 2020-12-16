import streamlit as st
from PIL import Image


def app():
    st.header('Indoor Air Quality Visualization App')
    st.write("""     
    This app explores Indoor Air Quality (IAQ) at several educational office rooms. 
    Main task of this visualization is to compare two monitoring periods - *BASELINE* and *MOBISTYLE*. 
    """)
    st.title('Project Description')

    image = Image.open('./Results/Figures/monitoring_periods.png')

    st.image(image, caption='Monitoring Periods', use_column_width=True)

    st.write("""
    It is interesting to explore if the IAQ quality has improved during the second monitoring year, 
    because during this period office employees were given a specially develop mobile app that reported bad IAQ 
    and urged app users to open their windows. Furthermore, there were special sensors with LED lights -
     that signalize high carbon dioxide levels in their rooms - installed on the walls.
    """)

    with st.beta_expander("More information", expanded=True):
        st.write("In this video office employee describes her project experience with MOBISTYLE mobile app "
                 "and LED sensors.")
        embed_youtube = """
        <iframe width="560" height="315" src="https://www.youtube.com/embed/jwieVTpdKFY" frameborder="0" 
        allow="accelerometer; &cc_load_policy=1 autoplay; clipboard-write; encrypted-media; gyroscope; 
        picture-in-picture" allowfullscreen></iframe>
        """
        st.markdown(embed_youtube, unsafe_allow_html=True)
