# Social Media Application
This is a simple social media application built with Neo4j and Python streamlit. It allows users to create posts, comment on them, and add friends. The application uses Neo4j as the database to store user data, posts, and comments. Images uploaded by users are stored in Azure blob storage with image urls stored in Neo4j.
![Social Media App using Neo4j](https://github.com/user-attachments/assets/8105ade1-a92c-4d9b-bc6f-c29463bcf12f)


# Installation and Setup
**1. Clone the repository**
```bash
git clone https://github.com/DevcharanK/Social-Media-App-Neo4j.git
cd Social-Media-App-Neo4j
```

**2. Install Requirements**
```
pip install -r requirements.txt
```
**3. Update config.py and database.py with your connection strings**

**4. Run the application**
```
streamlit run pages/app.py
```

### File description
- `app.py`: Main application file that contains the Flask app and routes.
- `database.py`: Contains the Neo4j database connection and query functions.
- `image_utils.py`: Contains Azure blob storage functions for uploading and retrieving images.
- `config.py` - Contains the configuration for the application, including the Neo4j connection details and Azure blob storage credentials. - Update with your connection strings
- `creae_new_data.py` - Automatically create new data in the database. This file is used to create new users, posts, and comments in the Neo4j database. It is useful for testing and development purposes.
- `requirements.txt`: Contains the required Python packages for the application.
- `README.md`: This file, which contains the project description and instructions.
- pages
  - `home.py`: Contains the home page route and logic.
  - `auth.py`: Contains the authentication routes - signup and login page logic
  - `post.py`: Contains logic to open and display single posts
  - `profile.py`: Contains logic to open and display user profiles
  - `add_friends_page.py`: Contains logic to open and display the add friends page
