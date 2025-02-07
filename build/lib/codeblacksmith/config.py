import os
from dotenv import load_dotenv

# Get absolute path to the project's root .env file
ROOT_ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env"))

# Load environment variables
load_dotenv(ROOT_ENV_PATH)

# Now, all environment variables will be available globally via os.getenv()