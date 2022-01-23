import shelve
import uuid

import config

def store_racebest_header(fields, yaml_file=None):
    if not isinstance(fields,list):
        raise TypeError
    shelve_path = config.racebest_headers_shelve(yaml_file)
    with shelve.open(shelve_path, flag='n') as book:
        book[str(uuid.uuid1())] = fields

def store_ukresults_header(fields, yaml_file=None):
    if not isinstance(fields,list):
        raise TypeError
    shelve_path = config.ukresults_headers_shelve(yaml_file)
    with shelve.open(shelve_path, flag='n') as book:
        book[str(uuid.uuid1())] = fields
