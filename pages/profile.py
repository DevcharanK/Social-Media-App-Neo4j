import streamlit as st
from datetime import datetime
from database import get_user_profile, get_user_posts, create_post, get_follower_count, add_friend,get_following_count, delete_post
from image_utils import upload_post_image
import time



def run():
    
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
    profile_picture = user_data.get("profile_image_url", "https://www.gravatar.com/avatar/2c7d99fe281ecd3bcd65ab915bac6dd5?s=250")

    #Logic to add friends and see friend count
    following_count = get_following_count(email)
    follower_count = get_follower_count(email)
    st.session_state["follower_count"] = follower_count  # Store follower count in session state for potential use elsewhere
    st.session_state["following_count"] = following_count  # Store friend count in session state for potential use elsewhere

    
    profile_html = f"""
    <div style="
        max-width: 720px;
        margin: 30px auto;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        font-family: Arial, sans-serif;
        text-align: center;
    ">
        <!-- Profile Picture - Inject CSS styling-->
        <img src="{profile_picture}" alt="Profile Picture" style="
            width: 200px;
            height: 200px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #3498db;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
        ">

        <!-- User Info -->
        <h2 style="color: #333; margin-top: 10px;">{name}</h2>
        <p style="color: #777; font-size: 16px; margin: 5px 0;">@{username}</p>
        <p style="color: #555; font-size: 14px;">📍 {location}</p>

        <!-- Bio Section -->
        <div style="
            background: #f4f4f4;
            padding: 10px;
            border-radius: 10px;
            margin-top: 10px;
        ">
            <p style="color: #333; font-size: 14px;">{bio}</p>
        </div>

        <!-- Followers & Following -->
        <div style="
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
        ">
            <div>
                <strong style="color: #3498db;">{follower_count}</strong>
                <p style="color: #777; font-size: 14px;">Followers</p>
            </div>
            <div>
                <strong style="color: #3498db;">{following_count}</strong>
                <p style="color: #777; font-size: 14px;">Following</p>
            </div>
        </div>
    </div>
    """

    # Display Profile
    st.html(profile_html)
    
    # Columns for add friends add update profile buttons
    col3,col4,col5 = st.columns([1.6,2,1])

    if col3.button("⬅️ Back to Home"):
        st.session_state["current_page"] = "Home"
        st.rerun()# Ensure "Home" matches the actual page filename without .py

    if col4.button("Manage Your Friendships"):
        st.session_state["current_page"] = "Add Friends"
        print(st.session_state)
        st.rerun()  # Debugging: Show session state before redirect

    #Redirect to update form screen if user clicks on update profile button
    if col5.button("Update Profile"):
        st.session_state["current_page"] = "Update Profile"
        print(st.session_state) #debugging
        st.rerun()

    

    @st.dialog('Delete Post Confirmation')
    def delete_post_dialog(post_id):
        st.write(f"Are you sure you want to delete Post {post_id}?")
        if st.button("Yes"):
            # Call the delete function here
            result = delete_post(post_id, email)
            if result:
                st.success(f"Post {post_id} deleted successfully.")
                time.sleep(2)  # Optional: Wait for 2 seconds before rerunning
                st.rerun()
            else:
                st.error(f"Failed to delete Post {post_id}.")
                time.sleep(2)
                st.rerun()
        if st.button("No"):
            st.write("Deletion cancelled.")
            time.sleep(2)
            st.rerun()
        # Debugging: Show session state details

    # Fetch and display user posts
    st.markdown("""
        <style>
            .section-title {
                font-size: 32px;
                font-weight: bold;
                color: {main_headers_color};
                text-align: center;
                margin-top: 30px;
                margin-bottom: 20px;
            }
            .section-subtitle {
                font-size: 24px;
                font-weight: bold;
                color: {main_headers_color};
                text-align: center;
                margin-top: 20px;
                margin-bottom: 10px;
            }
                
            .center-image {
            display: flex;
            justify-content: center;
            align-items: center;
            }
                
        </style>
                """, unsafe_allow_html=True)


    # Display the title with enhanced styling
    st.markdown('<div class="section-title">Your Posts</div>', unsafe_allow_html=True)

    user_posts = get_user_posts(email)

    
    if user_posts:
        for post in user_posts:
            container = st.container()
            with container:
                post_container_style = """
                <div style="
                    background-color: #FFFFFF;
                    padding: 10px;
                    border-radius: 1px;
                    <-box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);->
                    margin-bottom: 20px;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                ">
                """
                colx,coly,colz = st.columns([1, 4, 1])  # Adjust spacing, making col2 smaller
                
                with coly:
                    #Display image if post contains an image
                    if post["image_url"]:
                        st.markdown('<div class="center-image">', unsafe_allow_html=True)  # Center the image
                        st.image(post["image_url"], use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)  # Close the center div
                
                
                col1, col2 = st.columns([10, 1])  # Adjust spacing, making col2 smaller
                with col1:
                    # Format the timestamp
                    formatted_time = datetime.strptime(post["post_created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y • %I:%M %p")
                    
                    # Display the author's name and date in the styled container
                    post_container_style += f"""
                    <div style="font-size: 18px; font-weight: bold; color: #333333;">
                        👤 {post['author']}
                    </div>
                    
                    <div style="font-size: 14px; color: #777777; margin-top: 5px;">
                        📅 {formatted_time}, Likes: {post['like_count']}
                    </div>
                    
                    <div style="
                        background-color: #f9f9f9;
                        padding: 10px;
                        border-radius: 8px;
                        margin-top: 1px;
                        font-size: 16px;
                        color: #333333;
                    ">
                        {post['content']}
                    </div>
                    """
                # Display the delete button in the second column
                
                    '''delete_button = st.button(f"Delete Post 🗑️", key=f"delete_{post['post_id']}")
                    
                    if delete_button:
                        # Confirmation dialog
                        delete_post_dialog(post['post_id'])'''
                    
                    post_container_style += "</div>"  # Close the post container
                    
                    # Render the styled post container in Streamlit
                    st.html(post_container_style)
                    # Create a right-aligned button using columns
                
                with col2:
                    delete_button = st.button(f"🗑️", key=f"delete_{post['post_id']}")
                    if delete_button:
                        delete_post_dialog(post['post_id'])
    else:
        # Display a message if there are no posts
        st.markdown('<div class="section-subtitle">You havent posted anything yet!</div>', unsafe_allow_html=True)

        #Create a new post!
        cont = st.container()
        with cont:
            new_post_form = st.form(key = "new_post_form",clear_on_submit=True)
            with new_post_form:
                st.write("Share your thoughts with your friends!")
                new_post_content = st.text_area("Post Content", 
                                                placeholder = "What's on your mind?", 
                                                key="new_post_content")
                
                # File uploader for image
                uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

                submitted = new_post_form.form_submit_button("Post")

                if submitted:
                    if new_post_content.strip() == "" or uploaded_image is None:
                        st.warning("Post content cannot be empty.")
                    else:
                        # Generate image url if an image is uploaded
                        image_url = None
                        if uploaded_image:
                            image_url = upload_post_image(uploaded_image)

                        # Add the post to the database
                        result = create_post(email,new_post_content,image_url)
                        
                        if result:
                            st.success("Post added successfully!")
                            #st.session_state['new_post_content'] = ""  # Clear the text area
                            st.rerun()
                        else:
                            st.error("Failed to add post. Please try again.")

    

    if st.button("Test Database Connection"):
        test_data = get_user_profile(email),get_following_count(email), get_follower_count(email)
        st.write("Current DB Data:", test_data)  # Should match Neo4j Browser

