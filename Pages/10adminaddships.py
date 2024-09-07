import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector

if st.session_state.active == True:
    if st.session_state['username'] == 'admin':
        # Connect to your MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="916996",
            database="cargo"
        )

        cursor = connection.cursor()

        # Streamlit UI
        st.title("Add Ship to Ships Table (CREATE SHIP)")

        # Get ship details from the user
        ship_name = st.text_input("Enter Ship Name:")
        arrival_date = st.date_input("Enter Arrival Date:")
        departure_date = st.date_input("Enter Departure Date:")
        route_id = st.number_input("Enter Route ID:", min_value=1, step=1)
        max_payload = st.number_input("Enter Maximum Payload:", min_value=0, step=1)
        admin_id = st.text_input("Enter Admin ID:")
        '''Trigger is used here'''
        # Button to add the ship to the Ships table
        if st.button("Add Ship"):
            # Query to insert data into the Ships table
            insert_query = "INSERT INTO Ship (ship_name, arrival_date, departure_date, route_id, admin_id, max_storage) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (ship_name, arrival_date, departure_date, route_id, admin_id, max_payload)

            try:
                cursor.execute(insert_query, data)
                connection.commit()
                st.success("Ship added successfully!")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                cursor.close()
                connection.close()
    else:
        st.error('User is not admin')
else:
    st.error('User is not logged in')
