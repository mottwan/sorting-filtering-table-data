import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from config.test_data import TestData

LOGGER = logging.getLogger(__name__)


class BasePage(object):
    def __init__(self, driver, base_url=TestData.BASE_URL):
        self.base_url = base_url
        self.driver = driver
        self.timeout = 10

    def select_by_value(self, select_field, value):
        # LOGGER.info('select_by_value({}) {}'.format(select_field, bool(self.find_element(*select_field))))
        select = Select(self.driver.find_element(*select_field))
        return select.select_by_value(value)

    def check_page_loaded(self, *locator):
        # LOGGER.info('check_page_loaded({}) {}'.format(locator, bool(self.find_element(*locator))))
        self.wait_element(*locator)
        return bool(self.find_element(*locator))

    def find_element(self, *locator):
        # LOGGER.info('find_element({})'.format(locator))
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        # LOGGER.info('find_elements({})'.format(locator))
        return self.driver.find_elements(*locator)

    def refresh_page(self):
        return self.driver.refresh()

    def wait_element(self, *locator):
        try:
            WebDriverWait(self.driver, self.timeout).until(ec.presence_of_element_located(locator))
        except TimeoutException:
            LOGGER.error("\n * ELEMENT NOT FOUND WITHIN GIVEN TIME! --> %s\n%s" % (locator[1], TimeoutException))
            self.driver.quit()
