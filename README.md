# Sudoku Puzzle Solver
Sudoku is a puzzle that requires you to fill in blank cells in a 9x9 grid so that each column, row, and 3x3 subgrid contains all of the digits from 1 to 9. This project uses rule-based elimination and inference techniques to solve a given sudoku puzzle. The goal of this project is to develop software that can solve any sudoku puzzle.

## Requirements
  * Python >= 3.0
  * NumPy >= 1.16.1
  * TimeIt >= 2.3 
  * Pickle >= 4.0
  
## Dataset
Two datasets (DS) are used:
 * **DS 1:** 
    - Generated using https://github.com/Kyubyong/sudoku/blob/master/generate_sudoku.py
    - 1000 unique puzzles and solutions 
 * **DS 2:**
    * Obtained from https://github.com/Kyubyong/sudoku/blob/master/data/test.csv
    * Stored in `unique_puzzles.txt` and `unique_solutions.txt` using Python's Pickle format
    * 30 unique sudoku puzzles and solutions with distinct difficulty levels: 
      * Easy = 1-6
      * Medium = 7-12
      * Hard = 13-18
      * Expert = 19-24
      * Evil = 25-30
      
## File Description
 * `data.py` returns one of the two data sets
 * `sudoku_solver.py` contains the methods used to solve the sudoku puzzle
 * `test.py` loads the data, solves each sudoku puzzle, and compares it against the known solution. **Run this file.**
 
## Implimentation and Results
The techniques implimented to solve a given puzzle, which are explained at [here](https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php), include: 

 * Sole and Unique Canidate
 * Block and Column/Row Interaction 
 * Naked Subset
 * X-Wing
 
As the software is developed, more techniques will be implimented so that even the most difficult sudoku puzzles can be solved. **As of now, this software can correctly solve the entire first dataset and 21 out of 30 (=70%) puzzles in the second dataset.**
