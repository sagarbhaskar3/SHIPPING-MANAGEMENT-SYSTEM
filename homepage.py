import streamlit as st

def main():
    st.title("Cargo Management System")

    st.write("Welcome to Cargo Management System")

    # Display options based on user type
    user_type = st.radio("Choose your role:", ("New Customer", "Existing Customer/Admin"))

    if user_type == "New Customer":
        st.write("If you are a new customer, please sign up")

        st.write("If you are a new admin, create a new admin account")
    

    elif user_type == "Existing Customer/Admin":
        st.write("If you are an existing customer or admin, please log in")
        
if __name__ == "__main__":
    main()
