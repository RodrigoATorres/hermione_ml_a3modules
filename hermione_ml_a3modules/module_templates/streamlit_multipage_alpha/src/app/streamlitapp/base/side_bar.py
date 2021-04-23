import streamlit as st

class BaseSideBar:

    def __init__(self, app):
        self.app = app

    def render(self):
        st.sidebar.title('Hello! I am the side bar')