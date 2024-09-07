import streamlit as st
import streamlit_authenticator as stauth
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
        st.title("Customer Orders (READ CARGO)")

        customer_id = st.session_state["username"]

        # Query the database to get the customer's orders based on the customer ID
        cursor.execute("SELECT * FROM Cargo WHERE customer_id = %s", (customer_id,))
        orders_data = cursor.fetchall()

        if orders_data:
            st.subheader(f"Viewing Orders for Customer ID: {customer_id}")

            # Display the customer's orders as a table
            df = pd.DataFrame(orders_data, columns=["Cargo ID", "Customer ID", "Cargo Name", "Ship ID", "Cargo Type", "Route ID","adminid","Weight"])
            st.dataframe(df)
        else:
            st.write("No orders found for this customer.")
        # Close the database connection
        cursor.close()
        connection.close()
    else:
        st.error("Admin can not access these functions.")
else:
    st.link_button('Go to Login', url="http://localhost:8501/2customerlogin")