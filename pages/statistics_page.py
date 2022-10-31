from selenium.webdriver.common.by import By

from pages.base_page import BasePage
import logging

LOGGER = logging.getLogger(__name__)


class StatisticsPage(BasePage):

    FILTER_INPUT = 'filter-input'
    SORT_SELECT = 'sort-select'
    TABLE_HEADER = '//*[@class="table-header"]/*[@class="header__item"]/child::node()'
    TABLE_CELL = '//*[@class="table-content"]//*[contains(@class, "data-{}")]'
    TABLE_ROW = '//*[@class="table-content"]/*[@class="table-row"]'

    def __init__(self, driver):
        super().__init__(driver)

    def sorts_data_by(self, option: str):
        LOGGER.info('sorts_data_by("{}")'.format(option))
        self.select_by_value((By.ID, self.SORT_SELECT), option)
        return self.get_column_values(option)

    def filters_data_by(self, keyword: str):
        LOGGER.info('filters_data_by("{}")'.format(keyword))
        filter_input = self.find_element(By.ID, self.FILTER_INPUT)
        filter_input.clear()
        filter_input.send_keys(keyword)
        return self.__get_table_values()

    def get_table_headers(self):
        header_names: list = []
        elements = self.find_elements(By.XPATH, self.TABLE_HEADER)
        for element in elements:
            class_name = element.get_attribute('id')
            header_names.append(str(class_name).split('-')[1])
        return header_names

    def get_column_values(self, column_name: str):
        column_values: list = []
        elements = self.find_elements(By.XPATH, self.TABLE_CELL.format(column_name))
        for element in elements:
            column_values.append(element.text)
        return column_values

    def get_table_rows(self):
        return [element.text.splitlines() for element in self.find_elements(By.XPATH, self.TABLE_ROW)]

    def __get_table_values(self):
        table: list = []
        headers = self.get_table_headers()
        for header in headers:
            rows: list = []
            values = self.get_column_values(header)
            for value in values:
                rows.append(value)
            table.append(rows)
        return table
