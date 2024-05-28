import streamlit as st
import streamlit_antd_components as sac
from datapage import gdp, home, bond, pmi, nmi


class multiapp:
    st.set_page_config(layout="wide")

    def __init__(self):
        self.apps = []
    def add_app(self,tittle,funciton):
        self.apps.append({
            'tittle': tittle,
            'function': function
        })

    def run():

        with st.sidebar:
            app = sac.menu([
                sac.MenuItem('Home', icon='house-fill'),
                sac.MenuItem('Dataset', icon='box-fill', children=[
                    sac.MenuItem('GDP', icon='apple'),
                    sac.MenuItem('Bond Market', icon='apple'),
                    sac.MenuItem('ISM PMI', icon='apple'),
                    sac.MenuItem('ISM NMI', icon='apple'),
                    ]),
                sac.MenuItem('About', icon='house-fill'),
                sac.MenuItem(type='divider'),
            ], index=0,variant='filled', open_all=True)
        
        if app == 'Home':
            home.app()
        if app == 'GDP':
            gdp.app()
        if app == 'Bond Market':
            bond.app()
        if app == 'ISM PMI':
            pmi.app()
        if app == 'ISM NMI':
            nmi.app()

    run()




