from collections import defaultdict
import pathlib

# For colors in Windows terminal
if __import__("platform").system() == "Windows":
    kernel32 = __import__("ctypes").windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    del kernel32

# Use to generate locations for each sector
SECTORS_DEFINITIONS = {
    'NW': [(0, 1, 2), (0, 1, 2)],
    'N': [(0, 1, 2), (3, 4, 5)],
    'NE': [(0, 1, 2), (6, 7, 8)],
    'W': [(3, 4, 5), (0, 1, 2)],
    'C': [(3, 4, 5), (3, 4, 5)],
    'E': [(3, 4, 5), (6, 7, 8)],
    'SW': [(6, 7, 8), (0, 1, 2)],
    'S': [(6, 7, 8), (3, 4, 5)],
    'SE': [(6, 7, 8), (6, 7, 8)],
}


def make_sectors_dicts(sectors: dict) -> tuple[dict, dict]:
    """Generate locations to sector and sector to locations dictionaries

    Args:
        sectors (dict): Sectors definitions.

    Returns:
        tuple[dict, dict]: Two dictionaries. First one takes sector name and gives a
            list of locations, the other takes location and gives sector name.
    """
    sectors_locations = defaultdict(list)
    sectors_names = dict()
    for name, q in SECTORS_DEFINITIONS.items():
        x, y = q
        for i in range(x[0], x[2] + 1):
            for j in range(y[0], y[2] + 1):
                sectors_locations[name].append((i, j))
                sectors_names[(i, j)] = name
    return sectors_locations, sectors_names


def load_input_data(lines: list[str]) -> tuple[dict, list]:
    """Procees input file to load the data

    Input file should contain 9 characters in 9 lines. Any non-space character
    is consider a gap if it is not a number 1-9.

    Args:
        lines (list[str]): List of input lines.

    Returns:
        tuple[dict, list]: First item is the actual map of coordinates. Each field
            contains a list of allowed numbers. The input numbers are just single
            element lists. Empty fields are lists of numbers from 1 to 9
    """
    fields = dict()
    starting_numbers = list()

    for row_number, line in enumerate(lines):
        line = line.strip()

        if len(line) != 9:
            print(
                f'Incorrect line {row_number + 1}. '
                f'Expected 9 characters. Found {len(line)}'
            )
            exit()

        for colum_number, character in enumerate(line):
            if row_number > 8:
                print('Too many rows!')
                exit()

            if character.isdigit() and 0 < int(character) < 10:
                number = int(character)
                fields[(row_number, colum_number)] = [number]
                starting_numbers.append((row_number, colum_number))
            else:
                fields[(row_number, colum_number)] = list(range(1, 10))

    return fields, starting_numbers


def exclude_lines(number: int, location: tuple[int, int]):
    """Edit global sudoku. Excludes number present in lines.

    For each number all locations directly up, down, left, and right are checked and
    that number is removed from the list of possible numbers.

    Args:
        number (int): Number to remove from candidates lists.
        location (tuple[int, int]): Location of the investigated field.
    """
    global sudoku
    r, c = location
    for i in range(9):
        if i != r:
            if number in sudoku[(i, c)]:
                sudoku[(i, c)].remove(number)
        if i != c:
            if number in sudoku[(r, i)]:
                sudoku[(r, i)].remove(number)


def exclude_sectors(number: int, location: tuple[int, int]):
    """Edits global sudoku. Exclude numbers already present in a sector

    For each number, other locations in the sector have the number removed.

    Args:
        number (int): Number to remove from candidates lists.
        location (tuple[int, int]): Location of the investigated field.
    """
    global sudoku
    sector = sectors_names[location]
    for loc in sectors_locations[sector]:
        if loc != location and number in sudoku[loc]:
            sudoku[loc].remove(number)


def search_singles(visited: list) -> list[tuple]:
    """Find in sudoku single numbers that were not visited yet.

    Args:
        visited (list): List of visited locations.

    Returns:
        list(tuple): List of unvisited locations with just one number.
    """
    global sudoku
    singles = []
    for location, values in sudoku.items():
        if location not in visited:
            if len(values) == 1:
                singles.append(location)
    return singles


def print_sudoku(line_color: str = ''):
    """Print sudoku board in a nice away."""

    old = ''
    new = '\033[1;34m'  # Light blue
    end = '\033[0m'
    bg = '\u001b[30;1m'  # Gray

    ln = '\u2501' * 9  # Line
    ts = '\u2533'  # T-section
    cs = '\u254b'  # Cross
    rts = '\u253b'  # Reverse T-section

    top_line = line_color + '\u250f' + ln + ts + ln + ts + ln + '\u2513' + end
    mid_line = line_color + '\u2523' + ln + cs + ln + cs + ln + '\u252b' + end
    low_line = line_color + '\u2517' + ln + rts + ln + rts + ln + '\u251b' + end
    v_line = line_color + '\u2503' + end

    print(top_line)
    for i in range(9):
        # Horizontal lines lines
        if i % 3 == 0 and i != 0:
            print(mid_line)

        for j in range(9):
            # Vertical lines
            if j % 3 == 0:
                print(v_line, end='')

            number = sudoku.get((i, j))
            color = old if (i, j) in starting_numbers else new
            if len(number) == 1:
                print(f' {color}{number[0]}{end} ', end='')
            else:
                print(f'{bg} . {end}', end='')
        print(v_line)
    print(low_line)


def find_exclusive_locations(locations: list[tuple]):
    """Edits global sudoku. Looks for single location in a group containing a number.

    In a given group of location there might be a location that can have 2 or more
    candidate numbers, however if a given number appears only in one place in a group
    that place belongs to that number. Groups would be rows, columns, sectors

    Args:
        locations (list[tuple]): List of locations creating a group.
    """
    global sudoku
    for number in range(9):
        contain_number = []
        for location in locations:
            if number in sudoku[location]:
                contain_number.append(location)
        if len(contain_number) == 1:
            sudoku[contain_number[0]] = [number]


if __name__ == '__main__':
    # Load and show the data
    root_dir = pathlib.Path(__file__).resolve().parent
    input_files = [
        file for file in root_dir.iterdir()
        if file.stem.lower().startswith('sudoku') and file.suffix == '.txt'
    ]
    if not input_files:
        print('Found no input files. Their name should start with "sudoku" and be .txt')
        exit()

    # Ask user for a file number
    while True:
        print('Found the following input files:')
        [print(f'{num}: {file.stem}') for num, file in enumerate(input_files, start=1)]
        decision = input('Which file to load?: ')
        try:
            selected_number = int(decision)
        except ValueError:
            print('Incorrect choice.\n')
            # exit()
            continue
        if not (0 < selected_number <= len(input_files)):
            print('Wrong number!\n')
            # exit()
            continue
        break

    input_lines = open(input_files[selected_number - 1], 'r').readlines()
    sudoku, starting_numbers = load_input_data(input_lines)
    print_sudoku()

    # Prepare for solutions
    sectors_locations, sectors_names = make_sectors_dicts(SECTORS_DEFINITIONS)
    visited = []
    single_numbers_locations = starting_numbers.copy()

    # Actual solution
    cycles = 0
    while len(visited) <= 81:
        # Exclude neighbors for single numbers
        for single_number_location in single_numbers_locations:
            if single_number_location not in visited:
                visited.append(single_number_location)
                value = sudoku[single_number_location][0]
                exclude_lines(value, single_number_location)
                exclude_sectors(value, single_number_location)

        # Find exclusive locations in rows
        for row in range(9):
            locations = [loc for loc in sudoku.keys() if loc[0] == row]
            find_exclusive_locations(locations)

        # Find exclusive locations in columns
        for column in range(9):
            locations = [loc for loc in sudoku.keys() if loc[1] == column]
            find_exclusive_locations(locations)

        # Find exclusive locations in sections
        for sector in sectors_locations.values():
            find_exclusive_locations(sector)
        cycles += 1

        # Seacrch for non visited singles
        single_numbers_locations = search_singles(visited)
        if not single_numbers_locations:
            print(f'Finished after {cycles} cycles')
            break

    if len(visited) != 81:
        print('Could not find the solution')
        print_sudoku('\033[1;31m')
    else:
        print_sudoku()

    _ = input('Press [ENTER] to close the window')


"""  TODO:
Make sudoku board as a class so all operations on the board are methods.
When you reach the dead end generate a list of fields with only two choices.
Make a copy of the board - pick one choice. If fail pick another. If fail, go to another
bi-number location and repeat.
"""
