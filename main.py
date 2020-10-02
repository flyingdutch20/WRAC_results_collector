# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from urllib.request import urlopen
from bs4 import BeautifulSoup

def read_racingpost_index():
    html = urlopen("https://www.racingpost.com/racecards/")
    output = open("pages/racingpost_index.html", "wb")
    output.writelines(html.readlines())
    output.close()
    my_file = open("pages/racingpost_index.html").read()
    bs = BeautifulSoup(my_file, "html.parser")
    raw_meetings = bs.findAll("section", {"class":"ui-accordion__row"})
    print(len(raw_meetings))
    output.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_racingpost_index()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
