import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, date

if st.session_state.active == True:
    if st.session_state['username'] != 'admin':

        # Connect to your MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="916996",
            database="cargo"
        )

        cursor = connection.cursor()

        # Streamlit UI
        st.title("Customer Orders (READ CARGO)")

        customer_id = st.session_state["username"]

        # Query the database to get the customer's orders based on the customer ID
        cursor.execute("SELECT * FROM Cargo WHERE customer_id = %s", (customer_id,))
        orders_data = cursor.fetchall()

        if orders_data:
            st.subheader(f"Viewing Orders for Customer ID: {customer_id}")

            # Display the customer's orders as a table
            df = pd.DataFrame(orders_data, columns=["Cargo ID", "Customer ID", "Cargo Name", "Ship ID", "Cargo Type", "Route ID", "Admin ID", "Weight"])

            # Add a button column for deleting cargo orders
            df['Delete'] = df.apply(lambda row: st.button(f"Delete Cargo {row['Cargo ID']}"), axis=1)

            # Check if any delete button is pressed
            if any(df['Delete']):
                for index, row in df.iterrows():
                    if row['Delete']:
                        cargo_id_to_delete = row['Cargo ID']
                        weight_to_delete = row['Weight']

                        # Get the ship_id associated with the cargo
                        cursor.execute("SELECT ship_id FROM Cargo WHERE cargo_id = %s", (cargo_id_to_delete,))
                        ship_id = cursor.fetchone()[0]

                        # Get the departure_date of the ship
                        cursor.execute("SELECT departure_date FROM Ship WHERE ship_id = %s", (ship_id,))
                        departure_date = cursor.fetchone()[0]
                        current_datetime = datetime.combine(departure_date, datetime.min.time())  # Convert to datetime

                        if current_datetime > datetime.now():
                            # Update current storage of the ship by subtracting the weight of the cargo
                            cursor.execute("UPDATE Ship SET current_storage = current_storage - %s WHERE ship_id = %s", (weight_to_delete, ship_id))
                            connection.commit()

                            # Delete the cargo order
                            delete_query = "DELETE FROM Cargo WHERE cargo_id = %s"
                            cursor.execute(delete_query, (cargo_id_to_delete,))
                            connection.commit()

                            st.success(f"Cargo order {cargo_id_to_delete} deleted successfully!")
                        else:
                            st.error("The departure date of the selected ship has already passed. Cannot delete the order now.")

            # Display the updated dataframe without the 'Delete' column
            st.dataframe(df.drop(columns=['Delete']))
        else:
            st.write("No orders found for this customer.")

        # Close the database connection
        cursor.close()
        connection.close()
    else:
        st.error("Admin cannot access these functions.")
else:
    st.link_button('Go to Login', url="http://localhost:8501/2customerlogin")
