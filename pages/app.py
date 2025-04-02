import streamlit as st
from auth import run as auth_page
from home import run as home_page
from profile import run as profile_page
from post import run as post_page
from update_profile import run as update_profile_page
from add_friends_page import run as add_friends_page

# Ensure session state has 'current_page'
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Auth"  # Default to login/signup page

# Function to handle page navigation
def navigate_to(page):
    st.session_state["current_page"] = page
    st.rerun()

# Page routing logic
if st.session_state["current_page"] == "Auth":
    auth_page()
elif st.session_state["current_page"] == "Home":
    home_page()
elif st.session_state["current_page"] == "Profile":
    profile_page()
elif st.session_state["current_page"] == "Post":
    post_page()
elif st.session_state["current_page"] == "Update Profile":
    update_profile_page()
elif st.session_state["current_page"] == "Add Friends":
    add_friends_page()