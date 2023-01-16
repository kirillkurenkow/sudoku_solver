# sudoku_solver
Simple script to solve simple sudoku

## How to run
### Run examples
You have to provide one of two required arguments: `--data` or `--file`.

You can provide optional argument `--empty-sign` to specify what sign stands for empty cell in sudoku.

Parser ignores all another chars besides "123456789" and an empty sign.

```commandline
usage: sudoku_solver.py [-h] (-d DATA | -f FILE) [-e EMPTY_SIGN]

options:
  -h, --help            show this help message and exit
  -d DATA, --data DATA  Sudoku data. Can contain "\n" and spaces.
  -f FILE, --file FILE  File with sudoku data.
  -e EMPTY_SIGN, --empty-sign EMPTY_SIGN
                        Sign for an empty cell. Default is "x".
```
##### Run with data from commandline
```commandline
python sudoku_solver.py -d 4 7 9 x 1 2 x x x x 3 x 6 7 x x 1 x 1 x 2 9 x x 7 x 4 x x x x 4 x 5 6 8 6 8 x x x x x x 2 2 x x 8 6 3 x 9 x 3 4 x x 8 x 9 x x x 2 x 4 x x 8 x x 8 x 1 5 2 x 4 x x
```
##### Run with data from file
```commandline
python sudoku_solver.py -f "some_data.txt"
```

## Solving methods
Script uses the only one solving method besides basic filling the row and the square: scanning in two directions.

Maybe, I'll add some later.
