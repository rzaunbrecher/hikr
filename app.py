import sys

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hikes.db")

# Create list of regions hikes can be in
regions = [
    "W. Slopes North",
    "E. Slopes North",
    "W. Slopes Central",
    "E. Slopes Central",
    "Stevens Pass",
    "Snoqualmie Pass",
    "Olympics",
    "W. Slopes South",
    "E. Slopes South"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dist_min = request.form.get("dist_min", type=float)
        dist_max = request.form.get("dist_max", type=float)
        if not dist_min or dist_min < 0:
            dist_min = 0
        if not dist_max or dist_max < 0:
            dist_max = sys.float_info.max

        elev_min = request.form.get("elev_min", type=float)
        elev_max = request.form.get("elev_max", type=float)
        if not elev_min or elev_min < 0:
            elev_min = 0
        if not elev_max or elev_max < 0:
            elev_max = sys.float_info.max

        region = request.form.get("region")
        dogs = request.form.get("dogs")
        if not region:
            if not dogs or dogs == "either":
                hikes = db.execute("SELECT * FROM hikes WHERE distance >= ? AND distance <= ? AND elevGAIN >= ? AND elevGAIN <= ?",
                                dist_min, dist_max, elev_min, elev_max)
            else:
                hikes = db.execute("SELECT * FROM hikes WHERE distance >= ? AND distance <= ? AND elevGAIN >= ? AND elevGAIN <= ? AND dogs=?",
                                   dist_min, dist_max, elev_min, elev_max, dogs)
            return render_template("index.html", regions=regions, hikes=hikes)
        else:
            if not dogs or dogs == "either":
                hikes = db.execute("SELECT * FROM hikes WHERE distance >= ? AND distance <= ? AND elevGAIN >= ? AND elevGAIN <= ? AND region = ?",
                                dist_min, dist_max, elev_min, elev_max, region)
            else:
                dogs = request.form.get("dogs")
                hikes = db.execute("SELECT * FROM hikes WHERE distance >= ? AND distance <= ? AND elevGAIN >= ? AND elevGAIN <= ? AND region = ? AND dogs=?",
                                dist_min, dist_max, elev_min, elev_max, region, dogs)
            return render_template("index.html", regions=regions, hikes=hikes)
    else:
        hikes = db.execute("SELECT * FROM hikes")
        return render_template("index.html", regions=regions, hikes=hikes)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        hike = request.form.get("name")
        if not hike:
            message = "Please enter a name for the hike"
            return render_template("/error.html", message=message)
        distance = request.form.get("distance", type=float)
        if not distance or distance < 0:
            message = "Please enter a valid distance"
            return render_template("/error.html", message=message)

        elevation = request.form.get("elevation", type=int)
        if not elevation or elevation < 0:
            message = "Please enter a valid elevation"
            return render_template("/error.html", message=message)

        region = request.form.get("region")
        if not region or region not in regions:
            message = "Please enter a valid region"
            return render_template("/error.html", message=message)

        dogs = request.form.get("dogs")
        if not dogs:
            dogs = "No"

        db.execute("INSERT INTO hikes (name, distance, elevGain, region, dogs) VALUES (?, ?, ?, ?, ?)", hike, distance, elevation, region, dogs)
        return redirect("/")

    else:
        return render_template("add.html", regions=regions)

@app.route("/delete", methods=["GET", "POST"])
def delete():
    # Delete hike
    id = request.form.get("id")
    db.execute("DELETE FROM hikes WHERE hikeID = ?", id)
    return redirect("/")
