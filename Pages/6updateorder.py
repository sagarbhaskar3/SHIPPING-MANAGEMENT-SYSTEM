import streamlit as st
import mysql.connector
import pandas as pd

if st.session_state.active == True:
    if st.session_state['username']!='admin':

        # Connect to your MySQL database
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="916996",
            database="cargo"
        )

        cursor = connection.cursor()

        # Streamlit UI
        st.title("Customer Orders (UPDATE CARGO NAME)")

        customer_id = st.session_state["username"]

        # Query the database to get the customer's orders based on the customer ID
        cursor.execute("SELECT * FROM Cargo WHERE customer_id = %s", (customer_id,))
        orders_data = cursor.fetchall()

        if orders_data:
            st.subheader(f"Viewing Orders for Customer ID: {customer_id}")

            # Display the customer's orders as a table
            df = pd.DataFrame(orders_data, columns=["Cargo ID", "Customer ID", "Cargo Name", "Ship ID", "Cargo Type", "Route ID", "Admin ID","Weight"])

            # Add a column for updating cargo names
            df['New Cargo Name'] = df.apply(lambda row: st.text_input(f"New Cargo Name for Cargo {row['Cargo ID']}", key=f"new_cargo_name_{row['Cargo ID']}"), axis=1)
            df['Update'] = df.apply(lambda row: st.button(f"Update Cargo Name {row['Cargo ID']}"), axis=1)

            # Check if any update button is pressed
            if any(df['Update']):
                for index, row in df.iterrows():
                    if row['Update']:
                        cargo_id_to_update = row['Cargo ID']
                        new_cargo_name = row['New Cargo Name']

                        # Update the cargo name
                        update_query = "UPDATE Cargo SET cargo_name = %s WHERE cargo_id = %s AND customer_id = %s"
                        cursor.execute(update_query, (new_cargo_name, cargo_id_to_update, customer_id))
                        connection.commit()

                        st.success(f"Cargo name for Cargo {cargo_id_to_update} updated successfully!")

            # Display the updated dataframe without the 'New Cargo Name' and 'Update' columns
            st.dataframe(df.drop(columns=['New Cargo Name', 'Update']))
        else:
            st.write("No orders found for this customer.")

        # Close the database connection
        cursor.close()
        connection.close()
    else:
        st.error("Admin can not access these functions.")
else:
    st.link_button('Go to Login', url="http://localhost:8501/2customerlogin")
