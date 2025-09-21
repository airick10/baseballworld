from flask import Blueprint, render_template, request, abort, current_app
from .services import load_hitters, load_pitchers, load_people, get_person



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

@main.route("/all")
def all_people():
    people = load_people()
    return render_template("all_people.html", people=people)

@main.route("/playerpage")
def playerpage():
    kind = request.args.get("kind")
    pid  = request.args.get("id")
    if not kind or not pid:
        abort(404)
    person = get_person(kind, pid)
    if not person:
        abort(404)
    return render_template("playerpage.html", person=person, kind=kind, pid=pid)

# If you want the POST “Full” button to work for both kinds:
@main.route("/playerpagefull", methods=["POST"])
def playerpagefull():
    kind = request.form.get("kind")
    pid  = request.form.get("id")
    if not kind or not pid:
        abort(400)
    person = get_person(kind, pid)
    if not person:
        abort(404)
    return render_template("playerpagefull.html", person=person, kind=kind, pid=pid)


'''
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
'''
