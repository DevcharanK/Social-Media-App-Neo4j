import streamlit as st
from database import get_mutual_friend_count, get_non_friends, add_friend,remove_friend,get_following


def run():
    st.session_state["friends_list"] = {} # Initialize friends list if not already present


    # Debugging: Show session state details
    #st.write("DEBUG: Session State:", st.session_state)

    st.title("Your Profile")
    st.subheader("Manage your friendships")

    col1,col2 = st.columns([1,1])

    if col1.button("⬅️ Back to Profile"):
        if st.session_state["friends_list"]:
            if st.warning("You have unsaved changes. Do you want to proceed without saving?"):
                st.session_state["friends_list"] = {}
                st.session_state["current_page"] = "Profile"
                st.rerun()
        else:
            st.session_state["current_page"] = "Profile"
            st.rerun()

    # Ensure user is logged in
    user_email = st.session_state["email"]
    if not user_email:
        st.warning("You need to be logged in to view and update your profile.")
        return
    
    non_friends = get_non_friends(user_email)
    friends = get_following(user_email)  # Fetch the list of friends for the user

    for user in friends + non_friends:
        col1, col2 = st.columns([3, 1])

        #Display User Detials
        mutual_friends = get_mutual_friend_count(user_email,user['email'])  # Default to 0 if not present
        col1.markdown(
            f"""
            <div style="line-height:1;">
                <b>{user['name']} ({user['email']})</b><br>
                <small>Mutual Friends: {mutual_friends}</small>
                <hr style="margin:5px 0;">
            </div>
            """, unsafe_allow_html = True
        )
        
        #Determine if user is already a friend
        is_friend = user in friends

        if is_friend:
            if col2.button("Remove",key = f"remove_{user['email']}_{user['username']}"):
                print(f"user['email']") # Debugging output to verify the email being processed
                #st.session_state["friends_list"][f"{user['email']}"] = "remove"
                result = remove_friend(user_email, user['email'])  # Call the add_friend function to ensure it's removed from the database
                st.rerun()
                print(result)

        else:
            if col2.button("Add",key = f"add_{user['email']}_{user['username']}"):
                print(f"User email: {user['email']}")  # Debugging output to verify the email being processed
                #st.session_state["friends_list"][f"{user['email']}"] = "add"
                result = add_friend(user_email, user['email'])  # Call the add_friend function to ensure it's added to the database
                st.rerun()
                print(result)  # Debugging output to verify the result of the add_friend call
                
        
    


