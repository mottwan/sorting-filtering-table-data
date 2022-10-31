import logging
import os
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

LOGGER = logging.getLogger(__name__)

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from config.test_data import TestData
from config.utils import (capture_screenshot,
                          set_screenshot_name,
                          inject_screenshot_into_html,
                          append_extras)

os.environ['WDM_LOG_LEVEL'] = '0'
os.environ["WDM_LOCAL"] = '1'


@pytest.fixture(params=["chrome"], scope='class')
def init_driver(request):
    global driver
    LOGGER.info('web driver initialization {}'.format(request.param))
    if request.param is None or request.param == "chrome":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    if request.param == "firefox":
        driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
    LOGGER.info('opening url {}'.format(TestData.BASE_URL))
    driver.get(TestData.BASE_URL)
    request.cls.driver = driver
    yield
    driver.close()
    driver.quit()
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    setattr(report, "duration_formatter", "%H:%M:%S.%f")
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = set_screenshot_name(report)
            capture_screenshot(driver, file_name)
            if file_name:
                html = inject_screenshot_into_html(TestData.SCREENSHOTS_FROM_REPORTS_PATH.format(file_name))
                append_extras(extra, pytest_html.extras.url(TestData.BASE_URL), pytest_html.extras.html(html))
        report.extra = extra

    if report.when == 'teardown':
        LOGGER.info('Generating HTML Report in following folder {}'.format(TestData.REPORTS_DIR))


def pytest_html_report_title(report):
    report.title = "Swag Labs Python Test Automation!"
