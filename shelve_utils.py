import shelve
import csv


def output_shelve_as_csv(shelve_path):
    with shelve.open(shelve_path) as db:
        key_list = list(db.keys())


def delete_shelve(shelve_path):
    pass

def delect_all_shelves(shelves_dir):
    pass