import os
import re
import string
import sys
import glob
import logging
import random
from datetime import datetime
from itertools import groupby

from config.conf_data import ConfData

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

LOGGER = logging.getLogger(__name__)


def set_driver_options(driver_opts):
    arguments = ['--no-sandbox', 'disable-infobars', '--disable-extensions', '--disable-gpu', '--disable-web-security']
    options = driver_opts
    for arg in arguments:
        options.add_argument(arg)
    return options


def capture_screenshot(driver, name):
    # from pytest_html_reporter import attach
    # attach(data=driver.get_screenshot_as_png())
    driver.get_screenshot_as_file(os.path.join(ConfData.ROOT_DIR, ConfData.SCREENSHOTS_DIR, name))


def set_screenshot_name(report):
    test_file = report.fspath.split('/')[1].split('.py')[0] + '_'
    class_and_function_names = report.location[2].replace('.', '_') + '__'
    timestamp = datetime.now().strftime("%d_%m_%Y__%H-%M-%S__%f")
    return test_file + class_and_function_names + timestamp + ".png"


def inject_screenshot_into_html(screenshot_dir):
    return f'<div><img src="%s" alt="screenshot" style="width:600px;height:228px;" ' \
           'onclick="window.open(this.src)" align="right"/></div>' % screenshot_dir


def append_extras(extra, *extra_types):
    return [extra.append(extra_type) for extra_type in extra_types]


def clean_up_screenshots_folder():
    screenshots = glob.glob(os.path.join(ConfData.ROOT_DIR, "reports", "screenshots", "*"))
    for screenshot in screenshots:
        os.remove(screenshot)


complexity_order = {
    'from': 'low',
    'to': 'high'
}


def custom_sort(value_list: list, reverse: bool = False):
    new_list: list = []
    for value in value_list:
        if complexity_order['from'] == value:
            new_list.insert(0, value)
    for value in value_list:
        if complexity_order['from'] != value and complexity_order['to'] != value:
            new_list.insert(len(new_list) + 1, value)
    for value in value_list:
        if complexity_order['to'] == value:
            new_list.insert(len(new_list) + 1, value)
    if reverse:
        new_list.reverse()
    return new_list


def convert_str_to_float(string_list: list):
    new_list = []
    for value in string_list:
        new_list.append(float(value))
    return new_list


def convert_short_number_to_long_number_string(value: str):
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000, 'custom': '{}0000'}

    if value[0].isdigit():
        if len(value) > 1:
            if '.' in value:
                if value[-1].lower() in ['k', 'm', 'b']:
                    return str(float(value.split('.')[0] + num_map.get('custom').format(value.split('.')[1][:-1])))
                else:
                    return str(float(value))
            else:
                if value[-1].lower() in ['k', 'm', 'b']:
                    return str(float(value[:-1]) * num_map.get(value[-1].upper(), 1))
                else:
                    return str(value)
        else:
            return str(float(value))
    else:
        return str(value)


def key_func(s):
    return [int(''.join(g)) if k else ''.join(g) for k, g in groupby(s, str.isdigit)]


def generate_random_number(from_length: int, to_length: int):
    return random.randint(from_length, to_length)


def generate_random_keyword(length: int = 3):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def convert_a_collection_to_string(params: list):
    unique_values = set()
    joined_string: str = ''

    for param in params:
        unique_values.add(param[0])
        unique_values.add(param[-1])
    for value in list(unique_values):
        joined_string = ''.join(value)

    return re.sub(r"\s+", "", joined_string.lower())


def compute_expected_number_of_table_rows(table: list, keyword):
    counter = 0
    for i in range(len(table)):
        for j in range(len(table[i])):
            value = table[i][j]
            if re.search(keyword, convert_short_number_to_long_number_string(value), re.IGNORECASE):
                counter = counter + 1
                break
    return counter


def list_of_strings_to_float(arr: list):
    return [float(convert_short_number_to_long_number_string(value)) for value in arr]


def get_number_of_rows_duplicates(column: list):
    return {i: column.count(i) for i in column}


def remove_duplicated_values(column_values: list):
    return list(set(column_values))
