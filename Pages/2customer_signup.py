import streamlit as st
import mysql.connector
import yaml
import smtplib
import random
from email.mime.text import MIMEText
import streamlit_authenticator as stauth

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="916996",
    database="cargo"
)
# Initialize session state to store persistent values
if "random_pin" not in st.session_state:
    st.session_state.random_pin = None

try:
    with st.form(key="signup"):
        st.title("New User Registration (CREATE ACCOUNT)")
        st.title("Please fill out all the details")

        # User Input
        customer_id = st.text_input("customer_id")
        
        # Check if customer_id is 'admin' or 'ADMIN'
        if customer_id.lower() == 'admin':
            st.error("Invalid customer_id. Please choose a different one.")
            st.stop()

        customer_name = st.text_input("customer_name")
        email = st.text_input("Email")
        phone_number = st.text_input("Contact number")
        address = st.text_input("Address")
        admin_id = "ADMIN"
        password = st.text_input("Password", type="password")

        # Generate a 4-digit random pin before submit (if not generated yet)
        if st.session_state.random_pin is None:
            st.session_state.random_pin = str(random.randint(1000, 9999))

        # Submit Button to Trigger Email Verification
        submit_email_verification = st.form_submit_button(label="Send Verification Email")

        if submit_email_verification:
            # SMTP Configuration
            email_sender = 'anebanee1@gmail.com'
            email_password = 'qhea xdof eneq kxtl'
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

            # Sending Email
            try:
                body = f'Your OTP is {st.session_state.random_pin}'
                msg = MIMEText(body)
                msg['From'] = email_sender
                msg['To'] = email
                msg['Subject'] = 'Verification from SMMS'  # Set a fixed subject for verification email

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(email_sender, email_password)
                    server.sendmail(email_sender, email, msg.as_string())

                st.success('Email sent successfully! 🚀')

            except smtplib.SMTPException as e:
                st.error(f"Error sending email: {e}")
                st.stop()  # Stop execution if there's an error in sending the email

            # Email Verification Message
            st.info('Please check your email for the OTP.')

    # Separate form for OTP entry and registration
    with st.form(key="otp_registration"):
        user_input_otp = st.text_input("Enter OTP", type="password", key="otp_input")  # Use a unique key here
        submit_registration = st.form_submit_button(label="Register")

        if submit_registration and user_input_otp == st.session_state.random_pin:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO CUSTOMER(customer_id, customer_name, phone_number, address, password, admin_id) VALUES(%s, %s, %s, %s, %s, %s)", (customer_id, customer_name, phone_number, address, password, admin_id))
            connection.commit()

            with open("config.yaml", "r") as f:
                yaml_data = yaml.safe_load(f)
            hashed_password = stauth.Hasher([password]).generate()
            new_user_credentials = {
                customer_id: {
                    'name': customer_name,  # Replace with the actual account number
                    'phone number': phone_number,
                    'address': address,
                    'password': hashed_password[0]  # Replace with the new user's password
                }
            }

            yaml_data['credentials']['usernames'].update(new_user_credentials)

            with open("config.yaml", "w") as f:
                yaml.dump(yaml_data, f)

            st.write('Registration success, you can log in')
        elif submit_registration and user_input_otp != st.session_state.random_pin:
            st.error("Wrong OTP")

except mysql.connector.Error as e:
    st.error(f"Database error: {e}")
finally:
    if connection.is_connected():
        connection.close()
