import enum

class Colors(enum.Enum):
    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    WHITE = '\u001b[37m'

    END = '\u001b[0m'

class BackgroundColors(enum.Enum):
    BLACK = '\u001b[40m'
    RED = '\u001b[41m'
    GREEN = '\u001b[42m'
    YELLOW = '\u001b[43m'
    BLUE = '\u001b[44m'
    WHITE = '\u001b[47m'

    END = '\u001b[0m'

if __name__ == "__main__":
    print("Colors:")
    for color in Colors:
        print(f'\t{color.value}{color.name}{Colors.END.value}')

    print("BackgroundColors:")
    for color in BackgroundColors:
        print(f'\t{color.value}{color.name}{BackgroundColors.END.value}')