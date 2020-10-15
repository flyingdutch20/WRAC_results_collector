from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import re

class PPNag():
    name = ""
    result = ""
    placed = False
    bib = ""
    draw = ""
    pp_units = 0
    pp_percent = 0.0

class PPRace():
    leg = ""
    pool = 0.0
    remaining_units = 0
    fav_pp = 0
    fav_pp_perc = 0.0
    pp_nags = []

def getpage_for_leg(url, leg):
    race = PPRace()
    race.leg = leg
    getpage_for_race(url, race)
    return race

def extract_runner(elm):
    nag = PPNag()
    nag.bib = elm.find_element_by_class_name("horse-number").text
    nag.draw = elm.find_element_by_class_name("gate-number").text
#    nag.result = elm.find_element_by_class_name("finishing-position").text
    nag.name = elm.find_element_by_class_name("horse-name").text
    pp = elm.find_element_by_class_name("numerics")
    nag.pp_units = pp.find_element_by_class_name("number").text
    if nag.pp_units != 'Not backed':
        pp_percent = pp.find_element_by_class_name("perCent")
        nag.pp_percent = pp_percent.text if pp_percent is not None else None
    return nag

def extract_fav(elm, race):
    pp = elm.find_element_by_class_name("numerics")
    race.fav_pp = pp.find_element_by_class_name("number").text
    race.fav_pp_perc = pp.find_element_by_class_name("perCent").text


def getpage_for_race(url, race):
#    options = Options()
    #    options.headless = True
    driver = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
#    driver = webdriver.Remote(desired_capabilities={"browserName": "chrome"})
    driver.get("https://tote.co.uk/results")
    result = WebDriverWait(driver, timeout=20, poll_frequency=1).until(lambda d: d.find_element_by_xpath("//div[@data-testid='results']"))
#    with webdriver.Chrome(executable_path="./drivers/chromedriver.exe", options=options) as driver:
#        wait = WebDriverWait(driver, 10)
#        driver.get("https://tote.co.uk/results")
#        wait = WebDriverWait(driver, 10)
    driver.get(url)
    result = WebDriverWait(driver, timeout=30, poll_frequency=5).\
        until(lambda d: d.find_element_by_xpath("//div[@data-testid='pool-result-page-multibet']"))
    poolsize = result.find_element_by_class_name("value")
    race.pool = poolsize.text if poolsize is not None else ""
    legdetails = result.find_element_by_xpath(f"//div[@data-testid='racecard-tab-{race.leg}']")

    try:
        remaining_units = legdetails.find_element_by_xpath("div/ul")
        remaining_unit_list = remaining_units.find_elements_by_xpath("li")
        race.remaining_units = remaining_unit_list[race.leg].text if len(remaining_unit_list) >= race.leg else ""
    except:
        # No leg by leg data
        return None

    placed_runners_div = legdetails.find_element_by_xpath("div[3]/div[2]")
    placed_runners_table = placed_runners_div.find_elements(By.CSS_SELECTOR, "li")

    for elm in placed_runners_table:
        nag = extract_runner(elm)
        nag.placed = True
        race.pp_nags.append(nag)

    other_runners_div = legdetails.find_element_by_xpath("div[3]/div[3]")
    other_runners_table = other_runners_div.find_elements(By.CSS_SELECTOR, "li")

    re_fav = re.compile("Unnamed Favourite")

    for elm in other_runners_table:
        if re.search(re_fav, elm.text):
            extract_fav(elm, race)
        else:
            nag = extract_runner(elm)
            nag.placed = False
            race.pp_nags.append(nag)

    try:
        other_runners_div = legdetails.find_element_by_xpath("div[3]/div[4]")
        other_runners_table = other_runners_div.find_elements(By.CSS_SELECTOR, "li")

        for elm in other_runners_table:
            if re.search(re_fav, elm.text):
                extract_fav(elm, race)
            else:
                nag = extract_runner(elm)
                nag.placed = False
                race.pp_nags.append(nag)
    except:
        None

