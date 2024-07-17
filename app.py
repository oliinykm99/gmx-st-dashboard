import streamlit as st


def home():
    st.set_page_config(page_title="GMX V1 - Dashboard",
                        page_icon="data/gmx_logo.png",
                        layout="wide",
                        initial_sidebar_state='collapsed')

    st.title('GMX V1 - Dashboard')