
from neo4j import GraphDatabase
import uuid
from datetime import datetime

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "11112222"

AUTH = (NEO4J_USER, NEO4J_PASSWORD)

driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters={}):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]  # Fetch all results before closing
        
    # Function for write queries (INSERT, UPDATE, DELETE)
    def write_query(self, query, parameters={}):
        print(f"\n  Executing WRITE query:")
        print(f"Query: {query}")
        print(f"Parameters: {parameters}")  # Debugging output to see the parameters being passed

        try:
            with self.driver.session() as session:
                result = session.execute_write(self._execute_write, query, parameters)
                print(f"Result: {result}")  # Debugging output to see the result of the write operation
                return result  # Return the result of the write operation
        except Exception as e:
            print(f"Error executing write query: {str(e)}")
            return None

    @staticmethod
    def _execute_write(tx, query, parameters):
        result = tx.run(query, parameters)
        return [record for record in result]  # Ensure results are captured
    
db = Neo4jConnection(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

########################################
#           EMBEDDED QUERIES           #
########################################

# BUILD Custom Query
def build_search_query_new(search_query):
    query = """
    // Create the query for searching posts content
    MATCH (u:User)-[:FOLLOWS]->(f:User)-[:CREATES]->(p:Post)
    WHERE toLower(p.content) CONTAINS toLower($search_query)
    RETURN p.content AS content, p.post_created_at AS post_created_at, p.post_id AS post_id, p.image_url AS image_url, f.email AS author_email, f.name AS author_name, 'Content Search' AS source

    UNION

    // Create the query for searching by friends' names
    MATCH (u:User)-[:FOLLOWS]->(f:User)-[:CREATES]->(p:Post)
    WHERE toLower(f.name) CONTAINS toLower($search_query)
    RETURN p.content AS content, p.post_created_at AS post_created_at, p.post_id AS post_id, p.image_url AS image_url, f.email AS author_email, f.name AS author_name, 'Friends Search' AS source

    ORDER BY post_created_at DESC
    """
    
    # Run the query with parameters
    results = db.run_query(query, {"search_query": search_query})
    
    if results:
        # Sort results based on post creation date
        sorted_results = sorted(results, key=lambda x: datetime.strptime(x["post_created_at"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
        return [
            {
                "content": record["content"],
                "post_created_at": record["post_created_at"],
                "post_id": record["post_id"],
                "image_url": record["image_url"],
                "author_email": record["author_email"],
                "author_name": record["author_name"],
                "source": record["source"]
            }
            for record in sorted_results
        ]
    return []


# Search content from posts or friends
def build_search_query(search_query):
    # Create the query for searching posts content
    content_search_query = f"""
    MATCH (u:User)-[:FOLLOWS]->(f:User)-[:CREATES]->(p:Post)
    WHERE toLower(p.content) CONTAINS toLower("{search_query}")
    RETURN p.content AS content, p.post_created_at AS post_created_at, p.post_id AS post_id,p.image_url AS image_url,f.email as author_email,f.name as author_name, 'Content Search' AS source
    """
    
    # Create the query for searching by friends' names
    friends_search_query = f"""
    MATCH (u:User)-[:FOLLOWS]->(f:User)-[:CREATES]->(p:Post)
    WHERE toLower(f.name) CONTAINS toLower("{search_query}")
    RETURN p.content AS content, p.post_created_at AS post_created_at, p.post_id AS post_id,p.image_url AS image_url,f.email as author_email,f.name as author_name, 'Friends Search' AS source
    """
    
    # Combine both queries using UNION
    combined_query = content_search_query + " UNION " + friends_search_query
    
    return combined_query

def run_custom_query(query):
    with driver.session() as session:
        results = session.run(query)
        if results:
                sorted(results, key=lambda x: datetime.strptime(x["post_created_at"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
                return [
                    {
                        "content": record["content"],
                        "post_created_at": record["post_created_at"],
                        "post_id": record["post_id"],
                        "image_url": record["image_url"],
                        "author_email": record["author_email"],
                        "author_name": record["author_name"],
                        "source": record["source"]
                    }
                    for record in results
                ]
        return []  # Fetch all results before closing

def authenticate_user(email, password):
    """
    Check if a user exists with the given email and password.
    Returns user info if authentication is successful, else None.
    """
    query = """
    MATCH (u:User {email: $email, password: $password})
    RETURN u.user_id AS user_id, u.name AS name, u.email AS email
    """
    
    with driver.session() as session:
        result = session.run(query, email=email, password=password)
        user = result.single()
    
    if user:
        return {"user_id": user["user_id"], "name": user["name"], "email": user["email"]}
    return None  # Authentication failed


def get_user(email, password):
    query = """
    MATCH (u:User {email: $email, password: $password})
    RETURN u.user_id AS user_id, u.name AS name, u.email AS email
    """
    result = db.run_query(query, {"email": email, "password": password})
    return result.single()

#Create a new user in the database - Through SIGNUP page
def create_user(email,name, password, date_of_birth):
    with driver.session() as session:
        try:
            # Check if email already exists
            result = session.run("MATCH (u:User {email: $email}) RETURN u", email=email)
            if result.single():
                return False, "Email already exists. Please log in."

            # Create new user
            session.run(
                "CREATE (u:User {email: $email,name: $name, password: $password, date_of_birth: $dob, profile_image_url: $temp_image_url, user_id: $user_id})",
                email=email,
                password=password,
                dob=date_of_birth,
                name=name,
                temp_image_url = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&s=200",
                user_id=str(uuid.uuid4()) 
            )
            return True, "User created successfully."
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    return False, "Unexpected error occurred."  # This ensures it never returns None

def get_user_posts(email):
    query = """
    MATCH (u:User {email: $email})-[:CREATES]->(p:Post)
    RETURN p.post_id AS post_id, p.content AS content, p.post_created_at as post_created_at, p.like_count as post_like_count, p.image_url as image_url, u.name AS author
    ORDER BY p.post_created_at DESC
    """
    results = db.run_query(query, {"email": email})
    if results:
        return [
            {
                "post_id": record["post_id"],
                "content": record["content"],
                "post_created_at": record["post_created_at"],
                "like_count": record["post_like_count"],
                "author": record["author"],
                "image_url": record["image_url"]
            }
            for record in results
        ]
    return []

# RETURNS individual post details as a dictionary
def get_post_details(post_id,post_author):
    query = """
    MATCH (u:User {name: $post_author})-[:CREATES]->(p:Post {post_id: $post_id})
    OPTIONAL MATCH (p)-[:CONTAINS]->(c:Comment)
    OPTIONAL MATCH (commenter)-[:WRITES]->(c)
    RETURN p.content AS content, p.post_created_at as post_created_at, p.like_count as post_like_count,p.image_url as image_url, u.name AS author, collect({author: commenter.name, text: c.content}) AS comments
    """
    result = db.run_query(query, {"post_id": post_id,"post_author": post_author})
    if result:
        record = result[0]
        return {
            "content": record["content"],
            "author": record["author"],
            "comments": record["comments"],
            "like_count": record["post_like_count"],
            "timestamp": record["post_created_at"],
            "image_url": record["image_url"]
        }
    return None

def create_post(email, content, image_url):
    post_id = str(uuid.uuid4())
    post_created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    query = """
    MATCH (u:User {email: $email})
    CREATE (p:Post {post_id: $post_id, content: $content, post_created_at: $post_created_at, like_count: 0, image_url: $image_url})
    CREATE (u)-[:CREATES]->(p)
    RETURN p.post_id AS post_id, p.content AS content, p.post_created_at as post_created_at, p.like_count as post_like_count, p.image_url as image_url, u.name AS author
    """
    try:
        result = db.write_query(query, 
                   {"email": email, 
                    "content": content,
                    "post_id":post_id,
                    "post_created_at": post_created_at,
                    "image_url": image_url
                    })
        print(f"Query Result: {result}")  # Debugging

        if not result:
            print(f"Unable to create post for: {email}")
            return None
        else:
            print(f"Post created for: {email}")
        return result[0]
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return None
    
def delete_post(post_id, email):
    query = """
    MATCH (u:User) -[:CREATES]->(p:Post )
    WHERE p.post_id = $post_id and u.email = $email
    OPTIONAL MATCH (p)-[r:CONTAINS]->(c:Comment)
    detach delete p
    
    """
    try:
        # Run the delete query
        db.write_query(query, {"post_id": post_id, "email": email})
        print(f"Successfully deleted post: {post_id}")  # Log success
        return f"Successfully deleted post: {post_id}"
    except Exception as e:
        print(f"Database Error: {str(e)}")  # Log any errors that occur
        return None


def add_comment(post_id, email, content):
    query = """
    MATCH (p:Post {post_id: $post_id}), (u:User {email: $email})
    CREATE (c:Comment {comment_id: $random_comment_id, content: $content, created_at: datetime()})
    CREATE (p)-[:CONTAINS]->(c)
    CREATE (u)-[:WRITES]->(c)
    """
    db.run_query(query, {"post_id": post_id, "email": email, "content": content,"random_comment_id":str(uuid.uuid4())})

def like_post(post_id):
    query = """
    MATCH (p:Post {post_id: $post_id})
    SET p.like_count = COALESCE(p.like_count, 0) + 1
    RETURN p.like_count AS like_count
    """
    db.run_query(query, {"post_id": post_id})

def unlike_post(post_id):
    query = """
    MATCH (p:Post {post_id: $post_id})
    SET p.like_count = COALESCE(p.like_count, 0) - 1
    RETURN p.like_count AS like_count
    """
    db.run_query(query, {"post_id": post_id})

def get_friend_posts(email):
    query = """
    // Match posts from people the user follows
    MATCH (u:User {email: $email})-[:FOLLOWS]->(friend:User)-[:CREATES]->(p:Post)
    RETURN friend.email AS author_email, friend.name AS author_name, p.content AS content, p.post_created_at AS post_created_at, p.post_id AS post_id,p.image_url AS image_url, p.like_count AS post_like_count, 'Friend' AS source

    UNION

    // Match posts created by the user
    MATCH (u:User {email: $email})-[:CREATES]->(p:Post)
    RETURN u.email AS author_email, u.name AS author_name, p.content AS content, p.post_created_at AS post_created_at, p.post_id AS post_id,p.image_url AS image_url,p.like_count AS post_like_count, 'User' AS source
    
    
    ORDER BY post_created_at DESC
    """
    results = db.run_query(query, {"email": email})  # No `.data()`, result is already a list
    if results:
        sorted_results = sorted(results, key=lambda x: datetime.strptime(x["post_created_at"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
        return [
            {
                "author_email": record["author_email"],
                "author_name": record["author_name"],
                "content": record["content"],
                "post_created_at": record["post_created_at"],
                "post_id": record["post_id"],
                "image_url": record["image_url"],
                "post_like_count": record["post_like_count"]
            }
            for record in sorted_results
        ]
    return []


def update_user_profile(email, bio, location,username, image_url):
    print(f"Updating Profile for {email}...")  # Debugging    
    query = """
    MATCH (u:User {email: $email})
    SET u.bio = $bio, u.location = $location, u.username = $username, u.profile_image_url = $image_url
    RETURN u {.email, .bio, .location, .username, .profile_image_url } AS updated_user
    """
    
    try:
        result = db.write_query(query, {
            "email": email, 
            "bio": bio, 
            "location": location,
            "username": username,
            "image_url": image_url
            })
        print(f"Query Result: {result}")  # Debugging

        if not result:
            print(f"No User found with email: {email}") 
            return None
        else:
            print("Succesfully updated")  # Debugging

        return result[0].get("updated_user")
    
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return None
    
# Function to retrieve user profile details    
def get_user_profile(email):
    """Retrieve user details based on email."""
    query = """
    MATCH (u:User {email: $email})
    RETURN u.name AS name, u.email AS email, u.bio AS bio, u.location AS location, u.username AS username, u.user_id AS user_id, u.profile_image_url AS profile_image_url
    """

    result = db.run_query(query, {"email": email})
    return result[0] if result else None

def get_follower_count(email):
    query = """
    MATCH (u:User {email: $email})<-[:FOLLOWS]-(follower)
    RETURN COUNT(follower) AS follower_count
    """
    result = db.run_query(query, {"email": email})
    return result[0]["follower_count"] if result else 0
    
def get_following_count(email):
    query = """
    MATCH (u:User {email: $email})-[:FOLLOWS]->(friend)
    RETURN COUNT(friend) AS following_count
    """
    result = db.run_query(query, {"email": email})
    return result[0]["following_count"] if result else 0

def get_following(email):
    query = """
    MATCH (u:User {email: $email})
    MATCH (other:User)
    WHERE (u)-[:FOLLOWS]->(other) AND u <> other
    RETURN other.email AS email, other.name AS name, other.username AS username, other.user_id AS user_id
    """
    return db.run_query(query, {"email": email})

def get_non_friends(email):
    query = """
    MATCH (u:User {email: $email})
    MATCH (other:User)
    WHERE NOT (u)-[:FOLLOWS]->(other) AND u <> other
    OPTIONAL MATCH (u)-[:FOLLOWS]->(mutual)-[:FOLLOWS]->(other)
    WITH other, COUNT(mutual) AS mutual_friends
    RETURN other.email AS email, other.name AS name, other.username AS username, other.user_id as user_id, COALESCE(mutual_friends, 0) AS mutual_friends
    ORDER BY mutual_friends DESC
    """
    return db.run_query(query, {"email": email})

def get_mutual_friend_count(user_email, other_email):
    query = """
    MATCH (u:User {email: $user_email})-[:FOLLOWS]->(friend:User)-[:FOLLOWS]->(other:User {email: $other_email})
    RETURN COUNT(friend) AS mutual_friend_count
    """
    result = db.run_query(query, {"user_email": user_email, "other_email": other_email})
    return result[0]["mutual_friend_count"] if result else 0

def add_friend(user_email, friend_email):
    query = """
    MATCH (u:User {email: $user_email}), (f:User {email: $friend_email})
    MERGE (u)-[:FOLLOWS]->(f)
    RETURN u.email AS user, f.email AS friend
    """
    try:
        result = db.write_query(query, {
            "user_email": user_email, 
            "friend_email": friend_email
            })
        print(f"Query Result: {result}")  # Debugging

        if not result:
            print(f"Unable to add friend: {friend_email}")
            return None
        else:
            print(f"Added friend: {friend_email}")
        return result[0]
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return None

def remove_friend(user_email,friend_email):
    query = """
    MATCH (u:User {email: $user_email})-[r:FOLLOWS]->(f:User {email: $friend_email})
    DELETE r
    RETURN u.email AS user, f.email AS friend, f.name AS friend_name
    """
    try:
        result = db.write_query(query, {
            "user_email": user_email, 
            "friend_email": friend_email
            })
        print(f"Query Result: {result}")  # Debugging

        if not result:
            print(f"Unable to unfollow friend: {friend_email}")
            return None
        else:
            print(f"Unfollowed friend: ({friend_email})")
        return result[0]
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return None
    

if __name__ == "__main__":
    # Test the database functions here
    
    #posts = get_friend_posts("sophia.white@example.com")

    #dele = delete_post("404fcab3-257f-487d-89b3-04b78ca21af8","sophia.white@example.com")

    #print(f"Delete Post: {dele}")
    
    #print(type(posts))
    #print("---------------------")
    #for post in posts:
    #    print(post["post_created_at"])

    #print(f"Content: {post['content']}")
    #print(f"Author: {post['author']}")
    #print(f"Comments: {post['comments']}")

    #Test custom query
    build_search_query("Emily")
    results = run_custom_query("MATCH (u:User) RETURN u")
    for record in results:
        print(record)
    
    