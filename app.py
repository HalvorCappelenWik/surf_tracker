from flask import Flask, render_template, request
from surf_alert import check_conditions
from dotenv import load_dotenv



load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/track", methods=["POST"])
def track():
    beach = request.form["beach"]
    min_wave = float(request.form["min_wave"])
    
    result = check_conditions(beach, min_wave)  # This uses surf_alert.py
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
