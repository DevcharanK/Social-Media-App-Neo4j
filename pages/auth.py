import streamlit as st
import datetime
from database import create_user, authenticate_user

def signup_page():
    st.title("Social Media App")
    st.subheader("Sign Up")

    # Input fields
    email = st.text_input("Email")
    #sername = st.text_input("Username")  # Added username field for better user identification
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    date_of_birth = st.date_input("Date of Birth",min_value=datetime.date(1900, 1, 1),max_value=datetime.date.today())

    # Ensure user is at least 18 years old
    if date_of_birth:
        age = (datetime.date.today() - date_of_birth).days // 365
    else:
        age = 0

    if st.button("Create Account"):
        if not email or not password or not date_of_birth or not name:
            st.error("Please fill all fields.")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters long.")
        #Check if email has @ character
        elif "@" not in email:
            st.error("Invalid email address.")
        elif age < 18:
            st.error("You must be at least 18 years old to sign up.")
        else:
            # Create user in the database
            success,message  = create_user(email,name, password, date_of_birth.strftime("%Y-%m-%d"))
            if success:
                st.success("Account created successfully! Redirecting...")
                st.session_state["email"] = email  # Store logged-in user
                st.session_state["auth_mode"] = "login"  # Switch to login mode
                st.session_state["current_page"] = "Profile"  # Navigate to Profile page
                st.rerun()
            else:
                st.error(message)

def login_page():
    st.title("Social Media App")
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        if email and password:
            if authenticate_user(email, password):
                st.session_state["email"] = email  # Store email in session state
                st.session_state["current_page"] = "Home"
                st.success(f"Login successful! Logged in as {email}")  # Debugging
                print(st.session_state) #debugging
                st.rerun()
                
            else:
                st.error("Incorrect email or password.")
        else:
            st.error("Please enter both email and password.")


# **Run function to display the appropriate auth page**
def run():
    st.session_state.clear()  # Clear session state to avoid conflicts

    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"  # Default to login page

    #st.sidebar.title("Navigation")
    auth_mode = st.radio("Choose an option:", ["Login", "Sign Up"])

    if auth_mode == "Login":
        login_page()
    else:
        signup_page()