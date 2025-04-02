
import streamlit as st
from database import get_post_details, add_comment, like_post,unlike_post
from datetime import datetime

def run():
    # Check if user is authenticated
    if "email" not in st.session_state:
        st.session_state["current_page"] = "Auth"
        st.rerun()

    # Check if a post is selected
    if "selected_post" not in st.session_state:
        st.session_state["current_page"] = "Home"
        st.rerun()

    # Get the post details
    post_id = st.session_state["selected_post"]
    post_author = st.session_state["author_name"]
    post = get_post_details(post_id, post_author)

    # Handle case when the post is not found
    if not post:
        st.error("Post not found.")
        return

    # Format timestamp
    formatted_time = datetime.strptime(post["timestamp"], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y • %I:%M %p")

    # Initialize session state for like tracking
    if f"liked_{post_id}" not in st.session_state:
        st.session_state[f"liked_{post_id}"] = False

    cola,colb,colc = st.columns([2, 5, 2])
    with colb:
        #show image
        if post['image_url']:
            st.image((post['image_url']), use_container_width=True, output_format="auto")
        
    # Social media-style HTML template
    post_html = f"""
    <div style="
        max-width: 600px;
        margin: 20px auto;
        background-color: white;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        padding: 20px;
        font-family: Arial, sans-serif;
    ">
        <div style="display: flex; align-items: center;">
            <div style="font-weight: bold; font-size: 18px; color: #333;">👤 {post['author']}</div>
        </div>

        <div style="font-size: 14px; color: #777; margin-top: 5px;">
            📅 {formatted_time}
        </div>

        <div style="
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-size: 16px;
            color: #333;
        ">
            {post['content']}
        </div>

        <!-- Like and comment section -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <div style="font-size: 16px; color: #777;">❤️ {post['like_count']} Likes</div>
        </div>

    </div>
    """

    # Display post details
    st.html(post_html)

    # Comments Section
    st.subheader("Comments")
    #if not post["comments"]:
        #st.info("No comments yet.")
        
    if post["comments"]:
        for comment in post["comments"]:
            st.markdown(f"""
            <div style="
                background-color: #f0f2f6;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 10px;
                font-size: 14px;
            ">
                <b>{comment['author']}</b>: {comment['text']}
            </div>
            """, unsafe_allow_html=True)

    # Add comment form
    new_comment = st.text_area("Add a comment...", key="new_comment")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💬 Post Comment"):
            if new_comment.strip() == "":
                st.warning("Comment cannot be empty.")
            else:
                add_comment(post_id, st.session_state["email"], new_comment)
                st.success("Comment posted successfully.")
                st.rerun()
    
    with col2:
        if not st.session_state[f"liked_{post_id}"]:
            if st.button("❤️ Like Post"):
                like_post(post_id)
                st.session_state[f"liked_{post_id}"] = True  # Mark post as liked
                st.success("Post Liked")
                st.rerun()
        else:
            if st.button("❤️ Unlike"):
                # Unlike logic (if applicable)
                unlike_post(post_id)
                st.session_state[f"liked_{post_id}"] = False
                st.success("Post Unliked")
                st.rerun()
    # Back button
    if st.button("🔙 Back to Home"):
        st.session_state["current_page"] = "Home"
        st.rerun()
