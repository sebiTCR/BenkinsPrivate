from colored import Fore, Back, Style


def debug(message, file=""):
    print(f'{Fore.grey_100}{Back.grey_15} DEBUG [{file}] {Style.reset} {message} ')


def info(message):
    print(f'{Fore.grey_100}{Back.blue_1} INFO {Style.reset} {message} ')


def warn(message):
    print(f'{Fore.grey_15}{Back.light_yellow} INFO {Style.reset} {message} ')


def error(message):
    print(f'{Fore.grey_100}{Back.red_3a} ERROR {Style.reset} {message} ')


def fatal(message):
    print(f'{Fore.grey_100}{Back.red_3a} FATAL {Style.reset} {message} ')
