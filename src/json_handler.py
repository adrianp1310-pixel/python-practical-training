import json
from pathlib import Path
from csv_handler import read_people


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def write_json(path, data, indent=2):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except OSError:
        return False


def csv_people_to_json(csv_path, json_path):
    reader = read_people(csv_path)
    if reader is None:
        return False
    return write_json(json_path, reader, indent=2)



def filter_json_by_field(path, field, value):
    reader = read_json(path)
    if reader is None:
        return None
    return [item for item in reader if item[field] == value]
