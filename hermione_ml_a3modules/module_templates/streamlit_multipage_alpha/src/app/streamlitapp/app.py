from base import BaseApp
from base import BasePage,SaveLoad
from base import aux
import streamlit as st

class MyApp(BaseApp):
    
    def create_pages(self):
        self.pages = [
            IntroPage(self),
            SaveLoad(self),
        ]


class IntroPage(BasePage):

    def __init__(self, app):
        self.name = "home_page"
        self.title = "Home"
        self.app = app
        self.opts = {'reset_enabled':False}

    def load_dfs(self):

        dfs = {
            'titanic':aux.get_csv_as_df('data/train.csv')
        }

        self.dfs = dfs

    def render(self):
        st.markdown(aux.open_file("static/home.md").read())

def main():
    MyApp()

if __name__ == "__main__":
    main()
