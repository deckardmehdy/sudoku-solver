# Sudoku Puzzle Solver
Sudoku is a puzzle that requires you to fill in blank cells in a 9x9 grid so that each column, row, and 3x3 subgrid contains all of the digits from 1 to 9. This project uses rule-based elimination and inference techniques to solve a given puzzle. The goal of this project is to develop software that can solve any sudoku puzzle.

## Requirements
  * Python >= 3.0
  * NumPy >= 1.16.1
  * TimeIt >= 2.3 
  * Pickle >= 4.0
  
## Dataset
Two datasets (DS) are used:
 * **DS 1:** 
    - Generated using https://github.com/Kyubyong/sudoku/blob/master/generate_sudoku.py
    - 1000 unique sudoku puzzles with varying difficulty levels
 * **DS 2:**
    * Obtained from https://github.com/Kyubyong/sudoku/blob/master/data/test.csv
    * 30 unique sudoku puzzles with distinct difficulty levels: 
      * Easy = 1-6
      * Medium = 7-12
      * Hard = 13-18
      * Expert = 19-24
      * Evil = 25-30
      
## File Description
 * `data.py`: creates
