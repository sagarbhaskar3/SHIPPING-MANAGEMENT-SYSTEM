import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector 
import pandas as pd
if st.session_state.active == True:
    if st.session_state['username']=='admin':
    # Connect to your MySQL database
        connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="916996",
        database="cargo"
    )

        cursor = connection.cursor()

        # Streamlit UI
        st.title("Add Port to Ports Table (CREATE PORT)")

        # Get port details from the user
        port_name = st.text_input("Enter Port Name:")
        country = st.text_input("Enter Country:")
        phone_number = st.text_input("Enter Phone Number:")
        address = st.text_input("Enter Address:")
        admin_id = st.text_input("Enter Admin ID:")

        # Button to add the port to the Ports table
        if st.button("Add Port"):
            # Query to insert data into the Ports table
            insert_query = "INSERT INTO Port (port_name, country, phone_number, address, admin_id) VALUES (%s, %s, %s, %s, %s)"
            data = (port_name, country, phone_number, address, admin_id)

            try:
                cursor.execute(insert_query, data)
                connection.commit()
                st.success("Port added successfully!")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                cursor.close()
                connection.close()
    else:
        st.error('User is not admin')
else:
    st.error('User is not logged in')
            


