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
        st.title("Manage Origin and Destination Ports (CREATE ORIGIN AND DESTINATION PORT)")

        # Display available ports in a dropdown menu
        port_query = "SELECT port_id, port_name FROM Port"
        cursor.execute(port_query)
        ports_data = cursor.fetchall()
        ports_dict = {port[1]: port[0] for port in ports_data}
        selected_port_name = st.selectbox("Select a Port:", list(ports_dict.keys()))

        # Get the selected port ID
        selected_port_id = ports_dict[selected_port_name]
        admin_id = "ADMIN"

        # Choose whether to add the port to OriginPort or DestinationPort
        destination_or_origin = st.radio("Select Destination or Origin Port:", ["Destination Port", "Origin Port"])

        # Button to add the selected port to the chosen table
        if st.button("Add to Table"):
            try:
                if destination_or_origin == "Destination Port":
                    cursor.execute("INSERT INTO DestinationPort (port_id,admin_id) VALUES (%s,%s)", (selected_port_id,admin_id))
                else:
                    cursor.execute("INSERT INTO OriginPort (port_id,admin_id) VALUES (%s,%s)", (selected_port_id,admin_id))
                connection.commit()
                st.success(f"{selected_port_name} added to {destination_or_origin} successfully!")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                cursor.close()
                connection.close()
    else:
        st.error('User is not admin')
else:
    st.error('User is not logged in')
            
