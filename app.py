from flask import Flask, render_template, request
from surf_alert import check_conditions
from dotenv import load_dotenv
from email_alert import send_email  

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True)
