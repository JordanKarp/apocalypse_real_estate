import os
from math import sqrt


def distance_coords(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distance_points(a, b):
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def proceed():
    input("Press enter to return to menu.")


def clear():
    """Clears the terminal display"""
    _ = os.system("cls") if os.name == "nt" else os.system("clear")


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


def pick_option(prompt, given_list):
    print(prompt)
    choice = input("--> ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(given_list):
            choice -= 1
            return given_list[choice]
        else:
            print("Invalid choice. Please try again.")
            return pick_option(prompt, given_list)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return pick_option(prompt, given_list)


def create_table(data, header=True, max_rows=None):
    """
    Creates a user-readable table from a list of lists or tuples.
    Allows optional row limit for large datasets.
    """
    if max_rows is not None:
        data = data[:max_rows]

    # Calculate the maximum width of each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

    # Create the table string
    table = ""
    for i, row in enumerate(data):
        row_str = " | ".join(
            f"{str(item).ljust(width)}" for item, width in zip(row, col_widths)
        )
        table += row_str + "\n"

        # Add a separator line after the header row, if header=True
        if header and i == 0:
            separator = "-+-".join("-" * width for width in col_widths)
            table += separator + "\n"

    return table.strip()


def list2d_get(lst, row, col, default=None):
    """
    Gets the value at the specified row and column in a 2D list,
    or returns a default value if the indices are out of range.

    Args:
        lst (list[list]): The 2D list to access.
        row (int): The row index to retrieve.
        col (int): The column index to retrieve.
        default: The value to return if the indices are out of range. Default is None.

    Returns:
        The value at the specified indices or the default value.
    """
    if 0 <= row < len(lst) and 0 <= col < len(lst[row]):
        return lst[row][col]
    return default


def extract_subgrid(data, row_start, row_end, col_start, col_end):
    """
    Extract a subgrid from a 2D list based on the given row and column boundaries.

    Parameters:
        data (list of list): The 2D list of data.
        row_start (int): The starting row index (inclusive).
        row_end (int): The ending row index (exclusive).
        col_start (int): The starting column index (inclusive).
        col_end (int): The ending column index (exclusive).

    Returns:
        list of list: A new 2D list containing the extracted subgrid.
    """
    return [row[col_start:col_end] for row in data[row_start:row_end]]
