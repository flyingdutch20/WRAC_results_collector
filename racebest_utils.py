import shelve
import uuid

import config


shelve_path = config.racebest_headers_shelve()

def store_header(fields):
    with shelve.open(shelve_path) as book:
        book[str(uuid.uuid1())] = fields

