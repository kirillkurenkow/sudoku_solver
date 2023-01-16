import logging
import os
from argparse import (
    ArgumentParser,
    ArgumentTypeError,
)
from typing import Union

from Source import (
    SudokuSolver,
    T_SUDOKU,
)

logging.basicConfig(
    filename='sudoku_solver.log',
    filemode='a',
    format='[%(asctime)s] %(levelname)s: %(filename)s(%(lineno)d): %(funcName)s: %(message)s',
    level=logging.INFO,
    encoding='utf-8',
)
LOGGER = logging.getLogger(__name__)


def main(data) -> None:
    sudoku_solver = SudokuSolver(data)
    sudoku_solver.solve()
    print(sudoku_solver.pretty_str_solution)


class CheckArgs:
    """
    Check arguments for ArgParser
    """

    @staticmethod
    def data(value: str) -> Union[T_SUDOKU, None]:
        if value:
            parsed_data = parse_data(value)
            return parsed_data
        return None

    @staticmethod
    def file(value: str) -> Union[str, None]:
        if value:
            if not os.path.exists(value):
                raise ArgumentTypeError(f'File not exists: {value}')
            return os.path.realpath(value)
        return None


def get_data_from_file(filename_: str) -> T_SUDOKU:
    """
    Read data from file

    :param str filename_: Filename

    :return: Parsed data
    :rtype: T_SUDOKU
    """
    # Read file
    with open(filename_) as file:
        data = file.read()

    # Parse data
    parsed_data = parse_data(data)

    return parsed_data


def parse_data(data: str) -> T_SUDOKU:
    """
    Parse input data

    :param str data: Input data

    :return: Parsed data
    :rtype: T_SUDOKU
    """
    data = list(data)
    result = [[] for _ in range(9)]
    for row_index in range(9):
        for column_index in range(9):
            item = data.pop(0)
            while (item not in '123456789' + empty_sign) and data:
                item = data.pop(0)
            if item == empty_sign:
                result[row_index].append(None)
            else:
                result[row_index].append(int(item))
    return result


if __name__ == '__main__':
    # Parse args
    ArgParser = ArgumentParser()
    data_group = ArgParser.add_mutually_exclusive_group(required=True)
    data_group.add_argument('-d', '--data', action='store', type=CheckArgs.data,
                            help='Sudoku data. Can contain "\\n" and spaces.')
    data_group.add_argument('-f', '--file', action='store', type=CheckArgs.file,
                            help='File with sudoku data.')
    ArgParser.add_argument('-e', '--empty-sign', default='x', action='store',
                           help='Sign for an empty cell. Default is "x".', dest='empty_sign')

    ScriptArgs = ArgParser.parse_args()
    sudoku_data = ScriptArgs.data
    filename = ScriptArgs.file
    empty_sign = ScriptArgs.empty_sign

    # Parse data
    if filename is not None:
        sudoku_data = get_data_from_file(filename)

    # Main
    main(sudoku_data)
