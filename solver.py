from collections import defaultdict


def load_input_from_file(path: str) -> tuple[dict, list]:
    """Procees input file to load the data

    Input file should contain 9 characters in 9 lines. Any non-space character
    is consider a gap if it is not a number 1-9.

    Args:
        path (str): Path to the input file

    Returns:
        tuple[dict, list]: First item is the actual map of coordinates. Each field
            contains a list of allowed numbers. The input numbers are just single
            element lists. Empty fields are lists of numbers from 1 to 9
    """
    fields = dict()
    starting_numbers = list()

    for row_number, line in enumerate(open(path, 'r')):
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

# Generate locations to quardant and sector to locations dictionaries
sectorss_locations = defaultdict(list)
sectors_names = dict()
for name, q in SECTORS_DEFINITIONS.items():
    x, y = q
    for i in range(x[0], x[2] + 1):
        for j in range(y[0], y[2] + 1):
            sectorss_locations[name].append((i, j))
            sectors_names[(i, j)] = name


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
    for loc in sectorss_locations[sector]:
        if loc != location and number in sudoku[loc]:
            sudoku[loc].remove(number)


def search_singles(visited: list) -> list[tuple]:
    """Sind in sudoku single numbers that were not visited yet.

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


def print_sudoku():
    """Print sudoku board in a nice away."""
    line = '\u2501' * 9
    t_shape = '\u2533'
    cross = '\u254b'
    rt_shape = '\u253b'

    top_line = '\u250f' + line + t_shape + line + t_shape + line + '\u2513'
    mid_line = '\u2523' + line + cross + line + cross + line + '\u252b'
    low_line = '\u2517' + line + rt_shape + line + rt_shape + line + '\u251b'

    old = ''
    end = '\033[0m'
    new = '\033[0;31m'

    print(top_line)
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print(mid_line)
        for j in range(9):
            if j % 3 == 0:
                print('\u2503', end='')

            number = sudoku.get((i, j))
            if (i, j) in starting_numbers:
                print(f' {old}{number[0]}{end} ' if len(number) == 1 else ' . ', end='')
            else:
                print(f' {new}{number[0]}{end} ' if len(number) == 1 else ' . ', end='')

        print('\u2503', end='')
        print()
    print(low_line)


sudoku, starting_numbers = load_input_from_file('input')
print_sudoku()

visited = []
single_numbers_locations = starting_numbers.copy()


while len(visited) <= 81:
    for single_number_location in single_numbers_locations:
        if single_number_location not in visited:
            visited.append(single_number_location)
            value = sudoku[single_number_location][0]
            exclude_lines(value, single_number_location)
            exclude_sectors(value, single_number_location)
            # check each sector for numbers 1..9 if the number appears once on the list it becomes the list
            # same for lines

    single_numbers_locations = search_singles(visited)
    if not single_numbers_locations:
        print('Loop ended - FOUND NOTHING')
        break

# print('Non single elements on the board:')
# [print(location, value) for location, value in sudoku.items() if len(value) != 1]

print_sudoku()
