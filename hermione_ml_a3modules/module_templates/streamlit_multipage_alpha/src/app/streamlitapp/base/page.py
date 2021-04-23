import streamlit as st
import copy
from datetime import datetime
import pickle
import os

from . import aux

class BasePage:
    def __init__(self, app):
        self.name = "my_new_page"
        self.title = "My Page"
        self.app = app
        self.opts = {}

    def start(self):
        self.set_defaults()
        self.inputs = copy.deepcopy(self.defaults)

    def set_defaults(self):

        self.defaults = {}

    def exit_func(self):
        self.defaults = copy.deepcopy(self.inputs)

    def reset_func(self):

        reset = st.button("Clear/Reload Defaults")
        self.inputs.setdefault("is_load", True)

        if reset:
            if self.inputs["is_load"]:
                self.start()
                self.inputs["is_load"] = False
            else:
                self.inputs["is_load"] = True
        else:
            self.inputs["is_load"] = True

        return not (self.inputs["is_load"])

    def __render__(self):

        if self.opts.get('reset_enabled', True) and self.reset_func():
            return

        self.render()

    def render(self):
        pass


class SaveLoad(BasePage):
    def __init__(self, app):
        self.name = "save_page"
        self.title = "Salvar/Carregar Análise"
        self.app = app
        self.opts = {'reset_enabled':False}

    def set_defaults(self):

        self.defaults = {
            "save_name": datetime.now().strftime("%d-%d-%Y_%H-%M"),
            "save_desc": datetime.now().strftime(
                "Análise realizada em %d/%d/%Y às %H:%M"
            ),
            "load_name": "",
        }

    def save_analysis(self):

        self.pre_save()

        save_data = self.app.get_config()

        pickle.dump(
            save_data,
            aux.open_file(
                os.path.join("saved_sessions", f"{self.inputs['save_name']}.pickle"),
                "wb",
            ),
        )
        with aux.open_file(
            os.path.join("saved_sessions", f"{self.inputs['save_name']}.txt"),
            "w",
        ) as text_file:
            text_file.write(self.inputs["save_desc"])

    def load_analysis(self):

        if self.inputs["load_name"] != "":
            obj = pickle.load(
                aux.open_file(
                    os.path.join(
                        "saved_sessions",
                        self.inputs["load_name"] + ".pickle",
                    ),
                    "rb",
                )
            )
            self.app.load_config(obj)

        else:
            st.warning("Selecione uma análise")

    def render(self):

        st.markdown("# Salvar Análise")
        self.inputs["save_name"] = st.text_input(
            "Nome da análise", value=self.defaults["save_name"]
        )
        self.inputs["save_desc"] = st.text_input(
            "Descrição da análise", value=self.defaults["save_desc"]
        )
        save_butt = st.button("Recalcular e Salvar")

        if save_butt:
            self.save_analysis()

        st.markdown("# Carregar Análise")
        response = aux.files_select_ag_grid()
        self.inputs["load_name"] = (
            response["selected_rows"][0]["Nome"]
            if len(response["selected_rows"]) > 0
            else ""
        )
        load_butt = st.button("Carregar")

        if load_butt:
            self.load_analysis()

    def pre_save(self):
        pass