import re
import os
import json

def get_acronym_match(expression_to_match_against):
    p = re.compile(r'[A-Z]*')
    m = p.search(expression_to_match_against)
    if m:
        return m.group()
    else:
        return None

def create_agency_acronym(audit_name):
    audit_name_word_list = audit_name.split()
    agency_acronym = ''
    for word in audit_name_word_list:
        m = get_acronym_match(word)
        if m:
            agency_acronym += m
    return agency_acronym

def get_audit_num_match(expression_to_match_against):
    p = re.compile(r'202[0-9]-[a-z0-9][a-z0-9][a-z0-9][a-z0-9]-[a-z0-9]*', re.IGNORECASE)
    m = p.search(expression_to_match_against)
    if m:
        return m.group()
    else:
        return None

def get_all_subdir(folder):
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    return subfolders

def read_json_config():
    py_dir = os.path.dirname(os.path.realpath(__file__))
    py_filename = r"\config.json"
    py_filepath = py_dir + py_filename
    with open(py_filepath, "r") as read_file:
        configurations = json.load(read_file)
        return configurations