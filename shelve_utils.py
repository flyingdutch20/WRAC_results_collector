import shelve
import csv

import config

shelve_path = config.racebest_headers_shelve()

def output_shelve_as_csv():
    with open(shelve_path + ".csv", "w", newline="") as my_file:
        writer = csv.writer(my_file)
        with shelve.open(shelve_path) as db:
            key_list = list(db.keys())
            for key in key_list:
                line = db[key]
                writer.writerow(line)

def output_shelve_as_txt():
    with open(shelve_path + ".txt", "w") as my_file:
        with shelve.open(shelve_path) as db:
            key_list = list(db.keys())
            for key in key_list:
                line = db[key] + '\n'
                my_file.write(line)


def delete_shelve(shelve_path):
    pass

def delect_all_shelves(shelves_dir):
    pass