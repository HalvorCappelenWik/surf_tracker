from flask import Flask, render_template, request
from surf_alert import check_conditions
from dotenv import load_dotenv
from email_alert import send_email  
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    # Read current votes
    with open("votes.json", "r") as f:
        votes = json.load(f)
    return render_template("index.html", result=None, vote_counts=votes)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/track", methods=["POST"])
def track():
    beach = request.form["beach"]
    min_wave = float(request.form["min_wave"])
    email = request.form.get("email")
    notify = request.form.get("notify") == "yes"

    result = check_conditions(beach, min_wave)


    if "Score" in result and "✅" in result and notify and email:
        subject = f"Surf Alert for {beach} 🌊"
        send_email(email, subject, result)

    return render_template("index.html", result=result)


import json

@app.route("/vote", methods=["POST"])
def vote():
    spot = request.form["spot"]

    # Read current votes
    with open("votes.json", "r") as f:
        votes = json.load(f)

    # Update count
    if spot in votes:
        votes[spot] += 1

    # Save back to file
    with open("votes.json", "w") as f:
        json.dump(votes, f)

    # Render the main page again, passing updated votes
    return render_template("index.html", 
                            result=None,
                            vote_message=f"Thanks for voting for {spot}!",
                            vote_counts=votes)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's port or default locally
    app.run(host="0.0.0.0", port=port)