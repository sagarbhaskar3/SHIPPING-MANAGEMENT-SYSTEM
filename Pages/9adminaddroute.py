import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
import pandas as pd

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
        st.title("Add Route to Route Table (CREATE ROUTE)")

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

        # Select origin and destination ports
        selected_origin_port_name = st.selectbox("Select Origin Port:", origin_ports_df["Port Name"])
        selected_destination_port_name = st.selectbox("Select Destination Port:", destination_ports_df["Port Name"])

        # Get admin ID from the user
        admin_id = "ADMIN"

        # Check if origin port and destination port are the same
        if selected_origin_port_name == selected_destination_port_name:
            st.error("Origin Port and Destination Port cannot be the same.")
        else:
            # Check if a route already exists for the selected origin and destination ports
            route_exist_query = "SELECT route_id FROM Route WHERE origin_port_id = (SELECT origin_port_id FROM OriginPort WHERE port_id = (SELECT port_id FROM Port WHERE port_name = %s)) AND destination_port_id = (SELECT destination_port_id FROM DestinationPort WHERE port_id = (SELECT port_id FROM Port WHERE port_name = %s))"
            route_exist_data = (selected_origin_port_name, selected_destination_port_name)
            cursor.execute(route_exist_query, route_exist_data)
            existing_route = cursor.fetchone()

            if existing_route:
                st.error("A route already exists for the selected Origin Port and Destination Port.")
            else:
                # Button to add the route to the Routes table
                if st.button("Add Route"):
                    # Query to insert data into the Routes table
                    insert_query = "INSERT INTO Route (origin_port_id, destination_port_id, admin_id) VALUES ((SELECT origin_port_id FROM OriginPort WHERE port_id = (SELECT port_id FROM Port WHERE port_name = %s)), (SELECT destination_port_id FROM DestinationPort WHERE port_id = (SELECT port_id FROM Port WHERE port_name = %s)), %s)"
                    data = (selected_origin_port_name, selected_destination_port_name, admin_id)

                    try:
                        cursor.execute(insert_query, data)
                        connection.commit()
                        st.success("Route added successfully!")
                    except mysql.connector.Error as err:
                        st.error(f"Error: {err}")
                    finally:
                        cursor.close()
                        connection.close()
    else:
        st.error('User is not admin')
else:
    st.error('User is not logged in')
