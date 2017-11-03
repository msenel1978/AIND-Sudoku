
assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal units for Diagonal Sudoku
diagonal_units = [[rows[i] + cols[i] for i in range(len(rows))],\
                  [rows[::-1][i] + cols[i] for i in range(len(rows))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # display(values)

    # Boxes with two-digit values are potential naked twins
    potential_twins = [box for box in values
                       if (len(str(values[box])) == 2)]
    # Potential twins with equal values are naked twins
    naked_twins = [[box1,box2] for box1 in potential_twins
                   for box2 in peers[box1]
                   if values[box1] == values[box2] ]

    # Duplicates (A,B) and (B,A) both exist in the list
    # Remove duplicates by sorting the boxes in the list
    twins_sorted_within = [tuple(sorted(q)) for q in naked_twins]
    naked_twins_wo_dup = list(set(twins_sorted_within))

    # Go over the list and remove the digits from the peers
    for x in range(0, len(naked_twins_wo_dup)):
        [twin1, twin2] = naked_twins_wo_dup[x]
        # Find common peers of the naked twins (without duplicates)
        common_peers = set(peers[twin1]) & set(peers[twin2])

        #Remove the digits of the naked twins from the peers
        for digit in values[twin1]:
            dplaces = [box for box in common_peers if digit in values[box]]
            for y in range(0, len(dplaces)):
                assign_value(values, dplaces[y],\
                             values[dplaces[y]].replace(digit,''))
    #display(values)

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
        Returns:
            A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.abs
        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.abs

        Args:
            values: Sudoku in dictionary form

        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.
        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form
        Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys()
                                    if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys()
                                   if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys()
                if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values

    n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)

    if (solution):
        return solution
    else:
        return False

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
