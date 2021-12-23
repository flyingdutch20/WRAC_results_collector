import csv
import os

import result
import config

output_path = config.output_dir()

if not os.path.exists(output_path):
    os.makedirs(output_path)

def output_as_csv(results):
    with open(output_path + '/' + 'output.csv', mode='w', newline='') as csv_file:
        fieldnames = result.Result.fields()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for line in results:
            writer.writerow(line.to_dict())
