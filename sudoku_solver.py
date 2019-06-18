"""
    Deckard Mehdy | deckardmehdy@gmail.com | github.com/deckardmehdy
    
    This file solves a 9x9 sudoku puzzle. Sudoku is a puzzle that requires you to fill in blank cells in a 9x9 grid so that each column, row, and 3x3 subgrid contains all of the digits from 1 to 9.
    The techniques used to solve, which are explained at [https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php], include:
        - Sole and Unique Canidate
        - Block and column/row interaction
"""

import numpy as np

# Impliments the unique canidate method:
def checkNotes(notes):
    cellsToFill = []
    start, end = [0,3,6], [3,6,9]
    for row in range(3):
        for col in range(3):
            cell = checkSubGrid(start[row],end[row],start[col],end[col],notes)
            if cell != None:
                if cell not in cellsToFill:
                    cellsToFill.append(cell)

    for col in range(9):
        notes_in_col = 0
        for row in range(9):
            if notes[row][col] == 1:
                notes_in_col += 1
                cell = [row,col]
        if notes_in_col == 1:
            if cell not in cellsToFill:
                cellsToFill.append(cell)

    for row in range(9):
        notes_in_row = 0
        for col in range(9):
            if notes[row][col] == 1:
                notes_in_row += 1
                cell = [row,col]
        if notes_in_row == 1:
            if cell not in cellsToFill:
                cellsToFill.append(cell)

    return cellsToFill

def checkSubGrid(rowStart,rowEnd,colStart,colEnd,notes):
    notes_in_subgrid = 0
    for row in range(rowStart,rowEnd):
        for col in range(colStart,colEnd):
            if notes[row][col] == 1:
                notes_in_subgrid += 1
                cell = [row,col]
    if notes_in_subgrid == 1:
        return cell
    else:
        return None

def clearOtherSubGridCols(rowStart,rowEnd,col,notes):
    for row in range(9):
        if (row < rowStart) or (row >= rowEnd):
            notes[row][col] = 0
    return

def clearOtherSubGridRows(colStart,colEnd,row,notes):
    for col in range(9):
        if (col < colStart) or (col >= colEnd):
            notes[row][col] = 0
    return

def countEmptyCells(puzzle):
#   emptyCells[i] = val:
#       (i+1) = num in sudoku puzzle
#         val = num of cells left to fill
    emptyCells = [9] * 9
    totalEmptyCells = 81
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != 0:
                num = puzzle[row][col]
                emptyCells[num-1] -= 1
                totalEmptyCells -= 1
    return [emptyCells,totalEmptyCells]

def createNotes(puzzle):
#   notes[i,j,k] = val:
#       i = number the note corresponds to;
#       j = row of cell;
#       k = column of cell;
#       val = cell contains (1) or doesn't contain (0) a note.
    notes = np.ones((9,9,9),dtype=int)
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] != 0:
                eraseSubGridNotes(row,col,notes,puzzle)
                eraseRowAndColNotes(row,col,notes,puzzle)
                eraseCellNotes(row,col,notes)
    return notes

def eraseCellNotes(row,col,notes):
    notes[:,row,col] = 0
    return

def eraseSubGridNotes(row,col,notes,puzzle):
    num = (puzzle[row][col]) - 1
    [rowStart,rowEnd,colStart,colEnd] = subGridBoundaries(row,col)
    notes[num,rowStart:rowEnd,colStart:colEnd] = 0
    return

def eraseRowAndColNotes(row,col,notes,puzzle):
    num = puzzle[row][col] - 1
    notes[num,:,col], notes[num,row,:] = 0, 0
    return

# Impliments the block and column/row interaction method:
def inference(notes):
    start, end = [0,3,6], [3,6,9]
    for row in range(3):
        for col in range(3):
            subGrid = notes[start[row]:end[row],start[col]:end[col]]
            
            rowSums = np.sum(subGrid,axis=1,dtype=int)
            rows_with_no_notes, row_with_notes = 0, 0
            for i in range(3):
                if rowSums[i] == 0:
                    rows_with_no_notes += 1
                else:
                    row_with_notes = start[row] + i
            if rows_with_no_notes == 2:
                clearOtherSubGridRows(start[col],end[col],row_with_notes,notes)
            
            colSums = np.sum(subGrid,axis=0,dtype=int)
            cols_with_no_notes, col_with_notes = 0, 0
            for j in range(3):
                if colSums[j] == 0:
                    cols_with_no_notes += 1
                else:
                    col_with_notes = start[col] + j
            if cols_with_no_notes == 2:
                clearOtherSubGridCols(start[row],end[row],col_with_notes,notes)
    return

def solve(puzzle,maxIter):
    notes = createNotes(puzzle)
    [emptyCells,totalEmptyCells] = countEmptyCells(puzzle)
    iter = 0
    while totalEmptyCells > 0 and iter < maxIter:
        for num in range(9):
            if emptyCells[num] > 0:
                cellsToFill = checkNotes(notes[num][:][:])
                for cell in cellsToFill:
                    [row,col] = cell
                    puzzle[row][col] = num + 1
                    eraseSubGridNotes(row,col,notes,puzzle)
                    eraseRowAndColNotes(row,col,notes,puzzle)
                    eraseCellNotes(row,col,notes)
                    emptyCells[num] -= 1
                    totalEmptyCells -= 1
                inference(notes[num])
                    
#       Check if any cells have just one note (sole canidate method):
        totalNotes = np.sum(notes,axis=0,dtype=int)
        cellsToFill = []
        for row in range(9):
            for col in range(9):
                if totalNotes[row][col] == 1:
                    cellsToFill.append([row,col])
        if len(cellsToFill) > 0:
            for cell in cellsToFill:
                [row,col] = cell
                for num in range(9):
                    if notes[num][row][col] == 1:
                        numToFill = num
                puzzle[row][col] = numToFill + 1
                eraseSubGridNotes(row,col,notes,puzzle)
                eraseRowAndColNotes(row,col,notes,puzzle)
                eraseCellNotes(row,col,notes)
                emptyCells[numToFill] -= 1
                totalEmptyCells -= 1
        iter += 1
    return puzzle,notes

def subGridBoundaries(row,col):
    if row < 3:
        rowStart, rowEnd = 0, 3
    elif row > 5:
        rowStart, rowEnd = 6, 9
    else:
        rowStart, rowEnd = 3, 6
    
    if col < 3:
        colStart, colEnd  = 0, 3
    elif col > 5:
        colStart, colEnd  = 6, 9
    else:
        colStart, colEnd  = 3, 6

    return [rowStart,rowEnd,colStart,colEnd]
