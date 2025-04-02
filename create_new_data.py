from faker import Faker
import datetime
from datetime import timedelta
from neo4j import GraphDatabase
import random
import uuid

# Neo4j Connection Setup
NEO4J_URI = "bolt://localhost:7687"  # Change if using a remote database
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "11112222"

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters={}):
        with self.driver.session() as session:
            return session.run(query, parameters)

db = Neo4jConnection(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

fake = Faker()
fake_dob = fake.date_of_birth(minimum_age=18, maximum_age=80)

def random_past_date():
    """Generate a random date within the last year."""
    days_ago = random.randint(0, 365)  # Random number of days in the past
    random_time = timedelta(
        hours=random.randint(0, 23), 
        minutes=random.randint(0, 59), 
        seconds=random.randint(0, 59)
    )
    return (datetime.datetime.now() - timedelta(days=days_ago) - random_time).strftime("%Y-%m-%dT%H:%M:%SZ")


# Store user data for relationships
users = []

people = [
    {
        "name": "Alice Johnson",
        "username": "alicej",
        "email": "alice.johnson@example.com",
        "bio": "Software engineer with a love for AI and coffee.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "securePass123"
    },
    {
        "name": "Michael Smith",
        "username": "mike_smith",
        "email": "michael.smith@example.com",
        "bio": "Tech enthusiast, avid gamer, and part-time blogger.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "mikeStrong!99"
    },
    {
        "name": "Samantha Lee",
        "username": "samantha_lee",
        "email": "samantha.lee@example.com",
        "bio": "Fitness trainer sharing tips on health and wellness.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "fitLife2023"
    },
    {
        "name": "Daniel Martinez",
        "username": "dan_martinez",
        "email": "daniel.martinez@example.com",
        "bio": "Photographer capturing the world one shot at a time.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "photoPass!"
    },
    {
        "name": "Jessica Brown",
        "username": "jessb",
        "email": "jessica.brown@example.com",
        "bio": "Bookworm, writer, and cat lover.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "bookLover42"
    },
    {
        "name": "David Wilson",
        "username": "david_wilson",
        "email": "david.wilson@example.com",
        "bio": "Entrepreneur building the next big thing.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "startUpKing"
    },
    {
        "name": "Emily Davis",
        "username": "emily_d",
        "email": "emily.davis@example.com",
        "bio": "Travel blogger exploring the world.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "travelBug2023"
    },
    {
        "name": "Robert Thomas",
        "username": "robert_thomas",
        "email": "robert.thomas@example.com",
        "bio": "Foodie and chef, sharing recipes with the world.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "chefLife!55"
    },
    {
        "name": "Sophia White",
        "username": "sophiaw",
        "email": "sophia.white@example.com",
        "bio": "Digital marketer helping brands grow online.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "marketingPro$"
    },
    {
        "name": "James Anderson",
        "username": "james_a",
        "email": "james.anderson@example.com",
        "bio": "Musician, guitarist, and songwriter.",
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=80),
        "password": "rockOn2023"
    }
]

for person in people:
    name = person["name"]
    email = person["email"]
    username = person["username"]
    bio = person["bio"]
    dob = person["dob"]
    password = person["password"]
    user_id = str(uuid.uuid4())
    query = """
    CREATE (u:User {user_id: $user_id, name: $name, username: $username, email: $email, bio: $bio, date_of_birth: $dob, password: $password})
    RETURN u
    """
    db.run_query(query, {
            "user_id": user_id, 
            "name": name, 
            "username": username, 
            "email": email, 
            "bio": bio, 
            "dob": dob.strftime("%Y-%m-%d"),
            "password": password})
    users.append({"user_id": user_id, "username": username})



# Create posts for users
post_contents = [
    "Just finished an amazing book! Highly recommend it to everyone.",
    "Had the best coffee today. There’s something magical about the first sip.",
    "Exploring the city and found a hidden gem of a restaurant!",
    "Coding late at night feels different. The world is quiet, and the ideas just flow.",
    "Workout done! Feeling energized and ready to take on the day.",
    "AI is evolving so fast. Can’t wait to see where we’ll be in five years!",
    "Does anyone else feel like time moves faster on weekends?",
    "Tried making homemade pasta today. Messy but totally worth it!",
    "A little progress each day adds up to big results. Keep going!",
    "Traveling soon! Any recommendations for must-visit places?",
    "Listening to my favorite playlist and getting lost in the music. Pure bliss!",
    "Some days are tough, but remember: you’ve made it through all your bad days so far!",
    "Learning a new programming language is like unlocking a new superpower.",
    "Finally set up my home office. Productivity, here I come!",
    "There’s something about watching the sunset that makes you appreciate life a little more.",
    "Can’t believe how fast this year is going by. Feels like yesterday was January!",
    "Late-night thoughts: If we discovered aliens, would they find us interesting?",
    "Small wins matter. Celebrate them!",
    "Cooking is like coding—follow the recipe, but don’t be afraid to experiment.",
    "Social media detox for a few days. Let’s see how this goes!"
]

posts = []  
for user in users:
    num_posts = random.randint(1, 3)
    for _ in range(num_posts):
        post_id = str(uuid.uuid4())
        content = random.choice(post_contents)
        like_count = random.randint(0, 100)  # Random like count for the post
        post_created_at = random_past_date()
        query = """
        MATCH (u:User {user_id: $user_id})
        CREATE (p:Post {post_id: $post_id, content: $content, post_created_at: $post_created_at, like_count: $like_count})
        CREATE (u)-[:CREATES]->(p)
        RETURN p
        """
        db.run_query(query, {
                    "user_id": user["user_id"], 
                    "post_id": post_id, 
                    "content": content, 
                    "like_count": like_count,
                    "post_created_at": post_created_at})
        posts.append({"post_id": post_id, "user_id": user["user_id"]})


# Create comments on random posts
comment_texts = [
    "This is so relatable! Totally agree with you.",
    "I never thought about it this way. Great perspective!",
    "Hahaha, this made my day! 😂",
    "I love this idea! Might give it a try myself.",
    "So true! I feel the same way.",
    "Where did you learn this? Super interesting!",
    "I completely disagree, but I respect your opinion.",
    "Wow, that’s an amazing experience! Thanks for sharing.",
    "Couldn’t have said it better myself!",
    "This is exactly what I needed to hear today.",
    "Can you elaborate more on this? Sounds intriguing!",
    "I have a different take on this, but I see where you're coming from.",
    "Great advice! Definitely bookmarking this.",
    "Such a powerful message. Thanks for sharing!",
    "I wish more people understood this!",
    "Haha, I’ve been there! Glad to know I’m not alone.",
    "This reminds me of something similar that happened to me.",
    "I’ve been trying to work on this too. Any tips?",
    "This post deserves way more attention!",
    "I’d love to hear more about your thoughts on this!",
    "Mind if I share this with my friends? It's so insightful!",
    "You just put into words what I’ve been feeling lately.",
    "I was skeptical at first, but this really made me think.",
    "This is hilarious! You should write more like this.",
    "I completely relate to this. Thanks for putting it out there!",
    "I didn’t know that! Thanks for the info!",
    "You’ve inspired me to take action. Appreciate it!",
    "I love seeing posts like this. Keep it up!",
    "Wow, this blew my mind! Never looked at it this way before.",
    "Great discussion going on here. Loving the different perspectives!"
]

for _ in range(15):  # Create 15 random comments
    commenter = random.choice(users)
    post = random.choice(posts)
    comment_id = str(uuid.uuid4())
    comment_text = random.choice(comment_texts)  # Pick a random comment

    query = """
    MATCH (p:Post {post_id: $post_id}), (u:User {user_id: $user_id})
    CREATE (c:Comment {comment_id: $comment_id, content: $content, comment_created_at: datetime()})
    CREATE (p)-[:CONTAINS]->(c)
    CREATE (u)-[:WRITES]->(c)
    """
    db.run_query(query, {
        "post_id": post["post_id"], 
        "user_id": commenter["user_id"], 
        "comment_id": comment_id, 
        "content": comment_text
    })


# Create friendships between users (Follow relationships)
for _ in range(20):  # Create 20 random follow relationships
    user1, user2 = random.sample(users, 2)  # Pick two different users

    query = """
    MATCH (u1:User {user_id: $user1_id}), (u2:User {user_id: $user2_id})
    CREATE (u1)-[:FOLLOWS]->(u2)
    """
    db.run_query(query, {"user1_id": user1["user_id"], "user2_id": user2["user_id"]})

db.close()  # Close the database connection after all operations are done
print("Data creation complete!")
print("Dummy data inserted successfully!")

