"""
    Deckard Mehdy | deckardmehdy@gmail.com | github.com/deckardmehdy
    
    This file's main purpose is to test the solve() method developed in the sudoku_solver.py file by:
        1. Retreving a set of unique puzzles and their solutions
        2. Solving each puzzle using the solve() method
        3. Comparing the solutions obtained against the correct solutions
"""

import data, sudoku_solver
from timeit import default_timer as timer

def match(mySolution,correctSolution):
    for row in range(9):
        for col in range(9):
            if mySolution[row][col] != correctSolution[row][col]:
                return False
    return True

def printPuzzle(puzzle):
    print()
    for row in range(9):
        if (row == 3) or (row == 6):
            print("-----------------------")
        rowString = " "
        for col in range(9):
            if (col == 3) or (col == 6):
                rowString += "\t|"
            if puzzle[row][col] == 0:
                rowString += "_"
            else:
                rowString += str(puzzle[row][col])
            rowString += " "
        print(rowString)
    print()

def printNotes(notes):
    for num in range(9):
        print("Notes for num = " + str(num+1))
        printPuzzle(notes[num,:,:])
    return

#   -----------------------------------------------------------------------------------------
#                                   -- C O N T R O L --
#
#   maxIter       ->   maximum iterations for solving the sudoku puzzle     ->   val >= 1
#   dataSet       ->   chooses one of two data sets from data.py            ->   val = 1 or 2
#   printPuzzle   ->   prints a sudoku puzzle
#   printNotes    ->   prints all notes for a sudoku puzzle
#   -----------------------------------------------------------------------------------------
def run(maxIter=20,dataSet=2):
    puzzles, solutions = data.get(dataSet)
    correct = 0
    start = timer()
    for i in range(len(puzzles)):
        puzzle, solution = puzzles[i], solutions[i]
        mySolution, myNotes = sudoku_solver.solve(puzzle,maxIter)
        if match(mySolution,solution) == True:
            correct += 1
    end = timer()
    #print("- " + str(correct) + " puzzle(s) solved correctly")
    #print("- Accuracy = " + str(int((correct/len(puzzles)) * 100)) + "%")
    #print("- Total amount of time used to solve the puzzles = " + str(end-start) + " seconds")
    return

if __name__ == "__main__":
    run()
