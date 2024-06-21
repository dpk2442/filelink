from .base import *

DEBUG = True

TIME_ZONE = "America/Los_Angeles"

# Application settings

# Use project folder as fallback for local testing
FL_FILES_PATH = Path(os.environ["FL_FILES_PATH"]).resolve() \
    if "FL_FILES_PATH" in os.environ else BASE_DIR
