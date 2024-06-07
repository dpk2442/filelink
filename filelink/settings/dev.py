from .base import *

DEBUG = True

TIME_ZONE = "America/Los_Angeles"

# Application settings

# Use .git folder as fallback for local testing
FL_FILES_PATH = Path(os.getenv("FL_FILES_PATH", "./.git")).resolve()
