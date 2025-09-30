from flask import Flask
import json
import random
from pathlib import Path
from functools import lru_cache
from operator import itemgetter
import requests

input_file_h = "https://filedn.com/limKzbrdG9qBWDCDLoyNoHF/files/alltimebatters.json"
input_file_p = "https://filedn.com/limKzbrdG9qBWDCDLoyNoHF/files/alltimepitchers.json"

def _read_json(src: str):
    if src.startswith("http://") or src.startswith("https://"):
        resp = requests.get(src, timeout=10)
        resp.raise_for_status()
        return resp.json()
    p = Path(__file__).with_name(src)
    with p.open(encoding="utf-8") as f:
        return json.load(f)

def _index_by_id(seq):
    """
    Convert a list of records to a dict keyed by 'ID' (string).
    Ignores items that don't have an ID.
    """
    out = {}
    for rec in seq:
        # try common keys; adjust if your JSON uses a different one
        _id = rec.get("ID") or rec.get("_id") or rec.get("id")
        if _id is None:
            continue
        out[str(_id)] = rec
    return out

def load_hitters():
    data = _read_json(input_file_h)  # likely a list
    return _index_by_id(data) if isinstance(data, list) else data

def load_pitchers():
    data = _read_json(input_file_p)  # likely a list
    return _index_by_id(data) if isinstance(data, list) else data


def load_people():
    """Combine hitters and pitchers into a single sorted LIST."""
    hitters = load_hitters()
    pitchers = load_pitchers()

    people = []
    for _id, h in hitters.items():
        pos = h.get("s_fielding", "").split("-")[0].upper()
        if pos == "":
            pos = "DH"
        people.append({
            "kind": "hitter",
            "short_pos": pos,
            "id": _id,                 # keep as string to match your dict keys
            **h
        })
    for _id, p in pitchers.items():
        pos = p.get("s_endurance", "").split("(")[0].strip().upper()
        pos = pos+"P"
        people.append({
            "kind": "pitcher",
            "short_pos": pos,
            "id": _id,
            **p
        })

    # Sort by LastName then FirstName; missing keys fall back to ""
    people.sort(key=lambda r: (r.get("LastName", ""), r.get("FirstName", "")))
    return people

def get_person(kind: str, _id: str):
    """Lookup helper for detail pages."""
    if kind == "hitter":
        return load_hitters().get(_id)
    if kind == "pitcher":
        return load_pitchers().get(_id)
    return None

def compute_short_pos(kind: str, person: dict) -> str:
    if kind == "hitter":
        # e.g., "SS-2B" -> "SS"
        return person.get("s_fielding", "").split("-")[0].strip().upper()
    if kind == "pitcher":
        # e.g., "SP(7)" -> "SP"
        return person.get("s_endurance", "").split("(")[0].strip().upper()
    return ""


def positions(fielding: str):
    match fielding:
        case "C":
            return "Catcher"
        case "1B":
            return "First Baseman"
        case "2B":
            return "Second Baseman"
        case "SS":
            return "Shortstop"
        case "3B":
            return "Third Baseman"
        case "LF":
            return "Left Fielder"
        case "CF":
            return "Center Fielder"
        case "RF":
            return "Right Fielder"
        case "S":
            return "Starting Pitcher"
        case "R":
            return "Relief Pitcher"
        case "C":
            return "Closing Pitcher"
        case _:
            return "Designated Hitter"

def sort_people(stat: str, people: dict):

    if (stat != "p_earned_run_avg" and stat != "p_whip" and stat != "p_bb_per_nine"):
        people.sort(key=lambda r: float(r.get(stat, 0) or 0), reverse=True)
    else:
        people.sort(key=lambda r: float(r.get(stat, 0) or 0))

    return people

def pos_player_pool(pos: str, people: list[dict]) -> list[dict]:
    # filter down to just this position
    pool_temp = [h for h in people if h.get("short_pos") == pos]

    # how many to take (20%)
    num_players = round(len(pool_temp) * 0.2)

    # pick random unique players
    pool = random.sample(pool_temp, k=num_players) if num_players > 0 else []

    return pool