import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.join(ROOT_DIR, 'processing_result')

COUNT_TASK_EVENT_LOOP = 500
COUNT_EMIT_SONG_ITEMS = 1000
COUNT_EMIT_ARTIST_ITEMS = 100
COUNT_EMIT_MEMORY = 100
COUNT_EMIT_FILE_SIZE = 100
DEBUG = True

LOCALLY = False
TEST_MODE = True
