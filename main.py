from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from db import *

def parse_line(full_name, date, address, time_zone):
    ret_dict = {'lines': {},
                    "planets_stroke": {},
                    "planets": {},
                    "houses": {},
                    'first_table': {},
                    'second_table': {},
                    "third_table": {}}

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=options)
    try:
        browser.get("https://astrostudiya.ru/horoscope-create/")
        sleep(0.5)
        # Send keys
        browser.find_element(By.XPATH, "/html/body/div[2]/section/div/div/form/div[1]/input").send_keys(full_name)
        browser.find_element(By.XPATH, "/html/body/div[2]/section/div/div/form/div[2]/input").send_keys(date)
        browser.find_element(By.CLASS_NAME, "ymaps-2-1-79-searchbox-input__input").send_keys(address)

        sleep(5)

        # Search Location
        input_search_btn = browser.find_element(By.XPATH,
                                                "/html/body/div[2]/section/div/div/form/div[3]/div[2]/ymaps/ymaps/ymaps/ymaps[4]/ymaps[1]/ymaps[1]/ymaps/ymaps[1]/ymaps/ymaps/ymaps/ymaps/ymaps[1]/ymaps/ymaps[2]/ymaps")
        input_search_btn.click()
        sleep(1)

        action = ActionChains(browser)

        # If address not Accurate
        variant = browser.find_element(By.XPATH,
                                        "/html/body/div[2]/section/div/div/form/div[3]/div[2]/ymaps/ymaps/ymaps/ymaps[4]/ymaps[1]/ymaps[1]/ymaps/ymaps[1]/ymaps/ymaps/ymaps/ymaps/ymaps[2]/ymaps/ymaps/ymaps[2]/ymaps/ymaps/ymaps[1]")

        if variant:
            action.move_to_element_with_offset(variant, 140, 10).click().perform()

        sleep(5)
        tail = browser.find_element(By.CLASS_NAME, "ymaps-2-1-79-balloon-overlay")

        action.move_to_element(tail).click().perform()

        # If We have time_zone
        if time_zone:
            browser.find_element(By.XPATH, '/html/body/div[2]/section/div/div/form/a').click()
            browser.find_element(By.ID, "checkutc").click()
            browser.find_element(By.ID, "utc").clear()
            browser.find_element(By.ID, "utc").send_keys("+" + time_zone)

        sleep(1)
        submit_btn = browser.find_element(By.XPATH, "/html/body/div[2]/section/div/div/form/div[7]/div/input[2]")

        action.move_to_element(submit_btn).click().perform()
        sleep(1)

        # ANOTHER PAGE
        tables = browser.find_elements(By.CLASS_NAME, "table-natal")

        # First table

        curr_table = browser.find_element(By.CLASS_NAME, "table-natal")

        all_tr = curr_table.find_elements(By.TAG_NAME, "tr")
        c_tr = 1
        for tr in all_tr:
            data = tr.text.split()
            key = 'row_' + str(c_tr)

            if len(data) == 4:
                ret_dict['first_table'].update({key: {"first": '',
                                                        'second': data[0],
                                                        'third': data[1],
                                                        'four': data[2],
                                                        'five': data[3]}})
            elif len(data) == 5:
                ret_dict['first_table'].update({key: {"first": data[0],
                                                        'second': data[1],
                                                        'third': data[2],
                                                        'four': data[3],
                                                        'five': data[4]}})

            c_tr += 1

        # Second, Third tables

        second_table = tables[1]
        second_all_tr = second_table.find_elements(By.TAG_NAME, "tr")

        third_table = tables[2]
        third_all_tr = third_table.find_elements(By.TAG_NAME, "tr")

        c_tr = 1
        for i in range(len(third_all_tr)):
            key = 'row_' + str(c_tr)
            if i != len(second_all_tr) and i < len(second_all_tr):
                second_table_tr = second_all_tr[i]
                data = second_table_tr.text.split()
                ret_dict['second_table'].update({key: {"first": data[0],
                                                        'second': data[1],
                                                        'third': data[2]}})

            third_table_tr = third_all_tr[i]
            data_third = third_table_tr.text.split()
            ret_dict['third_table'].update({key: {"first": data_third[0],
                                                    'second': data_third[1],
                                                    'third': data_third[2],
                                                    'four': data_third[3]}})
            c_tr += 1

        # Houses
        all_numbers = browser.find_element(By.ID, "housenumber").find_elements(By.TAG_NAME, "text")
        all_houses = browser.find_element(By.ID, "house").find_elements(By.TAG_NAME, "path")
        c_tr = 1
        for i in range(12):
            ret_dict['houses'].update({f'house_{c_tr}': {
                "line": all_houses[i].get_attribute('transform'),
                "sign": {
                    "num": all_numbers[i].find_element(By.TAG_NAME, "tspan").text,
                    "x": all_numbers[i].get_attribute("x"),
                    "y": all_numbers[i].get_attribute("y")
                }
            }})
            c_tr += 1

        # Planets
        c_tr = 1
        all_planets = browser.find_element(By.ID, "znak").find_elements(By.TAG_NAME, "text")
        for planet in all_planets:
            ret_dict['planets'].update({f'planet_{c_tr}': {
                "sign": planet.find_element(By.TAG_NAME, 'tspan').text,
                'x': planet.get_attribute("x"),
                'y': planet.get_attribute("y")
            }})
            c_tr += 1

        # Connections
        all_lines = browser.find_elements(By.TAG_NAME, "line")
        c_tr = 1
        for line in all_lines:
            ret_dict['lines'].update({f'line_{c_tr}': {
                'x1': line.get_attribute("x1"),
                'x2': line.get_attribute("x2"),
                'y1': line.get_attribute("y1"),
                'y2': line.get_attribute("y2"),
                'color': line.get_attribute('stroke'),
                'dasharray': line.get_attribute("stroke-dasharray"),
                'data-tippy-content': line.get_attribute('data-tippy-content')
            }})
            c_tr += 1

        all_strokes = browser.find_elements(By.TAG_NAME, "use")

        c_tr = 1
        for stroke in all_strokes:
            if stroke.get_attribute('class') == "show-aspekt":
                ret_dict['planets_stroke'].update({f'stroke_{c_tr}': {
                    'transform': stroke.get_attribute('transform')
                }})
                c_tr += 1

        browser.quit()
        return ret_dict
    except:
        return None

if __name__ == '__main__':
    while True:
        data = get_parse_data()
        for i in data:
            rez = None
            try:
                rez = parse_line(full_name=str(i[1]), date=str(i[2]), address=str(i[3]), time_zone=None)
            except:
                rez = parse_line(full_name=str(i[1]), date=str(i[2]), address=str(i[3]), time_zone=None)
            finally:
                if rez == None:
                    rez = {
                            'ERROR': {
                                'address': 'Неверный формат адресса',
                            }
                        } 
            add_rezult_data(id = i[0], rez=rez)
