import streamlit as st
import streamlit_authenticator as stauth
import mysql.connector
from datetime import datetime, date
import pandas as pd
import pymysql  


if st.session_state.active == True:
    if st.session_state['username'] == 'admin':
        # Function to execute the stored procedure and retrieve customer information
        def get_customer_info():
            # Connect to the database
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='916996',
                database='cargo',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            try:
                with connection.cursor() as cursor:
                    # Execute the SQL query to get customer information
                    cursor.execute('SELECT customer_id, customer_name FROM Customer')
                    result = cursor.fetchall()
            finally:
                connection.close()

            return result

        # Function to get customer orders
        def get_customer_orders(customer_id):
            # Connect to the database
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='916996',
                database='cargo',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            try:
                with connection.cursor() as cursor:
                    # Execute the stored procedure to get customer orders
                    cursor.callproc('GetCustomerInfo', (customer_id,))
                    result = cursor.fetchall()
            finally:
                connection.close()

            return result

        # Function to get total weight of cargos for a customer
        def get_total_weight_for_customer(customer_id):
            # Connect to the database
            connection = pymysql.connect(
                host='127.0.0.1',
                user='root',
                password='916996',
                database='cargo',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            try:
                with connection.cursor() as cursor:
                    # Execute the SQL query to get total weight
                    cursor.execute('SELECT SUM(weight_in_tons) AS total_weight FROM Cargo WHERE customer_id = %s', (customer_id,))
                    result = cursor.fetchone()
            finally:
                connection.close()

            return result['total_weight'] if result and result['total_weight'] is not None else 0

        # Streamlit app
        def main():
            st.title("Customer Information with Orders")

            # Get customer information
            customer_data = get_customer_info()

            # Display the customer information as a DataFrame
            customer_df = pd.DataFrame(customer_data, columns=['customer_id', 'customer_name'])
            st.dataframe(customer_df)

            # Input for customer_id
            customer_id = st.text_input("Enter Customer ID:", "")

            # Button to execute the stored procedure
            if st.button("Get Customer Orders"):
                # Check if customer_id is provided
                if not customer_id:
                    st.warning("Please enter a Customer ID.")
                else:
                    # Call the function to get customer orders
                    orders_result = get_customer_orders(customer_id)

                    # Display the result as a DataFrame
                    if orders_result:
                        orders_df = pd.DataFrame(orders_result)
                        st.dataframe(orders_df)

                        # Display total weight for the customer
                        total_weight = get_total_weight_for_customer(customer_id)
                        st.write(f"Total Weight of Cargos for Customer {customer_id}: {total_weight} tons")
                    else:
                        st.warning("No orders found for the given Customer ID.")

        if __name__ == "__main__":
            main()
    else:
    
        st.error("Admin cannot access these functions.")
else:
    st.link_button('Go to Login', url="http://localhost:8501/2customerlogin")
