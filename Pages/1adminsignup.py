import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
import yaml

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="916996",
    database="cargo"
)

try:
    with st.form(key="signup", clear_on_submit=True):
        st.title("New User Registration (CREATE ADMIN)")
        st.title("Please fill out all the details")
        admin_name = st.text_input("Admin Name")
        admin_id = st.selectbox("Admin ID", ["ADMIN"])  # Default value "ADMIN" in a dropdown menu
        password = st.text_input("Password")
        submit_button = st.form_submit_button(label="Register")

        if submit_button:
            # Add to the DB
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Admin(admin_id, admin_name, password) VALUES(%s, %s, %s)", (admin_id, admin_name, password))
            connection.commit()

            with open("config.yaml", "r") as f:
                try:
                    yaml_data = yaml.load(f, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:
                    st.error(f"Error loading YAML file: {exc}")
                    yaml_data = {}

            if 'credentials' not in yaml_data:
                yaml_data['credentials'] = {'usernames': {}}

            # Hash the password using stauth Hasher
            hashed_password = stauth.Hasher([password]).generate()

            new_user_credentials = {
                admin_id: {
                    'name': admin_name,
                    'password': hashed_password[0]  # Replace with the new admin's password
                }
            }

            # Add the new admin's credentials to the existing data
            yaml_data['credentials']['usernames'].update(new_user_credentials)

            with open("config.yaml", "w") as f:
                yaml.dump(yaml_data, f)

            st.write('Registration success, you can log in')
except Exception as e:
    st.error(e)
