
import random, time


def random_wait(min:int, max:int) -> None:
    """
    Wait randomly between min and max milliseconds
    """
    time.sleep(random.randint(min, max)/1000)

class Colors:
    BOLD = '\033[1m'
    OK = f'{BOLD}\033[92m'
    WARNING = f'{BOLD}\033[93m'
    ERROR = f'{BOLD}\033[91m'
    NORMAL = '\033[0m'

