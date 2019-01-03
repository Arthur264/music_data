from os.path import dirname, abspath, join

ROOT_DIR = abspath(dirname(__file__))
PROCESSING_DIR = join(ROOT_DIR, 'processing_result')

COUNT_TASK_EVENT_LOOP = 500
COUNT_EMIT_SONG_ITEMS = 1000
COUNT_EMIT_ARTIST_ITEMS = 100
COUNT_EMIT_MEMORY = 100
COUNT_EMIT_FILE_SIZE = 100
DEBUG = False

LOCALLY = False
TEST_MODE = False

