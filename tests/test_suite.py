import logging

from config.helpers import custom_sort
from config.helpers import convert_str_to_float
from config.helpers import key_func
from config.helpers import generate_random_keyword
from config.helpers import generate_random_number
from config.helpers import compute_expected_number_of_table_rows
from config.helpers import list_of_strings_to_float
from config.helpers import get_number_of_rows_duplicates
from config.helpers import remove_duplicated_values
from tests.base_test import BaseTest


LOGGER = logging.getLogger(__name__)


class TestSuite(BaseTest):

    def test_sorting_by_complexity_column(self):
        """
            This test case validates that the table data filters by known values from "Complexity" column
        """
        complexity = self.statistics_page().get_table_headers()[3]

        complexity_value_list = self.statistics_page().get_column_values(complexity)
        sorted_complexity_list = self.statistics_page().sorts_data_by(complexity)
        complexity_value_list = custom_sort(complexity_value_list)
        assert complexity_value_list == sorted_complexity_list

    def test_sorting_by_impact_score_column(self):
        """
            This test case validates that the table data filters by known values from "Average Impact Score" column
        """
        impact_score = self.statistics_page().get_table_headers()[2]

        impact_score_value_list = self.statistics_page().get_column_values(impact_score)
        sorted_impact_score_list = self.statistics_page().sorts_data_by(impact_score)
        impact_score_value_list = convert_str_to_float(impact_score_value_list)
        sorted_impact_score_list = convert_str_to_float(sorted_impact_score_list)
        impact_score_value_list.sort()
        assert impact_score_value_list == sorted_impact_score_list

    def test_sorting_by_number_of_cases_column(self):
        """
            This test case validates that the table data filters by known values from "Number Of Cases" column
        """
        number_of_cases = self.statistics_page().get_table_headers()[1]

        number_of_cases_value_list = self.statistics_page().get_column_values(number_of_cases)
        sorted_number_of_cases_list = self.statistics_page().sorts_data_by(number_of_cases)
        number_of_cases_value_list = list_of_strings_to_float(number_of_cases_value_list)
        sorted_number_of_cases_list = list_of_strings_to_float(sorted_number_of_cases_list)
        number_of_cases_value_list.sort()
        assert number_of_cases_value_list == sorted_number_of_cases_list

    def test_sorting_by_name_column(self):
        """
            This test case validates that the table data filters by known values from "Name" column
        """
        name = self.statistics_page().get_table_headers()[0]

        name_value_list = self.statistics_page().get_column_values(name)
        sorted_name_list = self.statistics_page().sorts_data_by(name)
        sorted_name_list = sorted(sorted_name_list, key=key_func)
        name_value_list.sort()
        assert name_value_list == sorted_name_list

    def test_filter_data_by_complexity_levels(self):
        """
            This test case validates that the table data filters by known values from "Complexity" column
        """
        column = 'complexity'

        complexity_value_list = self.statistics_page().get_column_values(column)
        keywords = remove_duplicated_values(complexity_value_list)
        expected_number_of_rows = get_number_of_rows_duplicates(complexity_value_list)
        table_headers = self.statistics_page().get_table_headers()
        index = table_headers.index(column)

        for keyword in keywords:
            table_rows = self.statistics_page().filters_data_by(keyword)
            complexity_column_values = self.statistics_page().get_column_values(column)

            for row_value in complexity_column_values:
                assert row_value == keyword
            assert len(table_rows[index]) == expected_number_of_rows[keyword]

    def test_filter_data_by_names(self):
        """
            This test case validates that the table data filters by known values from "Name" column
        """

        column = 'name'
        keywords = self.statistics_page().get_column_values(column)
        table_headers = self.statistics_page().get_table_headers()
        index = table_headers.index(column)
        expected_number_of_displayed_rows = 1

        for keyword in keywords:
            filtered_table_data = self.statistics_page().filters_data_by(keyword.lower())
            values_of_name_column = self.statistics_page().get_column_values(column)

            for value_of_the_row in values_of_name_column:
                assert keyword == value_of_the_row
            assert len(filtered_table_data[index]) == expected_number_of_displayed_rows

    def test_filter_data_by_containing_random_keywords(self):
        """
            This test case validates that the table data filters by random keywords
        """

        keyword_list_length = 20
        random_keyword_length = generate_random_number(1, 2)
        self.statistics_page().refresh_page()
        full_table_data = self.statistics_page().get_table_rows()

        # Generates a list of random keywords for filtering data table
        keywords = [generate_random_keyword(random_keyword_length) for _ in range(keyword_list_length)]

        for keyword in keywords:
            self.statistics_page().refresh_page()
            filtered_table_data = self.statistics_page().filters_data_by(keyword)
            expected_number_of_table_rows = compute_expected_number_of_table_rows(full_table_data, keyword)
            for filtered_table_rows in filtered_table_data:
                assert len(filtered_table_rows) == expected_number_of_table_rows

    def test_filter_data_by_white_spaces(self):
        """
            This test case validates that the table data filters by white spaces
        """

        keywords = [' ', '  ']
        self.statistics_page().refresh_page()
        table_data_values = self.statistics_page().get_table_rows()
        for keyword in keywords:
            self.statistics_page().refresh_page()
            filtered_table_data = self.statistics_page().filters_data_by(keyword)
            expected_number_of_table_rows = compute_expected_number_of_table_rows(table_data_values, keyword)

            for filtered_table_rows in filtered_table_data:
                assert len(filtered_table_rows) == expected_number_of_table_rows

    def test_filter_data_by_number_of_cases(self):
        """
            This test case validates that the table data filters by white spaces
        """

        self.statistics_page().refresh_page()
        full_table_data = self.statistics_page().get_table_rows()
        expected_number_of_displayed_rows = 0

        for cases in full_table_data:
            self.statistics_page().refresh_page()
            filtered_table_data = self.statistics_page().filters_data_by(cases[1])

            for filtered_table_rows in filtered_table_data:
                assert len(filtered_table_rows) == expected_number_of_displayed_rows

    def test_filter_data_by_average_impact_score(self):
        """
            This test case validates that the table data filters by white spaces
        """
        column = 'averageImpact'
        keywords = self.statistics_page().get_column_values(column)
        self.statistics_page().refresh_page()
        expected_number_of_displayed_rows = 0
        for keyword in keywords:
            self.statistics_page().refresh_page()
            filtered_table_data = self.statistics_page().filters_data_by(keyword)

            for filtered_table_rows in filtered_table_data:
                assert len(filtered_table_rows) == expected_number_of_displayed_rows
