
import dotenv, os

try: LANGUAGE_MODEL = os.environ["LANGUAGE_MODEL"]
except: LANGUAGE_MODEL = dotenv.get_key(".env", "LANGUAGE_MODEL")
try: OPEN_AI_API_KEY = os.environ["OPEN_AI_API_KEY"]
except: OPEN_AI_API_KEY = dotenv.get_key(".env", "OPEN_AI_API_KEY")
try: TWITTER_USER_TAG = os.environ["TWITTER_USER_TAG"]
except: TWITTER_USER_TAG = dotenv.get_key(".env", "TWITTER_USER_TAG")
try: TWITTER_AUTH_COOKIE = os.environ["TWITTER_AUTH_COOKIE"]
except: TWITTER_AUTH_COOKIE = dotenv.get_key(".env", "TWITTER_AUTH_COOKIE")
