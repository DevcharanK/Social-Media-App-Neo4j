import streamlit as st
from database import db  
from datetime import datetime
from database import get_friend_posts,create_post,run_custom_query,build_search_query_new
from image_utils import upload_post_image


def run():
    st.title("Feed")

    # Ensure user is logged in
    if "email" not in st.session_state:
        st.warning("Please login first.")
        return

    email = st.session_state["email"]

    #Profile and logout pages on two cols
    col1,col2 = st.columns([7,1])
    with col1:
        if st.button("Go to Profile"):
            st.session_state["current_page"] = "Profile"
            print(st.session_state) #debugging
            st.rerun()
    with col2:
        if st.button("Logout"):
            st.session_state["current_page"] = "Auth"
            st.rerun()# Ensure "Home" matches the actual page filename without .py
    
    #Create a container for search bar and its results
    search_container = st.container()
    with search_container:
        # Streamlit UI setup
        search_query = st.text_input("Search Posts or Friends:")

        if search_query:
            # Build and execute the Cypher query
            #cypher_query = build_search_query(search_query)
            #filtered_posts = run_custom_query(cypher_query)  # Custom function to execute Cypher queries
            
            filtered_posts = build_search_query_new(search_query)  # Custom function to execute Cypher queries
            # Display search results (Posts)
            
            if filtered_posts:
                for post in filtered_posts:  # Looping through posts
                    c = st.container()  # Create a container for each post
                    with c:
                        
                        post_container_style = """
                        <div style="
                            background-color: #FFFFFF;
                            padding: 16px;
                            border-radius: 10px;
                            <-box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);->
                            margin-bottom: 20px;
                            font-family: Arial, sans-serif;
                            font-size: 16px;
                        ">
                        """

                        
                        col1,col_image,col2 = st.columns([5,2,2])  # Adjust spacing, making col2 smaller
                        with col_image:
                            #Display post image on top if available
                            if post['image_url']:
                                st.image((post['image_url']), width = 100, output_format="auto")
                        
                        with col1:
                            formatted_time = datetime.strptime(post["post_created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y • %I:%M %p")
                        
                            # Add the author's name and date in the styled container
                            post_container_style += f"""
                            <div style="font-size: 18px; font-weight: bold; color: #333333;">
                                👤 {post['author_name']}
                            </div>
                            
                            <div style="font-size: 14px; color: #777777; margin-top: 5px;">
                                📅 {formatted_time}
                            </div>
                            
                            <div style="
                                background-color: #f9f9f9;
                                padding: 12px;
                                border-radius: 8px;
                                margin-top: 15px;
                                font-size: 16px;
                                color: #333333;
                            ">
                                {post['content']}
                            </div>
                            """
                            # Close the post container
                            post_container_style += "</div>"

                            # Render the post container in Streamlit
                            st.html(post_container_style)

                        with col2:
                            # Add some spacing and a decorative divider
                            #st.markdown("<br>", unsafe_allow_html=True)
                            if st.button("Open Post",key = f"open_post_{post['author_name']}_{post['post_id']}"):
                                st.session_state["selected_post"] = post['post_id']
                                st.session_state["author_name"] = post['author_name']  # Store author name for context
                                st.session_state["current_page"] = "Post"  # Navigate to the post details page
                                print(st.session_state)  # Debugging: Show session state before redirect    
                                st.rerun()
                
            else:
                st.info("No results found.")

    def clear_post_content():
        """Callback function to clear post content"""
        st.session_state["new_post_content"] = ""

    # Initialize session state for post content
    if "new_post_content" not in st.session_state:
        st.session_state['new_post_content'] = ""
    #st.session_state['new_post_content'] = ""  # Clear the text area on page load

    # Show post creation form only if no search query is present
    if not search_query:
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
        # Debugging: Show session state details
        #st.write("DEBUG: Session State:", st.session_state)

    posts = get_friend_posts(email)  # Fetch friends' posts

    if not posts:
        st.info("No posts from your friends yet!")
        

    if not search_query:
        for post in posts:  # Looping through posts
            
            c = st.container()  # Create a container for each post
            with c:
                post_container_stylea = """
                <div style="
                    background-color: #FFFFFF;
                    padding: 20px;
                    border-radius: 15px;
                    <-box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);->
                    margin-bottom: 20px;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                ">
                """
                post_container_styleb = """
                <div style="
                    background-color: #FFFFFF;
                    padding: 0px;
                    border-radius: 10px;
                    <-box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);->
                    margin-bottom: 20px;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                ">
                """
                post_container_style = """
                <div style="
                    background-color: #FFFFFF;
                    padding: 0px;
                    border-radius: 10px;
                    <-box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);->
                    margin-bottom: 20px;
                    font-family: Arial, sans-serif;
                    font-size: 16px;
                ">
                """
                
                cola,colb = st.columns([8,1]) 
                with cola:
                    formatted_time = datetime.strptime(post["post_created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y • %I:%M %p")
                
                    post_container_stylea += f"""
                    <div style="font-size: 18px; font-weight: bold; color: #333333;">
                        👤 {post['author_name']}
                    </div>
                    
                    <div style="font-size: 14px; color: #777777; margin-top: 5px;">
                        📅 {formatted_time}
                    </div>"""
                    
                    post_container_stylea += "</div>"

                    # Render the post container in Streamlit
                    st.html(post_container_stylea)

                with colb:
                    # Add some spacing and a decorative divider
                    #st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Open",key = f"open_post_{post['author_name']}_{post['post_id']}"):
                        st.session_state["selected_post"] = post['post_id']
                        st.session_state["author_name"] = post['author_name']  # Store author name for context
                        st.session_state["current_page"] = "Post"  # Navigate to the post details page
                        print(st.session_state)  # Debugging: Show session state before redirect    
                        st.rerun()

                if post['image_url']:
                    colx,coli, coly = st.columns([2,5,2])
                    with coli:
                    #Display post image on top if available                    
                        st.image((post['image_url']), use_container_width=True, output_format="auto")
                
                col1,col2 = st.columns([1.25,9])  # Adjust spacing, making col2 smaller
                with col1:
                    # Add the author's name and date in the styled container
                    post_container_styleb += f"""
                    
                    
                    <div style="
                        background-color: #f9f9f9;
                        padding: 12px;
                        border-radius: 8px;
                        margin-top: 15px;
                        font-size: 16px;
                        color: #333333;
                    ">
                        ❤️{post['post_like_count']}
                    </div>
                    """
                    # Close the post container
                    post_container_styleb += "</div>"
                    st.html(post_container_styleb)
                    
                    # Display number of likes
                    #st.write(f"❤️ {post['like_count']} Likes")

                with col2:
                    
                    # Add the author's name and date in the styled container
                    post_container_style += f"""
                    
                    
                    <div style="
                        background-color: #f9f9f9;
                        padding: 12px;
                        border-radius: 8px;
                        margin-top: 15px;
                        font-size: 16px;
                        color: #333333;
                    ">
                        {post['content']}
                    </div>
                    """
                    # Close the post container
                    post_container_style += "</div>"

                    # Render the post container in Streamlit
                    st.html(post_container_style)

                
            st.divider()

    

