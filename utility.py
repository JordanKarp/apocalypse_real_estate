import os


def clear():
    """Clears the terminal display"""
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


def colored(text, color):
    color_dict = {
        "black": "30",
        "red": "31",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "purple": "35",
        "cyan": "36",
        "white": "37",
        "bold": "1",
        "dim": "2",
        "italic": "3",
        "underline": "4",
    }
    color_val = color_dict.get(color, "38")
    return f"\033[{color_val}m{text}\033[00m"
