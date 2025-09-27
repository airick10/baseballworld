from flask import Blueprint, render_template, request, abort, current_app
from .services import load_hitters, load_pitchers, load_people, get_person, compute_short_pos, positions, sort_people



main = Blueprint("main", __name__)

@main.route("/")
def index():
    #return "<h1>Using Blueprint</h1>"
    return render_template("index.html")
    
@main.route("/all")
def all_people():
    people = load_people()
    return render_template("all_people.html", people=people)

@main.route("/hit_stats")
def hit_stats():
    stat = request.args.get("stat")
    if not stat:
        stat = "_id"
    people = load_people()
    people = sort_people(stat, people)
    return render_template("hit_stats.html", people=people)

@main.route("/pit_stats")
def pit_stats():
    stat = request.args.get("stat")
    if not stat:
        stat = "_id"
    people = load_people()
    people = sort_people(stat, people)
    return render_template("pit_stats.html", people=people)

@main.route("/hit_strat")
def hit_strat():
    stat = request.args.get("stat")
    if not stat:
        stat = "_id"
    people = load_people()
    people = sort_people(stat, people)
    return render_template("hit_strat.html", people=people)

@main.route("/pit_strat")
def pit_strat():
    stat = request.args.get("stat")
    if not stat:
        stat = "_id"
    people = load_people()
    people = sort_people(stat, people)
    return render_template("pit_strat.html", people=people)

@main.route("/playerpage")
def playerpage():
    kind = request.args.get("kind")
    pid  = request.args.get("id")
    if not kind or not pid:
        abort(404)
    person = get_person(kind, pid)
    if not person:
        abort(404)
    short = compute_short_pos(kind, person)   # derive from JSON fields
    position = positions(short)
    return render_template("playerpagefull.html", person=person, kind=kind, pid=pid, position=position)

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
    short = compute_short_pos(kind, person)   # derive from JSON fields
    position = positions(short)
    return render_template("playerpagefull.html", person=person, kind=kind, pid=pid, position=position)


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
