from flask import Flask
import json
from pathlib import Path
from functools import lru_cache
from operator import itemgetter

input_file_h = Path(__file__).with_name("alltimebatters.json")
input_file_p = Path(__file__).with_name("alltimepitchers.json")

def load_hitters():
    with input_file_h.open(encoding="utf-8") as f:
        parsed = json.load(f)
    # dict keyed by string ID (as in your JSON)
    return {h["ID"]: h for h in parsed}

def load_pitchers():
    with input_file_p.open(encoding="utf-8") as f:
        parsed = json.load(f)
    return {p["ID"]: p for p in parsed}

def load_people():
    """Combine hitters and pitchers into a single sorted LIST."""
    hitters = load_hitters()
    pitchers = load_pitchers()

    people = []
    for _id, h in hitters.items():
        people.append({
            "kind": "hitter",
            "id": _id,                 # keep as string to match your dict keys
            **h
        })
    for _id, p in pitchers.items():
        people.append({
            "kind": "pitcher",
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