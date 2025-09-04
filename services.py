from flask import Flask
import json
from pathlib import Path
from functools import lru_cache

input_file = Path(__file__).with_name("https://filedn.com/limKzbrdG9qBWDCDLoyNoHF/files/alltimebatters.json")
input_file_p = Path(__file__).with_name("https://filedn.com/limKzbrdG9qBWDCDLoyNoHF/files/alltimepitchers.json")

def load_hitters():

    with open(input_file, encoding="utf-8") as json_file:
        parsed_json = json.load(json_file)

    extracted_data = {}
    for hitter in parsed_json:
        extracted_data[hitter["ID"]] = hitter
    return extracted_data

def load_pitchers():

    with open(input_file_p, encoding="utf-8") as json_file:
        parsed_json = json.load(json_file)

    extracted_data = {}
    for pitcher in parsed_json:
        extracted_data[pitcher["ID"]] = pitcher
    return extracted_data
