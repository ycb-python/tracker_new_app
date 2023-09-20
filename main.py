from flask import Flask, jsonify
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from flask_cors import CORS
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

app = Flask(__name__)
CORS(app)

# def get_chrome_driver():
#     driver = uc.Chrome(headless=True)
#     return driver

def get_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = '/usr/bin/google-chrome'
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path= ChromeDriverManager().install(), options=chrome_options)

    return driver


def is_element_exists(driver, by, element):
    try:
        driver.find_element(
            by, element)
        return True
    except:
        return False


def search_case(driver, case_number):
    if is_element_exists(driver, By.CSS_SELECTOR, "#cvCaseNumber"):
        driver.find_element(By.CSS_SELECTOR, "#cvCaseNumber").send_keys(case_number)

    if is_element_exists(driver, By.CSS_SELECTOR, "input[value = 'SEARCH']"):
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value = 'SEARCH']"))))



def extract_information(driver):
    raw_data = ""
    if is_element_exists(driver, By.CSS_SELECTOR, ".Print"):
        raw_data = driver.find_element(By.CSS_SELECTOR, ".Print").text.replace("Case Information | Register Of Actions | FUTURE HEARINGS | PARTY INFORMATION | Documents Filed | Proceedings Held","").replace("Click here to access document images for this case","").replace("If this link fails, you may go to the Case Document Images site and search using the case number displayed on this page","")
    return raw_data

@app.route('/<case_number>', methods=['GET'])
def get_case_info(case_number):
    try:
        driver = get_chrome_driver()
        
        driver.get("https://www.lacourt.org/casesummary/ui/index.aspx?casetype=civil")
        search_case(driver, case_number)
        case_details = extract_information(driver)
        driver.quit()

        return jsonify(case_details)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
