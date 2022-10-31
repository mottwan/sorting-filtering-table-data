import os
import platform
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


def get_executable_file_path_for(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '../resources/{}/{}'.format(platform.system(), __executable_file_name(filename)))


def __executable_file_name(binary_file):
    return '{}.exe'.format(binary_file) if platform.system() == 'Windows' else binary_file


class TestData:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')
    SCREENSHOTS_DIR = os.path.join(ROOT_DIR, 'reports', 'screenshots')
    SCREENSHOTS_FROM_REPORTS_PATH = "../screenshots/{}"
    SCREENSHOTS_FROM_ROOT_DIR_PATH = "../reports/screenshots/{}"
    CHROME_EXECUTABLE = get_executable_file_path_for("chromedriver")
    FIREFOX_EXECUTABLE = get_executable_file_path_for("geckodriver")
    FIREFOX_BINARY_FILE = '/Users/${USER}/Library/Application Support/Firefox/Profiles/*.default'
    BASE_URL = 'https://mystifying-beaver-ee03b5.netlify.app/'
