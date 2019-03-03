from os.path import dirname, abspath, join

ROOT_DIR = abspath(dirname(__file__))
PROCESSING_DIR = join(ROOT_DIR, 'processing_result')
LOG_FOLDER = 'log'
LOG_FILE = 'log/log.txt'

COUNT_TASK_EVENT_LOOP = 500
COUNT_EMIT_ITEMS = 1000
COUNT_EMIT_MEMORY = 100
COUNT_EMIT_FILE_SIZE = 100
DEBUG = False

LOCALLY = False
TEST_MODE = False

