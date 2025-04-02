
import streamlit as st
from database import get_user_profile, get_user_posts, update_user_profile 
from image_utils import upload_profile_image

def run():
    st.title("Update your Profile")

    # Ensure user is logged in
    if "email" not in st.session_state:
        st.warning("You need to be logged in to view and update your profile.")
        return

    email = st.session_state["email"]  # Get user's email from session state

    # Debugging: Show session state details
    #st.write("DEBUG: Session State:", st.session_state)

    # Fetch user profile data
    user_data = get_user_profile(email)

    if not user_data:
        st.error("User profile not found.")
        return

    name = user_data.get("name", "Unknown User")
    bio = user_data.get("bio", "Update profile to add bio!")
    location = user_data.get("location", "Unknown Location")
    username = user_data.get("username", "Unknown Username")
    current_profile_image_url = user_data.get("profile_image_url")

    if st.button("⬅️ Back to Profile"):
        st.session_state["current_page"] = "Profile"
        st.rerun()

    #current_profile_pic = current_profile_image_url 
    update_form = st.form(key="update_profile_form")
    with update_form:

        # File uploader for image
        profile_image = st.file_uploader("Upload your photo", type=["jpg", "jpeg", "png"])
        new_bio = st.text_area("Bio", value=bio)
        new_location = st.text_input("Location", value=location)
        new_username = st.text_input("Username", value=username)
        new_email = st.text_input("Email", value=email, disabled=True)  # Disable email field

        #new_password = st.text_input("Password", type="password")  # Optional: Add password field if needed

        # If submitted
        submitted = update_form.form_submit_button("Save Changes")
        # Debugging: Show session state details
        #st.write("DEBUG: Session State:", st.session_state)
        
        #if button is clicked
        if submitted:

            #Generate image url if an image is uploaded
            image_url = current_profile_image_url  # Default to current profile picture URL
            if profile_image:
                image_url = upload_profile_image(profile_image)

            #DEBUG Code
            #print("within if loop",submitted)
            #st.write(f"Before Update - Email: {email}, Bio: {bio}, Location: {location}")  # Debugging UI
            #st.write(st.session_state)

            # Update the user profile in the database
            update_user_profile(email, new_bio, new_location,new_username,image_url)

            #print("Did you update profile?",submitted)
            # Fetch updated profile data
            result = get_user_profile(email)

            # Debugging: Show raw result structure
            #st.write("Raw update result:", result)  # Critical for debugging

            #st.write(f"After Update - New Bio: {new_bio}, New Location: {new_location}")  # Debugging UI
            #st.write(f"Database Update Result: {result}")  # Debugging UI

            if result:

                st.write(st.session_state)
                #st.success("Profile updated successfully!")

                # Force a refresh
                #st.session_state["profile_updated"] = True  # Store update flag in session
                #st.rerun()

                st.success(f"Updated profile: {result['bio']} | {result['location']}")
                # Update session data immediately
                print(st.session_state) #debugging
                st.session_state.profile_data = result
                st.session_state["current_page"] = "Profile"  # Navigate back to Profile page
                st.rerun()
            else:
                st.error("Error updating profile. Please try again.")
        

    

    if st.button("Test Database Connection"):
        test_data = get_user_profile(email)
        st.write("Current DB Data:", test_data)  # Should match Neo4j Browser

