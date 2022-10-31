import logging

import pytest

from pages.statistics_page import StatisticsPage

LOGGER = logging.getLogger(__name__)


@pytest.mark.usefixtures("init_driver")
class BaseTest:
    LOGGER.info('log something')

    def statistics_page(self):
        return StatisticsPage(self.driver)

