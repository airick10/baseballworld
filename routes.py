from flask import Blueprint, render_template, request, abort, current_app
from .services import load_hitters, load_pitchers, load_people, get_person, compute_short_pos, positions, sort_people, pos_player_pool
import random



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

@main.route("/position_pool")
def position_pool():
    people = load_people()
    var_c = pos_player_pool("C", people)
    var_1b = pos_player_pool("1B", people)
    var_2b = pos_player_pool("2B", people)
    var_3b = pos_player_pool("3B", people)
    var_ss = pos_player_pool("SS", people)
    var_lf = pos_player_pool("LF", people)
    var_cf = pos_player_pool("CF", people)
    var_rf = pos_player_pool("RF", people)
    var_sp = pos_player_pool("SP", people)
    var_rp = pos_player_pool("RP", people)
    
    return render_template("position_pool.html", people=people, var_c=var_c, var_1b=var_1b, var_2b=var_2b, var_ss=var_ss, var_3b=var_3b, var_lf=var_lf, var_cf=var_cf, var_rf=var_rf, var_sp=var_sp, var_rp=var_rp)

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
    k = random.randint(0, 1)
    return render_template("playerpagefull.html", person=person, kind=kind, pid=pid, position=position, rand=k)

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
    k = random.randint(0, 1)
    return render_template("playerpagefull.html", person=person, kind=kind, pid=pid, position=position, rand=k)


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
