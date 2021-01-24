from selenium import webdriver
#   from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
#   from selenium.webdriver.support import expected_conditions as EC
#   from selenium.webdriver.support.select import Select
import re
from sys import platform
import logging


logger = logging.getLogger("Placepot.tote")


class PPNag:
    name = ""
    result = ""
    placed = False
    bib = ""
    draw = ""
    pp_units = 0
    pp_percent = 0.0


class PPRace:
    leg = ""
    pool = 0.0
    remaining_units = 0
    fav_pp = 0
    fav_pp_perc = 0.0
    pp_nags = []


def hammer_it(driver, url):
    try:
        driver.get(url)
        result = WebDriverWait(driver, timeout=30, poll_frequency=5). \
            until(lambda d: d.find_element_by_xpath("//div[@data-testid='pool-result-page-multibet']"))
    except:
        result = None
    return result


def getpage_for_races(my_dict):
    pp_list = []
    if platform == 'linux' or platform == 'linux2':
        driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
    else:
        driver = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
#    driver = webdriver.Remote(desired_capabilities={"browserName": "chrome"})
    driver.get("https://tote.co.uk/results")
    WebDriverWait(driver, timeout=20, poll_frequency=1).\
        until(lambda d: d.find_element_by_xpath("//div[@data-testid='results']"))
    for url, leg in my_dict.items():
        repeat = 1
        result = None
        while result is None and repeat < 6:
            result = hammer_it(driver, url)
            logger.debug(f"Attempt {repeat} to get pp for leg {leg}")
            repeat += 1
        if result is not None:
            race = extract_pprace(result, leg, driver)
            pp_list.append(race)
    return pp_list


def extract_pprace(result, leg, driver):
    race = PPRace()
    race.leg = leg
    logger.info(f"Getting pp data for leg {leg}")
    poolsize = result.find_element_by_class_name("value")
    race.pool = poolsize.text if poolsize is not None else ""
    legdetails = WebDriverWait(driver, timeout=30, poll_frequency=5). \
        until(lambda d: d.find_element_by_xpath(f"//div[@data-testid='racecard-tab-{leg}']"))
    try:
        remaining_units = legdetails.find_element_by_xpath("div/ul")
        remaining_unit_list = remaining_units.find_elements_by_xpath("li")
        race.remaining_units = remaining_unit_list[leg].text if len(remaining_unit_list) >= leg else ""
    except:
        # No leg by leg data
        return None
    extract_placed_runners(legdetails, race)
    extract_other_runners(legdetails, race)
    return race


def extract_placed_runners(legdetails, race):
    placed_runners_div = legdetails.find_element_by_xpath("div[3]/div[2]")
    placed_runners_table = placed_runners_div.find_elements(By.CSS_SELECTOR, "li")
    for elm in placed_runners_table:
        nag = extract_runner(elm)
        nag.placed = True
        race.pp_nags.append(nag)


def extract_other_runners(legdetails, race):
    re_fav = re.compile("Unnamed Favourite")
    other_runners_div = legdetails.find_element_by_xpath("div[3]/div[3]")
    other_runners_table = other_runners_div.find_elements(By.CSS_SELECTOR, "li")
    for elm in other_runners_table:
        if re.search(re_fav, elm.text):
            extract_fav(elm, race)
        else:
            nag = extract_runner(elm)
            nag.placed = False
            race.pp_nags.append(nag)
    #   if fav placed then extra table for other runners after unnamed fav and non-runners
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
    finally:
        return None


def extract_fav(elm, race):
    pp = elm.find_element_by_class_name("numerics")
    race.fav_pp = pp.find_element_by_class_name("number").text
    if race.fav_pp != 'Not backed':
        pp_percent = pp.find_element_by_class_name("perCent")
        race.fav_pp_perc = pp_percent.text if pp_percent is not None else None


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
