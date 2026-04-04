from colored import Fore, Back, Style


def debug(message):
    print(f'{Fore.grey_100} {Back.grey_15} DEBUG {Style.reset} {message} ')


def info(message):
    print(f'{Fore.grey_100}{Back.blue_1} INFO {Style.reset} {message} ')


def error(message):
    print(f'{Fore.grey_15}{Back.red_3a} ERROR {Style.reset} {message} ')


def fatal(message):
    print(f'{Fore.grey_100}{Back.red_3a} FATAL {Style.reset} {message} ')
