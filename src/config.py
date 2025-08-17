# src/config.py
import os
import configparser
from dotenv import load_dotenv

# --- Project Root and .env Loading ---
project_root = os.path.join(os.path.dirname(__file__), '..')
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

# --- INI Configuration ---
config = configparser.ConfigParser()
config_path = os.path.join(project_root, 'config.ini')
config.read(config_path)

# --- Scraping Parameters ---
TARGET_SUBREDDITS = config.get('reddit', 'target_subreddits').split(',')
POST_LIMIT = config.getint('reddit', 'post_limit')
RETRY_ATTEMPTS = config.getint('scraper', 'retry_attempts')