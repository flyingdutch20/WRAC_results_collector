import csv
import os
import fpdf
from datetime import date

import result
import config

fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts'))

output_path = config.output_dir()
today = date.today().strftime("%y-%m-%d")
basename = f"{output_path}/results-{today}"

if not os.path.exists(output_path):
    os.makedirs(output_path)

def output_as_csv(results):
    filename = basename + '.csv'
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = result.Result.fields()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for line in results:
            writer.writerow(line.to_dict())
        return filename

def output_as_pdf(results):
    filename = basename + '.pdf'
    pdf = fpdf.FPDF()
    pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", style="B", fname="NotoSans-Bold.ttf", uni=True)
    pdf.add_font("NotoSans", style="I", fname="NotoSans-Italic.ttf", uni=True)
    pdf.add_font("NotoSans", style="BI", fname="NotoSans-BoldItalic.ttf", uni=True)
    pdf.add_page()
    pdf.set_font('NotoSans', 'B', 16)
    for race in results:
        pdf.cell(0, 10, f"{race.date} - {race.event} - Winning time: {race.winningtime}", 0, 1)
        pdf.set_font('NotoSans', '', 12)
        for runner in race.runners:
            pdf.cell(0, 7, runner.textoutput, 0, 1)
    pdf.output(filename, 'F')
    return filename

def output_as_html_table(results):
    filename = basename + '.txt'
    with open(filename, mode='w', newline='') as text_file:
        for race in results:
            text_file.write(race.html_race_output())
    return filename