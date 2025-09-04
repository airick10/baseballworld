from flask import Blueprint, render_template, request, abort, current_app
from .services import load_hitters, load_pitchers



main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "<h1>Using Blueprint</h1>"

@main.route("/json")
def json():
    hitters = load_hitters()
    return render_template("json.html", hitters=hitters)

@main.route("/pitcherjson")
def pitcherjson():
    pitchers = load_pitchers()
    return render_template("pitcherjson.html", pitchers=pitchers)

@main.route("/playerpage")
def playerpage():
    hitter_id = request.args.get("hitter_id")
    if not hitter_id:
        abort(404)
    return render_template("playerpage.html", hitter_id=hitter_id)

@main.route("/playerpagefull", methods=["POST"])
def playerpagefull():
    hitter_id = request.form.get("hitter_id")
    if not hitter_id:
        abort(400)
    hitters = load_hitters()
    hitter = hitters.get(hitter_id)   # <-- no int()
    if not hitter:
        abort(404)
    return render_template("playerpagefull.html", hitter=hitter)
