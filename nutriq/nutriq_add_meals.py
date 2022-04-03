import datetime
import json
import os
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from meal_components import Food, MatchType, MealType
from meal_components import Mealtime, get_meal_component_foods


DEFAULT_TIMEOUT = 3
BASE_URL = "https://client.nutri-q.com"


def get_driver(headless):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=options)
    return driver


def x(browser, xpath_string):
    return browser.find_element(By.XPATH, xpath_string)


def xs(browser, xpath_string):
    return browser.find_elements(By.XPATH, xpath_string)


def csss(browser, css_selector):
    return browser.find_elements(By.CSS_SELECTOR, css_selector)


def xs_contains(browser, attr=".", concat=True, *text_filters):
    xpath = ""
    for i in range(len(text_filters)):
        if i > 0:
            xpath = xpath + " and "
        if concat:
            xpath = xpath + "contains(concat(' '," + attr + ",' '),\" " \
                    + text_filters[i] + " \")"
        else:
            xpath = xpath + "contains(" + attr + \
                                      ",\"" + text_filters[i] + " \")"
    xpath = "//*[" + xpath + "]"
    return browser.find_elements(By.XPATH, xpath)


def wait(browser, xpath, *timeout):
    if len(timeout) == 0 or timeout[0] is None:
        use_timeout = 5
    else:
        use_timeout = timeout[0]
    WebDriverWait(browser, use_timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def get_month_string(month_index):
    if month_index == 1:
        return "January"
    elif month_index == 2:
        return "February"
    elif month_index == 3:
        return "March"
    elif month_index == 4:
        return "April"
    elif month_index == 5:
        return "May"
    elif month_index == 6:
        return "June"
    elif month_index == 7:
        return "July"
    elif month_index == 8:
        return "August"
    elif month_index == 9:
        return "September"
    elif month_index == 10:
        return "October"
    elif month_index == 11:
        return "November"
    elif month_index == 12:
        return "December"
    else:
        raise AssertionError("Invalid month")


def get_two_digit_int_string(integer):
    if integer < 10:
        return "0" + str(integer)
    else:
        return str(integer)


def get_date_range(startdate, *_enddate):
    if len(_enddate) == 0:
        enddate = startdate
    else:
        enddate = _enddate[0]
    if not isinstance(startdate, datetime.date) or not isinstance(startdate, datetime.date):
        raise AssertionError("Anchor date given was invalid")
    return [startdate + datetime.timedelta(days=x) for x in range((enddate - startdate).days)]


def connect_to_base(browser):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        creds_loc = os.path.join(base_dir, "creds.json")
        creds = json.load(open(creds_loc, 'r'))
    except Exception as e:
        traceback.print_exc()
        print("creds.json file not found in nutriq directory or invalid.")
        print("Credentials file should be in the format:")
        print("{\n\t\"username\": \"***\",\n\t\"password\": \"***\"\n}")
        return False
    if (not "username" in creds or not "password" in creds
            or creds["username"] == "" or creds["password"] == ""):
        print("Invalid username or password in creds.json.")
        print("Credentials file should be in the format:")
        print("{\n\t\"username\": \"***\",\n\t\"password\": \"***\"\n}")
        return False
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(BASE_URL)
            time.sleep(1)
            wait(browser, "//input[@type='email']")
            wait(browser, "//button[@type='submit']")
            login(browser, creds.get("username"), creds.get("password"))
            wait(browser, "//*[@id='sProClientNavLogSomething']")
            return True
        except Exception as e:
            traceback.print_exc()
            print(e)
            connection_attempts += 1
            print(f"Error connecting to {BASE_URL}.")
            print(f"Attempt #{connection_attempts}.")

    return False


def login(browser, username, password):
    x(browser, "//input[@type='email']").send_keys(username)
    x(browser, "//input[@type='password']").send_keys(password)
    x(browser, "//button[@type='submit']").click()


def set_date(browser, date):
    x(browser, "//*[contains(@class,'glyphicon-calendar')]/..").click()
    gridcell_xpath = "//td[@role='gridcell' and contains(@id,'datepicker')]"
    wait(browser, gridcell_xpath)
    month_str = get_month_string(date.month)
    month_xpath = "//button[contains(@id,'datepicker') and @role='heading']"
    if month_str not in x(browser, month_xpath).text:
        x(browser, month_xpath).click()
        monthcell_xpath = gridcell_xpath + \
            "//span[contains(.,'" + month_str + "')]"
        wait(browser, monthcell_xpath)
        if x(browser, monthcell_xpath + "/..").get_attribute("disabled") is not None:
            x(browser,
              "//*[contains(@class,'glyphicon-chevron-left')]/..").click()
            time.sleep(1)
        x(browser, monthcell_xpath).click()
    date_str = get_two_digit_int_string(date.day)
    datecell_xpath = gridcell_xpath + \
        "//span[not(contains(@class,'text-muted')) and contains(.,'" + date_str + "')]"
    wait(browser, datecell_xpath)
    x(browser, datecell_xpath).click()


def set_time(browser, mealtime):
    hours_string = get_two_digit_int_string(mealtime.hour)
    x(browser, "//input[@ng-model='hours']").click()
    x(browser, "//input[@ng-model='hours']").clear()
    x(browser, "//input[@ng-model='hours']").send_keys(hours_string)
    minutes_string = get_two_digit_int_string(mealtime.minute)
    x(browser, "//input[@ng-model='minutes']").click()
    x(browser, "//input[@ng-model='minutes']").clear()
    x(browser, "//input[@ng-model='minutes']").send_keys(minutes_string)
    current_meridian = x(
        browser, "//button[contains(@ng-class,'ToggleMeridian')]").text
    if not current_meridian == mealtime.meridian:
        x(browser, "//button[contains(@ng-class,'ToggleMeridian')]").click()


def get_time(browser) -> Mealtime:
    hours = int(
        x(browser, "//input[@ng-model='hours']").get_attribute("value"))
    minutes = int(
        x(browser, "//input[@ng-model='minutes']").get_attribute("value"))
    meridian = x(
        browser, "//button[contains(@ng-class,'ToggleMeridian')]").text
    return Mealtime(hours, minutes, meridian)


def _add_food_to_meal(browser, food, foods_added):
    # Try to avoid duplication
    for food_added in foods_added:
        if food_added.name == food.name:
            if food.quantity is None:
                if food_added.quantity is None or food_added.quantity >= 2:
                    print("Skipping duplicate food: " + food.name)
                    return
                else:
                    print("Duplicate food " + food.name
                          + " not skipped as quantity larger than pre-existing food quantity.")
            elif food_added.quantity >= food.quantity:
                print("Skipping duplicate food: " + food.name)
                return
            else:
                print("Duplicate food " + food.name
                      + " not skipped as quantity larger than pre-existing food quantity.")

    x(browser, "//input[@ng-model='searchFoodString']").send_keys(food.name)
    wait(browser, "//li[@role='option']")

    if food.prep_type is None:
        if food.match_type == MatchType.EXACT:
            x(browser, "//li[@role='option']//span[@class='ng-binding'][.='"
                + str(food.name) + "']").click()
        else:
            x(browser, "//li[@role='option']").click()
    elif food.match_type is None:
        x(browser, "//li[@role='option' and contains(.,'" + str(food.prep_type)
            + "')]").click()
    elif food.match_type == MatchType.EXACT:
        x(browser, "//li[@role='option' and contains(.,'" + str(food.prep_type)
            + "') and contains(.,'" + str(food.name) + ": ')]").click()

    wait(browser, "//option[@value='Regular']")
    if food.quantity is None:
        x(browser, "//option[@value='Regular'").click()
    else:
        x(browser, "//option[@value='"
          + food.get_quantity_string() + "']").click()

    foods_added.append(food)
    print("- " + food.name + " (" + food.get_quantity_string() + ")")


def set_meal_type(browser, mealtype):
    if mealtype is None or mealtype == "":
        mealtype = MealType.SNACK
    mealtype_xpath = "//select[@ng-model='mealType']/option[@value='" + \
        mealtype.value + "']"
    x(browser, mealtype_xpath).click()


def open_log_meal_page(browser):
    time.sleep(2)
    x(browser, "//*[@id='sProClientNavLogSomething']/a").click()
    x(browser, "//*[@href='./#/logMeal']").click()


def _log_meal(browser, date, mealtype, mealtime, auto_confirm, base_foods, extras):
    log_meal_url = BASE_URL + '/private/app/#/logMeal'
    if not browser.current_url == log_meal_url:
        open_log_meal_page(browser)
    wait(browser, "//*[@ng-model='pickedDate']")
    set_date(browser, date)
    if mealtime is None:
        mealtime = mealtype.get_standard_meal_time()
    set_time(browser, mealtime)
    set_meal_type(browser, mealtype)
    foods_added = []

    for food in base_foods:
        _add_food_to_meal(browser, food, foods_added)
    if extras is not None:
        for component in extras:
            if isinstance(component, Food):
                _add_food_to_meal(browser, component, foods_added)
            else:
                component_foods = get_meal_component_foods(component, mealtype)
                for food in component_foods:
                    _add_food_to_meal(browser, food, foods_added)

    if auto_confirm == 0:
        if mealtype is not None and mealtype.value != "":
            confirm = input("Confirm meal: \"" + mealtype.value + "\" (y/n): ")
        else:
            confirm = input("Confirm meal (y/n): ")
        if not confirm == "y":
            return
    elif auto_confirm == -1:
        wait(browser, "//button[contains(.,'View your log')]", 1000)
        x(browser, "(//button[contains(.,'Close')])[last()]").click()
        print("Meal confirmed: \"" + mealtype.value + "\"")
        return

    x(browser, "//button[contains(.,'Submit Meal')]").click()
    wait(browser, "//button[contains(.,'View your log')]")
    x(browser, "(//button[contains(.,'Close')])[last()]").click()


def log_meal(browser, date, mealtype: str, auto_confirm: int, extras: list):
    mealtype = MealType.fromValue(mealtype)
    base_foods = mealtype.get_base_foods()
    _log_meal(browser, date, mealtype, None, auto_confirm, base_foods, extras)


def log_unique_meal(browser, date, mealtime, auto_confirm, foods):
    _log_meal(browser, date, "", mealtime, auto_confirm, [], foods)
