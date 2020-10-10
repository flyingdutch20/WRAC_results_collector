from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

## for each race, create the tote results url;
## tote.co.uk/results/totecoursename/time(hh:mm)/placepot
def getpage(url):
#    options = Options()
    #    options.headless = True
    driver = webdriver.Chrome(executable_path="./drivers/chromedriver.exe")
#    driver = webdriver.Remote(desired_capabilities={"browserName": "chrome"})
    driver.get("https://tote.co.uk/results")
    result = WebDriverWait(driver, timeout=20, poll_frequency=1).until(lambda d: d.find_element_by_xpath("//div[@data-testid='results']"))
    print(result.text)
#    with webdriver.Chrome(executable_path="./drivers/chromedriver.exe", options=options) as driver:
#        wait = WebDriverWait(driver, 10)
#        driver.get("https://tote.co.uk/results")
#        wait = WebDriverWait(driver, 10)
    driver.get(url)
    result = WebDriverWait(driver, timeout=20, poll_frequency=1).\
        until(lambda d: d.find_element_by_xpath("//div[@data-testid='pool-result-page-multibet']"))
    poolsize = result.find_element_by_class_name("value")
    print(poolsize.text)
    legbuttons = result.find_elements_by_xpath("//li")
    button = legbuttons[0]
#    legdetails = WebDriverWait(driver, timeout=20, poll_frequency=1).\
#        until(lambda d: d.find_element_by_xpath("//div[@data-testid='racecard-tab-1']"))
    legdetails = result.find_element_by_xpath("//div[@data-testid='racecard-tab-1']")

    remaining_units = legdetails.find_element_by_xpath("div/ul")
    remaining_unit_list = remaining_units.find_elements_by_xpath("li")
    print(remaining_unit_list[1].text)

    placed_runners_div = legdetails.find_element_by_xpath("div[3]/div[2]")
    placed_runners_table = placed_runners_div.find_elements(By.CSS_SELECTOR, "li")

    print("*** Placed runners ***")

    for elm in placed_runners_table:
        print(elm.tag_name + " " + elm.text)

    print("*** Other runners ***")

    other_runners_div = legdetails.find_element_by_xpath("div[3]/div[3]")
    other_runners_table = other_runners_div.find_elements(By.CSS_SELECTOR, "li")

    print("******")
    for elm in other_runners_table:
        print(elm.tag_name + " " + elm.text)

    other_runners_div = legdetails.find_element_by_xpath("div[3]/div[4]")
    other_runners_table = other_runners_div.find_elements(By.CSS_SELECTOR, "li")


    for elm in other_runners_table:
        print(elm.tag_name + " " + elm.text)



getpage("https://tote.co.uk/results/hexham/12:25/placepot")