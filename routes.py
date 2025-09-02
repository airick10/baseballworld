from flask import Blueprint, render_template, request, abort, render_template
from .services import load_hitters



main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "<h1>Using Blueprint</h1>"

@main.route("/json")
def json():
    hitters = load_hitters()
    return render_template("json.html", hitters=hitters)

@main.route("/playerpage")
def playerpage():
    hitter_id = request.args.get("hitter_id")
    if not hitter_id:
        abort(404)
    return render_template("playerpage.html", hitter_id=hitter_id)