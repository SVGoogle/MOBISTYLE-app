import streamlit as st
import home
import room


def main():
    # NAVIGATION
    pages = {
        "Home": home,
        "Room Selection": room
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio('Go to', list(pages.keys()))
    page = pages[selection]

    # with st.spinner(f'Loading {selection} ...'):
    page.app()

    about_project = st.sidebar.beta_expander('About project')
    about_project.info("""      
    - Project: MOBISTYLE, EU H2020 
    - Website: [LINK](https://www.mobistyle-project.eu)
    - Period: 2018-2020
    - Deliverable: D6.2
    """)
    about_app = st.sidebar.beta_expander('About app')
    about_app.info("""
        - Author: Sandijs Vasilevskis
        - Date: December 2020      
        - GitHub repository: [LINK](https://github.com/SVGoogle/MOBISTYLE-app)              
        """)


if __name__ == '__main__':
    main()
