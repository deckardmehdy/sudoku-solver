"""
    Deckard Mehdy | deckardmehdy@gmail.com | github.com/deckardmehdy
    
    This file solves a 9x9 sudoku puzzle. Sudoku is a puzzle that requires you to fill in blank cells in a 9x9 grid so that each column, row, and 3x3 subgrid contains all of the digits from 1 to 9.
    The techniques used to solve, which are explained at [https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php], include:
        - Sole and Unique Canidate
        - Block and Column/Row Interaction
        - Block and Block Interaction
        - Naked Subset
        - Hidden Subset
        - X-Wing
"""

import numpy as np
from itertools import combinations

# Impliments the 'Unique Canidate' method:
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

def eraseCanidatesInCol(nums,col,rows_to_exclude,notes):
    for num in nums:
        for row in range(9):
            if row not in rows_to_exclude:
                notes[num,row,col] = 0
    return

def eraseCanidatesInRow(nums,row,cols_to_exclude,notes):
    for num in nums:
        for col in range(9):
            if col not in cols_to_exclude:
                notes[num,row,col] = 0
    return

def eraseCanidatesInOtherSubGridRows(notes,rows,subgrids_to_exclude):
    subgrid_one, subgrid_two = subgrids_to_exclude
    if subgrid_one[1] == 0:
        if subgrid_two[1] == 1:
            colStart,colEnd = 6, 9
        else:
            colStart,colEnd = 3, 6
    elif subgrid_one[1] == 1:
        if subgrid_two[1] == 0:
            colStart,colEnd = 6, 9
        else:
            colStart,colEnd = 0, 3
    else:
        if subgrid_two[1] == 0:
            colStart,colEnd = 3, 6
        else:
            colStart,colEnd = 0, 3
    for row in rows:
        notes[row,colStart:colEnd] = 0
    return

def eraseCanidatesInOtherSubGridCols(notes,cols,subgrids_to_exclude):
    subgrid_one, subgrid_two = subgrids_to_exclude
    if subgrid_one[0] == 0:
        if subgrid_two[0] == 1:
            rowStart,rowEnd = 6, 9
        else:
            rowStart,rowEnd = 3, 6
    elif subgrid_one[0] == 1:
        if subgrid_two[0] == 0:
            rowStart,rowEnd = 6, 9
        else:
            rowStart,rowEnd = 0, 3
    else:
        if subgrid_two[0] == 0:
            rowStart,rowEnd = 3, 6
        else:
            rowStart,rowEnd = 0, 3
    for col in cols:
        notes[rowStart:rowEnd,col] = 0
    return

def eraseCanidatesInSubGrid(nums,subGridBounds,cells_to_exclude,notes):
    [rowStart,rowEnd,colStart,colEnd] = subGridBounds
    for num in nums:
        for row in range(rowStart,rowEnd):
            for col in range(colStart,colEnd):
                cell = [row,col]
                if cell not in cells_to_exclude:
                    notes[num,row,col] = 0
    return

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

def findSubsets(notes,subset_size):
    totalNotes = np.sum(notes,axis=0,dtype=int)
    subsets_in_notes = [[],[],[],[],[],[],[],[],[]]
    for row in range(9):
        for col in range(9):
            if totalNotes[row][col] == subset_size:
                subset = []
                for num in range(9):
                    if notes[num,row,col] == 1:
                        subset.append(num)
                subsets_in_notes[row].append(subset)
            else:
                subsets_in_notes[row].append([])
    return subsets_in_notes

# Impliments the 'Hidden Subset' method
def hiddenSubset(notes,puzzle):
    max_subset_length = 2       # 2 <= max_subset_length <= 9 (2 or 3 are recommended)
    start, end = [0,3,6], [3,6,9]
    for subset_length in range(2,(max_subset_length+1)):
        subgrids, rows, cols = hiddenSubsetHelper(notes,puzzle)
        for subgrid_row in range(3):
            for subgrid_col in range(3):
                for row in range(start[subgrid_row],end[subgrid_row]):
                    for col in range(start[subgrid_col],end[subgrid_col]):
                        if puzzle[row][col] == 0:
                            for num in range(9):
                                if notes[num,row,col] == 1:
                                    subgrids[str(subgrid_row)+"-"+str(subgrid_col)].setdefault(str(num),[]).append([row,col])
                                    rows[str(row)].setdefault(str(num),[]).append(col)
                                    cols[str(col)].setdefault(str(num),[]).append(row)

        for row in range(9):
            row_to_investigate = rows[str(row)]
            potential_subsets = []
            for num in range(9):
                if len(row_to_investigate.get(str(num),[])) == subset_length:
                    potential_subsets.append(num)
            if len(potential_subsets) >= subset_length:
                combos = combinations(potential_subsets,subset_length)
                for potential_subset in combos:
                    match = True
                    for j in range(1,subset_length):
                        num, another_num = potential_subset[j-1], potential_subset[j]
                        if row_to_investigate[str(num)] != row_to_investigate[str(another_num)]:
                            match = False
                    if match == True:
                        for col in row_to_investigate[str(potential_subset[0])]:
                            partiallyEraseCellNotes(row,col,potential_subset,notes)

        
        for col in range(9):
            col_to_investigate = cols[str(col)]
            potential_subsets = []
            for num in range(9):
                if len(col_to_investigate.get(str(num),[])) == subset_length:
                    potential_subsets.append(num)
            if len(potential_subsets) >= subset_length:
                combos = combinations(potential_subsets,subset_length)
                for potential_subset in combos:
                    match = True
                    for j in range(1,subset_length):
                        num, another_num = potential_subset[j-1], potential_subset[j]
                        if col_to_investigate[str(num)] != col_to_investigate[str(another_num)]:
                            match = False
                    if match == True:
                        for row in col_to_investigate[str(potential_subset[0])]:
                            partiallyEraseCellNotes(row,col,potential_subset,notes)

        for subgrid_row in range(3):
            for subgrid_col in range(3):
                subgrid_to_investigate = subgrids[str(subgrid_row)+"-"+str(subgrid_col)]
                potential_subsets = []
                for num in range(9):
                    if len(subgrid_to_investigate.get(str(num),[])) == subset_length:
                        potential_subsets.append(num)
                if len(potential_subsets) >= subset_length:
                    combos = combinations(potential_subsets,subset_length)
                    for potential_subset in combos:
                        match = True
                        for j in range(1,subset_length):
                            num, another_num = potential_subset[j-1], potential_subset[j]
                            if subgrid_to_investigate[str(num)] != subgrid_to_investigate[str(another_num)]:
                                match = False
                        if match == True:
                            for cell in subgrid_to_investigate[str(potential_subset[0])]:
                                [row,col] = cell
                                partiallyEraseCellNotes(row,col,potential_subset,notes)
    return

def hiddenSubsetHelper(notes,puzzle):
    subgrids, rows, cols = {}, {}, {}
    for subgrid_row in range(3):
        for subgrid_col in range(3):
            subgrids[str(subgrid_row)+"-"+str(subgrid_col)] = {}
    for i in range(9):
        rows[str(i)] = {}
        cols[str(i)] = {}
    return subgrids, rows, cols

def inference(notes):
    # Impliments the 'Block and Column/Row Interaction' method:
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
                
    # Impliments the 'Block and Block Interaction' method:
    subgrids = [[{},{},{}],[{},{},{}],[{},{},{}]]
    for i in range(3):
        for j in range(3):
            subgrid = subgrids[i][j]
            subgrid["nonzero_rows"] = False
            subgrid["nonzero_cols"] = False
    for row in range(3):
        for col in range(3):
            subGrid = notes[start[row]:end[row],start[col]:end[col]]
            
            rowSums = np.sum(subGrid,axis=1,dtype=int)
            rows_with_notes = []
            for i in range(3):
                if rowSums[i] > 0:
                    rows_with_notes.append(start[row] + i)
            if len(rows_with_notes) == 2:
                subgrid_storage = subgrids[row][col]
                subgrid_storage["nonzero_rows"] = rows_with_notes

            colSums = np.sum(subGrid,axis=0,dtype=int)
            cols_with_notes = []
            for j in range(3):
                if colSums[j] > 0:
                    cols_with_notes.append(start[col] + j)
            if len(cols_with_notes) == 2:
                subgrid_storage = subgrids[row][col]
                subgrid_storage["nonzero_cols"] = cols_with_notes
    for row in range(3):
        for col in range(3):
            subgrid = subgrids[row][col]
            if subgrid["nonzero_rows"] != False:
                for c in range(3):
                    if c != col:
                        another_subgrid = subgrids[row][c]
                        if subgrid["nonzero_rows"] == another_subgrid["nonzero_rows"]:
                            eraseCanidatesInOtherSubGridRows(notes,subgrid["nonzero_rows"],[[row,col],[row,c]])
                            another_subgrid["nonzero_rows"] = False
            if subgrid["nonzero_cols"] != False:
                for r in range(3):
                    if r != row:
                        another_subgrid = subgrids[r][col]
                        if subgrid["nonzero_cols"] == another_subgrid["nonzero_cols"]:
                            eraseCanidatesInOtherSubGridCols(notes,subgrid["nonzero_cols"],[[r,col],[row,col]])
                            another_subgrid["nonzero_cols"] = False
    return

# Impliments the 'Naked Subset' method:
def nakedSubset(notes,puzzle):
    max_subset_length = 3       # 2 <= max_subset_length <= 9 (2 or 3 are recommended)
    for subset_size in range(2,(max_subset_length+1)):
        subsets_in_notes = findSubsets(notes,subset_size)
        for row in range(9):
            for col in range(9):
                if len(subsets_in_notes[row][col]) > 0:
                    subset = subsets_in_notes[row][col]
                    
                    cols_containing_same_subset = [col]
                    for c in range(9):
                        another_subset = subsets_in_notes[row][c]
                        if c != col and subset == another_subset:
                            cols_containing_same_subset.append(c)
                    if len(cols_containing_same_subset) == subset_size:
                        eraseCanidatesInRow(subset,row,cols_containing_same_subset,notes)
                
                    rows_containing_same_subset = [row]
                    for r in range(9):
                        another_subset = subsets_in_notes[r][col]
                        if r != row and subset == another_subset:
                            rows_containing_same_subset.append(r)
                    if len(rows_containing_same_subset) == subset_size:
                        eraseCanidatesInCol(subset,col,rows_containing_same_subset,notes)
        
                    [rowStart,rowEnd,colStart,colEnd] = subGridBoundaries(row,col)
                    cells_containing_same_subset = [[row,col]]
                    for r in range(rowStart,rowEnd):
                        for c in range(colStart,colEnd):
                            if r != row or c != col:
                                another_subset = subsets_in_notes[r][c]
                                if subset == another_subset:
                                    cells_containing_same_subset.append([r,c])
                    if len(cells_containing_same_subset) == subset_size:
                        eraseCanidatesInSubGrid(subset,[rowStart,rowEnd,colStart,colEnd],cells_containing_same_subset,notes)
    return

def partiallyEraseCellNotes(row,col,nums_to_keep,notes):
    for num in range(9):
        if num not in nums_to_keep:
            notes[num,row,col] = 0
    return

# MAIN METHOD #
def solve(puzzle,maxIter):
    notes = createNotes(puzzle)
    [emptyCells,totalEmptyCells] = countEmptyCells(puzzle)
    iter = 0
    while totalEmptyCells > 0 and iter < maxIter:
        cellsFilled = 0
        for num in range(9):
            if emptyCells[num] > 0:
                cellsToFill = checkNotes(notes[num][:][:])
                cellsFilled += len(cellsToFill)
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
            cellsFilled += len(cellsToFill)
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
    
#       Use the 'Naked Subset' and 'X-Wing' methods if no cells were filled during this iteration:
        if cellsFilled == 0:
            nakedSubset(notes,puzzle)
            xwing(emptyCells,notes,puzzle)
            hiddenSubset(notes,puzzle)
        
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

# Impliments the 'X-Wing' method:
def xwing(emptyCells,notes,puzzle):
    for num in range(9):
        if emptyCells[num] > 0:
            colSums = np.sum(notes[num,:,:],axis=0,dtype=int)
            rowSums = np.sum(notes[num,:,:],axis=1,dtype=int)
            cols_to_check, rows_to_check = [],[]
            for i in range(9):
                if colSums[i] == 2:
                    cols_to_check.append(i)
                if rowSums[i] == 2:
                    rows_to_check.append(i)
        
            if len(cols_to_check) > 1:
                rows_containing_notes = []
                for col in cols_to_check:
                    rows = []
                    for row in range(9):
                        if notes[num,row,col] == 1:
                            rows.append(row)
                    rows_containing_notes.append(rows)
                for i in range(len(cols_to_check)-1):
                    for j in range((i+1),len(cols_to_check)):
                        if rows_containing_notes[i] == rows_containing_notes[j]:
                            for row in rows_containing_notes[i]:
                                eraseCanidatesInRow([num],row,cols_to_check,notes)

            if len(rows_to_check) > 1:
                cols_containing_notes = []
                for row in rows_to_check:
                    cols = []
                    for col in range(9):
                        if notes[num][row][col] == 1:
                            cols.append(col)
                    cols_containing_notes.append(cols)
                for i in range(len(rows_to_check)-1):
                    for j in range((i+1),len(rows_to_check)):
                        if cols_containing_notes[i] == cols_containing_notes[j]:
                            for col in cols_containing_notes[i]:
                                eraseCanidatesInCol([num],col,rows_to_check,notes)
    return
