import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
from datetime import datetime, date
import pandas as pd

if st.session_state.active == True:
    if st.session_state['username'] != 'admin':
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="916996",
            database="cargo"
        )
        cursor = connection.cursor()
        customer_id = st.session_state["username"]
        st.title("Place an Order (CREATE CARGO)")

        # Display available origin ports in a dropdown menu
        origin_port_query = "SELECT o.origin_port_id, p.port_id, p.port_name, p.country FROM OriginPort o JOIN Port p ON o.port_id = p.port_id"
        cursor.execute(origin_port_query)
        origin_ports_data = cursor.fetchall()
        origin_ports_df = pd.DataFrame(origin_ports_data, columns=["Origin Port ID", "Port ID", "Port Name", "Country"])
        st.subheader("Origin Ports")
        st.dataframe(origin_ports_df)

        # Display available destination ports in a dropdown menu
        destination_port_query = "SELECT d.destination_port_id, p.port_id, p.port_name, p.country FROM DestinationPort d JOIN Port p ON d.port_id = p.port_id"
        cursor.execute(destination_port_query)
        destination_ports_data = cursor.fetchall()
        destination_ports_df = pd.DataFrame(destination_ports_data, columns=["Destination Port ID", "Port ID", "Port Name", "Country"])
        st.subheader("Destination Ports")
        st.dataframe(destination_ports_df)

        # Create a form for the user to input the origin and destination
        origin_port = st.text_input("Enter OriginPortID")
        destination_port = st.text_input("Enter DestinationPortID")
        admin_id = 'ADMIN'
        if origin_port and destination_port:
            # Query the database to get ship details for the selected origin and destination
            cursor.execute(
                "SELECT * FROM Ship WHERE route_id IN (SELECT route_id FROM Route WHERE origin_port_id = %s AND destination_port_id = %s)",
                (origin_port, destination_port))
            ships = cursor.fetchall()

            if ships:
                st.write("Available Ships for the selected route:")
                # Create a list to store ship_ids that match the route
                ship_ids = [ship[0] for ship in ships]
                for ship in ships:
                    st.write(f"Ship ID: {ship[0]}")
                    st.write(f"Ship Name: {ship[1]}")
                    st.write(f"Arrival Date: {ship[2]}")
                    st.write(f"Departure Date: {ship[3]}")
                    st.write(f"Route ID: {ship[4]}")
                    st.write(f"Admin ID: {ship[5]}")
                    st.write(f"Max Storage: {ship[6]}")
                    st.write(f"Current Storage: {ship[7]}")
                    st.write("----------")

                # Create a drop-down menu for the user to select a ship_id
                selected_ship_id = st.selectbox("Select a Ship ID", ship_ids)

                if selected_ship_id:
                    st.write("You selected Ship ID:", selected_ship_id)

                    # Query the selected ship details
                    cursor.execute("SELECT * FROM Ship WHERE ship_id = %s", (selected_ship_id,))
                    selected_ship = cursor.fetchone()

                    # Check if departure date is in the future
                    departure_date = selected_ship[3]
                    current_datetime = datetime.combine(departure_date, datetime.min.time())  # Convert to datetime

                    if current_datetime > datetime.now():
                        # Additional cargo details form
                        st.subheader("Cargo Details")
                        cargo_name = st.text_input("Cargo Name")
                        cargo_type = st.text_input("Cargo Type")
                        cargo_weight = st.number_input("Cargo Weight (in tons)", min_value=1, step=1)

                        # Check if adding the cargo will exceed max_storage
                        if (selected_ship[7] + cargo_weight) > selected_ship[6]:
                            st.error("Adding this cargo will exceed the maximum storage capacity of the selected ship.")
                        else:
                            if st.button("Place Order"):
                                # Update the local current_storage for display
                                updated_current_storage = selected_ship[7] + cargo_weight
                                st.success(
                                    f"Order placed successfully! Updated Current Storage: {updated_current_storage} tons")

                                # Update the current_storage in the Ship table
                                cursor.execute(
                                    "UPDATE Ship SET current_storage = current_storage + %s WHERE ship_id = %s",
                                    (cargo_weight, selected_ship_id))
                                connection.commit()

                                # Insert the cargo record into the database
                                cursor.execute(
                                    "INSERT INTO Cargo (customer_id, cargo_name, ship_id, cargo_type, route_id, admin_id, weight_in_tons) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                    (customer_id, cargo_name, selected_ship_id, cargo_type, selected_ship[4], admin_id,
                                     cargo_weight))
                                connection.commit()
                    else:
                        st.error("The departure date of the selected ship has already passed. Cannot place an order.")

                else:
                    st.write("Please select a Ship ID from the dropdown.")
            else:
                st.write("No ships found for the selected route.")
        else:
            st.write("Please enter both Origin Port and Destination Port.")
    else:
        st.error("Admin cannot access these functions.")
else:
    st.link_button('Go to Login', url="http://localhost:8501/2customerlogin")
