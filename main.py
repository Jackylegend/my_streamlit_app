import streamlit as st
import streamlit_antd_components as sac
import gdp, bond, bond2, bond3,home



class MultiApp:
    st.set_page_config(layout='wide',initial_sidebar_state="expanded")
    def __init__(self):
        self.apps = []
    def add_app(self, tittle, function):
        self.apps.append({
            'tittle':tittle,
            'function': function
        })
    def run():
        with st.sidebar:
            app = sac.menu([sac.MenuItem('Home', icon='house-fill'),
                sac.MenuItem('Dataset', icon='box-fill', children=[
                    sac.MenuItem('GDP', icon='apple'),
                    sac.MenuItem('Bond Market', icon='git', children=[
                        sac.MenuItem('Yield Level', icon='google'),
                        sac.MenuItem('Term Structure Analysis', icon='gitlab'),
                        sac.MenuItem('Statistcal Analysis', icon='wechat'),
                        ]),
                        ]),
                        ], open_all=True)
        if app == 'Home':
            home.app()    
        if app == 'Yield Level':
            bond2.app()
        if app == 'Term Structure Analysis':
            bond3.app()    
        
    run()

    