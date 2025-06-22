import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/about')
def about():
    return render_template('about.html', title="About Liza Tinku")

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