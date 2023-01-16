import copy
import logging
from datetime import datetime
from typing import (
    List,
    Union,
)

LOGGER = logging.getLogger(__name__)

T_SUDOKU_NODE = Union[int, None]
T_SUDOKU = List[List[T_SUDOKU_NODE]]
_TEST_DATA = [
    [4, 7, 9, None, 1, 2, None, None, None],
    [None, 3, None, 6, 7, None, None, 1, None],
    [1, None, 2, 9, None, None, 7, None, 4],

    [None, None, None, None, 4, None, 5, 6, 8],
    [6, 8, None, None, None, None, None, None, 2],
    [2, None, None, 8, 6, 3, None, 9, None],

    [3, 4, None, None, 8, None, 9, None, None],
    [None, 2, None, 4, None, None, 8, None, None],
    [8, None, 1, 5, 2, None, 4, None, None],
]
_TEST_SOLUTION = [
    [4, 7, 9, 3, 1, 2, 6, 8, 5],
    [5, 3, 8, 6, 7, 4, 2, 1, 9],
    [1, 6, 2, 9, 5, 8, 7, 3, 4],

    [9, 1, 3, 2, 4, 7, 5, 6, 8],
    [6, 8, 7, 1, 9, 5, 3, 4, 2],
    [2, 5, 4, 8, 6, 3, 1, 9, 7],

    [3, 4, 5, 7, 8, 1, 9, 2, 6],
    [7, 2, 6, 4, 3, 9, 8, 5, 1],
    [8, 9, 1, 5, 2, 6, 4, 7, 3],
]


class WrongSchemaError(Exception):
    ...


class CanNotSolveError(Exception):
    ...


class SudokuSolver:
    def __init__(self, data: T_SUDOKU):
        self._raw_data = copy.deepcopy(data)
        self.__check_data()
        self._solution = copy.deepcopy(self._raw_data)

    @property
    def solved(self) -> bool:
        """
        Is sudoku solved or not

        :return: Solved
        :rtype: bool
        """
        for row in self._solution:
            for item in row:
                if item is None:
                    return False
        return True

    def __check_data(self) -> None:
        """
        Check sudoku schema

        :return: None
        """
        try:
            assert type(self._raw_data) is list, 'Wrong data type'
            assert len(self._raw_data) == 9, 'Wrong column length'
            for row in self._raw_data:
                assert type(row) is list, 'Wrong data type'
                assert len(row) == 9, 'Wrong row length'
                for item in row:
                    assert (type(item) is int) or (item is None), 'Wrong data type'
                    if type(item) is int:
                        assert 1 <= item <= 9, f'Wrong number: {item}'
        except AssertionError as error:
            LOGGER.error('Wrong sudoku schema')
            LOGGER.exception(error)
            raise WrongSchemaError('Wrong sudoku schema') from error
        LOGGER.info('Raw data:\n' + '\n'.join([str(row) for row in self._raw_data]))

    def _change_number(self, row_index: int, column_index: int, value: int) -> None:
        """
        Change number in solution

        :param int row_index: Row index
        :param int column_index: Column index
        :param int value: New value

        :return: None
        """
        self._solution[row_index][column_index] = value
        LOGGER.info(f'Changed [{row_index}][{column_index}] None -> {value}')

    def _try_square(self, square_y: int, square_x: int) -> bool:
        """
        Try to solve in one square

        :param int square_y: Square y0
        :param int square_x: Square x0

        :return: Anything changed or not
        :rtype: bool
        """
        changed = False

        for number in range(1, 10):
            square_numbers = [
                self._solution[square_y][square_x:square_x + 3],
                self._solution[square_y + 1][square_x:square_x + 3],
                self._solution[square_y + 2][square_x:square_x + 3],
            ]
            if number not in [x for y in square_numbers for x in y]:
                # Options where the number can be
                number_options = [[True for _ in range(3)] for _ in range(3)]

                # Remove occupied places from options
                for i in range(3):
                    for j in range(3):
                        if square_numbers[i][j] is not None:
                            number_options[i][j] = False

                # Remove places impossible horizontally
                if number in self._solution[square_y]:
                    number_options[0] = [False] * 3
                if number in self._solution[square_y + 1]:
                    number_options[1] = [False] * 3
                if number in self._solution[square_y + 2]:
                    number_options[2] = [False] * 3

                # Remove places impossible vertically
                if number in [row[square_x] for row in self._solution]:
                    for i in range(3):
                        number_options[i][0] = False
                if number in [row[square_x + 1] for row in self._solution]:
                    for i in range(3):
                        number_options[i][1] = False
                if number in [row[square_x + 2] for row in self._solution]:
                    for i in range(3):
                        number_options[i][2] = False

                # Count options
                options = []
                for i in range(3):
                    for j in range(3):
                        if number_options[i][j] is True:
                            options.append((i, j))

                # If there is only one option - change None to number
                if len(options) == 1:
                    self._change_number(
                        row_index=square_y + options[0][0],
                        column_index=square_x + options[0][1],
                        value=number,
                    )
                    changed = True

        return changed

    def _try_squares(self) -> bool:
        """
        Try to solve by squares

        :return: Anything changed or not
        :rtype: bool
        """
        changed = False

        for i in range(3):
            for j in range(3):
                result = self._try_square(square_y=i * 3, square_x=j * 3)
                if result is True:
                    changed = True

        return changed

    def _try_lines(self) -> bool:
        """
        Try to solve by lines

        :return: Anything changed or not
        :rtype: bool
        """
        changed = False

        # Horizontal
        for row_index in range(9):
            numbers = self._solution[row_index]
            if numbers.count(None) == 1:
                for i in range(1, 10):
                    if i not in numbers:
                        self._change_number(
                            row_index=row_index,
                            column_index=numbers.index(None),
                            value=i,
                        )
                        changed = True
                        break

        # Vertical
        for column_index in range(9):
            numbers = [row[column_index] for row in self._solution]
            if numbers.count(None) == 1:
                for i in range(1, 10):
                    if i not in numbers:
                        self._change_number(
                            row_index=numbers.index(None),
                            column_index=column_index,
                            value=i,
                        )
                        changed = True
                        break

        return changed

    def solve(self) -> T_SUDOKU:
        """
        Solve the sudoku

        :return: Solution
        :rtype: _T_SUDOKU
        """
        time_start = datetime.now()
        while not self.solved:
            if not self._try_lines():
                if not self._try_squares():
                    raise CanNotSolveError('Can not solve the sudoku')
        LOGGER.info(f'Solving time: {(datetime.now() - time_start).total_seconds()} sec')
        LOGGER.info('Solution result:\n' + '\n'.join([str(row) for row in self._solution]))
        return copy.deepcopy(self._solution)

    @property
    def pretty_str_solution(self) -> str:
        """
        Get sudoku solution as formatted string

        :return: Formatted solution
        :rtype: str
        """
        result = ''
        for row in self._solution:
            result += '\n| {} |'.format(' | '.join([str(item) for item in row]))
        return result[1:]


if __name__ == '__main__':
    sudoku_solver = SudokuSolver(_TEST_DATA)
    solution = sudoku_solver.solve()
    assert solution == _TEST_SOLUTION, 'Wrong solution'
