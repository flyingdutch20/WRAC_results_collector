from selenium import webdriver

# start server:
#
#   java -jar selenium-server-standalone-3.xxx -port 4444 -role hub
#   http://allselenium.info/execute-python-selenium-tests-in-selenium-grid/
#   java -jar selenium-server-4.0.0-alpha-6.jar standalone
#   java -jar selenium-server-4.0.0-alpha-6.jar hub
#   java -jar selenium-server-4.0.0-alpha-6.jar node --detect-drivers
#   curl -X POST -H "Content-Type: application/json" --data '{ "query": "{grid{uri}}" }' -s http://localhost:4444/graphql | jq .
#   https://www.selenium.dev/documentation/en/grid/grid_4/setting_up_your_own_grid/
#

desiredCapabilities={"browserName":"chrome"}

#driver = webdriver.Remote(
#   command_executor='http://127.0.0.1:4444/wd/hub',
#   desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True})

driver = webdriver.Remote(desired_capabilities = {"browserName":"chrome"})
driver.get("https://tote.co.uk/results")
driver.get("https://tote.co.uk/results/hexham/12:25/placepot")
print(driver.title)
driver.quit()