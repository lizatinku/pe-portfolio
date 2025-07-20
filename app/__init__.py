import os
import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from playhouse.shortcuts import model_to_dict
from peewee import Model, CharField, TextField, DateTimeField, SqliteDatabase, MySQLDatabase

# Add this block to set up the database depending on environment
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

load_dotenv()

app = Flask(__name__)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

@app.route("/api/timeline_post", methods=["POST"])
def create_timeline_post():
    name = request.form.get("name")
    email = request.form.get("email")
    content = request.form.get("content")

    # Validation for missing name
    if not name or name.strip() == "":
        return "Invalid name", 400

    # Validation for missing or empty content
    if not content or content.strip() == "":
        return "Invalid content", 400

    # Validation for malformed email (very basic check)
    if not email or "@" not in email or "." not in email:
        return "Invalid email", 400

    post = TimelinePost.create(name=name, email=email, content=content)
    return jsonify({
        "id": post.id,
        "name": post.name,
        "email": post.email,
        "content": post.content,
        "created_at": post.created_at.isoformat()
    })

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Liza Tinku")

@app.route('/education')
def education():
    education = [
        {
            "degree": "B.S. Computer Engineering",
            "institution": "University of California, Davis",
            "date": "Sept 2022 – June 2026",
            "description": "Relevant coursework: Data Structures, Embedded Systems, Machine Learning",
            "courses": ["EEC 111", "EEC 180", "ECS 122A", "EEC 170"]
        },
        {
            "degree": "High School Diploma",
            "institution": "GEMS Westminster School, RAK, UAE",
            "date": "Sept 2018 – June 2022",
            "courses": ["A-Level Math", "A-Level Physics", "A Level Computer Science"]
        }
    ]
    return render_template("education.html", title="education")

@app.route('/experience')
def experience():
    experiences = [
        {
            "title": "Production Engineering/SRE Fellow",
            "date": "June 2025 – Present",
            "ongoing": True,
            "description": "Selected for the Meta and MLH Fellowship which has a 2.5% acceptance rate. Working on impactful projects under the guidance of Meta mentors.",
        },
        {
            "title": "Undergraduate Researcher",
            "date": "Sept 2024 – Present",
            "ongoing": True,
            "description": "Building ML models to predict Alzheimer's progression. Presented work at Northern California Undergraduate Research Symposium at SJSU.",
        },
        {
            "title": "Full-stack Developer(Freelance)",
            "date": "Dec 2024 – March 2025",
            "ongoing": False,
            "description": "Built a website using the MERN stack for a landscaping business. Implemented REST APIs in backend & designed frontend in React.js",
        },
        {
            "title": "SWE at AI Student Collective(AISC)",
            "date": "Oct 2024 - May 2025",
            "ongoing": False,
            "description": "Led frontend development for an AI-powered ASL translator. Designed UI in Figma and built using Next.js and Tailwind CSS.",
        },
        {
            "title": "Computer Room Consultant at UC Davis IET",
            "date": "Sept 2024 - Dec 2024",
            "ongoing": False,
            "description": "Provided Mac/Windows troubleshooting support for 100+ faculty and students. Ensured compliance with UC Davis policies.",
        },
        {
            "title": "ML Engineer at GDSC Club",
            "date": "Nov 2022 – March 2023",
            "ongoing": False,
            "description": "lt a flight price predictor using Python libraries. Learned the ML pipeline and evaluated model using ROC curves.",
        },

    ]
    return render_template("experience.html", experiences=experiences)

@app.route('/hobbies')
def hobbies():
    return render_template("hobbies.html", title="Hobbies")

@app.route('/travel')
def travel():
    return render_template("travel.html", title="Places I've Visited")

@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/api/timeline_post/<int:post_id>", methods=["DELETE"])
def delete_timeline_post(post_id):
    try:
        post = TimelinePost.get_by_id(post_id)
        post.delete_instance()
        return jsonify({"message": f"Post {post_id} deleted."})
    except TimelinePost.DoesNotExist:
        return jsonify({"error": "Post not found."}), 404
