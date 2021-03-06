'''
8 puzzle problem, a smaller version of the fifteen puzzle:
http://en.wikipedia.org/wiki/Fifteen_puzzle
States are defined as string representations of the pieces on the puzzle.
Actions denote what piece will be moved to the empty space.

States must allways be inmutable. We will use strings, but internally most of
the time we will convert those strings to lists, which are easier to handle.
For example, the state (string):

'1-2-3
 4-5-6
 7-8-e'

will become (in lists):

[['1', '2', '3'],
 ['4', '5', '6'],
 ['7', '8', 'e']]

'''

from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import WebViewer


INITIAL = '''4-5-1
8-3-7
e-6-2'''

GOAL = '''1-2-3
4-5-6
7-8-e'''


def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])


def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]


def find_location(rows, element_to_find):
    '''Find the location of a piece in the puzzle.
       Returns a tuple: row, column'''
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic


# we create a cache for the goal position of each piece, so we don't have to
# recalculate them every time
goal_positions = {}
rows_goal = string_to_list(GOAL)
for number in '12345678e':
    goal_positions[number] = find_location(rows_goal, number)


class EigthPuzzleProblem(SearchProblem):
    def actions(self, state):
        '''Returns a list of the numbers we can move to the empty space.'''
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')

        deltas = (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        )

        actions = []
        for d_row, d_col in deltas:
            new_row = row_e + d_row
            new_col = col_e + d_col
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                actions.append(rows[new_row][new_col])

        return actions

    def result(self, state, action):
        '''Return the resulting state after moving a piece to the empty space.
           (the "action" parameter contains the number to move)
        '''
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')
        row_n, col_n = find_location(rows, action)

        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]

        return list_to_string(rows)

    def is_goal(self, state):
        '''Returns true if a state is the goal state.'''
        return state == GOAL

    def cost(self, state1, action, state2):
        '''Returns the cost of performing an action. No useful on this problem, i
           but needed.
        '''
        return 1

    def heuristic(self, state):
        '''Returns an *estimation* of the distance from a state to the goal.
           We are using the manhattan distance.
        '''
        rows = string_to_list(state)

        distance = 0

        for number in '12345678e':
            row_n, col_n = find_location(rows, number)
            row_n_goal, col_n_goal = goal_positions[number]

            distance += abs(row_n - row_n_goal) + abs(col_n - col_n_goal)

        return distance


result = astar(EigthPuzzleProblem(INITIAL))
#result = astar(EigthPuzzleProblem(INITIAL), viewer=WebViewer())

for action, state in result.path():
    print 'Move number', action
    print state
