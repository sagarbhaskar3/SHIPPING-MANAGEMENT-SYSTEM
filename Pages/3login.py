import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# LOGIN PHASE 
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# AFTER USER CREATION LOGIN PAGE
if "active" not in st.session_state:
    st.session_state.active = False

placeholder = st.empty()
authenticator.login('Login', 'main')
placeholder.link_button('Sign Up',help="New User? Click to create User",url="http://localhost:8501/3customer_signup")


if st.session_state["authentication_status"]:
        st.session_state.active = True
        placeholder.empty()
        authenticator.logout('Logout', 'sidebar', key='unique_key')
        st.write(f'Welcome  *{st.session_state["name"]}*')
        st.write(st.session_state['username'])
        
    
        
        
        
elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    
