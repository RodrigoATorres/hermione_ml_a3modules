import streamlit as st
import os
from SessionState import get

from .side_bar import BaseSideBar
from .page import BasePage

class BaseApp:
    def __init__(self):

        session_state = get(
            app_config=False,
            login_info={'password':""},
            cur_page_idx=0,
        )
        
        self.login_info = session_state.login_info
        self.create_pages()
        self.create_side_bar()

        self.pages_dict = {page.name: page for page in self.pages}
        self.page_names = [page.name for page in self.pages]
        self.page_titles = [page.title for page in self.pages]

        self.cur_page = self.pages[session_state.cur_page_idx]
        self.cur_page_title = self.page_titles[session_state.cur_page_idx]
        self.cur_page_idx = session_state.cur_page_idx

        if session_state.app_config:
            self.load_config(session_state.app_config)
        else:
            self.start()

        self.render()
        session_state.app_config = self.get_config()
        session_state.login_info = self.login_info
        session_state.cur_page_idx = self.cur_page_idx

    def start(self):
        self.load_dfs()
        [page.start() for page in self.pages]

    def load_config(self, config):

        self.dfs = config["dfs"]
        for key in config["inputs"]:
            self.pages_dict[key].inputs = config["inputs"][key]
            if hasattr(self.pages_dict[key], "exit_func"):
                self.pages_dict[key].exit_func()
        for key in config["defaults"]:
            self.pages_dict[key].defaults = config["defaults"][key]

    def get_config(self):
        return {
            "dfs": self.dfs,
            "inputs": {page.name: page.inputs for page in self.pages},
            "defaults": {page.name: page.defaults for page in self.pages},
        }

    def config_styles(self):
        with open("/usr/src/app/static/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def render(self):

        self.config_styles()

        if self.authenticate():
            self.navigation_menu()
            self.cur_page.__render__()
            self.pre_render()
            self.side_bar.render()

    def authenticate(self):

        if os.environ["APP_ENV"] == "dev":
            return True

        password = self.login_info['password']

        if password == "teste123":
            return True
        else:
            pwd_placeholder = st.empty()
            pwd = pwd_placeholder.text_input("Password:", value="", type="password")
            password = pwd
            if password == "teste123":
                pwd_placeholder.empty()
                self.login_info['password'] = password
                return True
            else:
                if password != "":
                    st.error("the password you entered is incorrect")
                return False

    def navigation_menu(self):

        option = st.selectbox("", self.page_titles)

        if option != self.cur_page_title:
            if hasattr(self.cur_page, "exit_func"):
                self.cur_page.exit_func()

        self.cur_page_title = option
        self.cur_page_idx = self.page_titles.index(option)
        self.cur_page = self.pages[self.cur_page_idx]

    def create_side_bar(self):

        self.side_bar = BaseSideBar(self)

    def create_pages(self):

        self.pages = [BasePage(self)]

    def load_dfs(self):

        dfs = {}

        self.dfs = dfs

    def pre_render(self):
        pass
