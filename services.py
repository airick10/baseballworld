from flask import Flask
import json
from pathlib import Path
from functools import lru_cache

input_file = Path(__file__).with_name("alltimebatters.json")

def load_hitters():

    with open(input_file, encoding="utf-8") as json_file:
        parsed_json = json.load(json_file)

    extracted_data = {}
    for hitter in parsed_json:
        extracted_data[hitter['ID']] = {
            'firstName': hitter['FirstName'],
            'lastName': hitter['LastName'],
            'team': hitter['s_team']
        }
    return extracted_data