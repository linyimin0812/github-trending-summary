import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
NTFY_TOPIC = os.getenv('NTFY_TOPIC', 'github-trending-daily')
NTFY_SERVER = os.getenv('NTFY_SERVER', 'https://ntfy.sh')

# GitHub Settings
GITHUB_TRENDING_URL = 'https://github.com/trending'
TRENDING_LANGUAGE = os.getenv('TRENDING_LANGUAGE', '')  # 空字符串表示所有语言
TRENDING_SINCE = 'daily'  # daily, weekly, monthly

# Database
DB_PATH = os.getenv('DB_PATH', 'data/trending.db')

# Analysis Settings
MAX_PROJECTS_PER_RUN = int(os.getenv('MAX_PROJECTS_PER_RUN', '3'))
MIN_STARS_THRESHOLD = int(os.getenv('MIN_STARS_THRESHOLD', '100'))