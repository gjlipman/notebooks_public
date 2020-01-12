#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 18:55:46 2020

@author: gjlipman
"""

def fillcells(sudoku):
    # This goes through each cell and removes any numbers it couldn't be
    for iteration in range(5):
        for row in range(9):
            for col in range(9):
                cell = sudoku[row][col]
                if len(cell)>1:
                    for val in cell:
                        if [val] in sudoku[row]:
                            cell.remove(val)
                        elif [val] in [row[col] for row in sudoku]:
                            cell.remove(val)
                        else:
                            boxrow, boxcol = int(row/3)*3, int(col/3)*3
                            box = [row[boxcol:boxcol+3] for row in sudoku[boxrow:boxrow+3]]
                            if [val] in box[0]+box[1]+box[2]:
                                cell.remove(val)
    return sudoku


def findknowns(sudoku):
    # This goes through each number, and finds any columns, rows or boxes we know it is in
    for iteration in range(5):
        for val in range(1,10):
            for row in range(9):
                if [val] not in sudoku[row]:
                    matches = [col for col in sudoku[row] if val in col ]
                    if len(matches)==1:
                        position = sudoku[row].index(matches[0])
                        sudoku[row][position] = [val]
            for col in range(9):
                if [val] not in [row[col] for row in sudoku]:
                    matches =  [row[col] for row in sudoku if val in row[col]]
                    if len(matches)==1:
                        position = [row[col] for row in sudoku].index(matches[0])
                        sudoku[position][col] = [val]
            for boxrow in [0,3,6]:
                for boxcol in [0, 3, 6]:
                    box = [row[boxcol:boxcol+3] for row in sudoku[boxrow:boxrow+3]]
                    matches = [cell for cell in box[0]+box[1]+box[2] if val in cell]
                    if len(matches)==1:
                        position = (box[0]+box[1]+box[2]).index(matches[0])
                        sudoku[boxrow+int(position/3)][boxcol + position%3] = [val]
    return sudoku

def isitthere(cell, i):
    if i in cell:
        if len(cell)==1:
            return '*'
        else:
            return '+'
    else:
        return '-'

def printsudoku(i=None):
    if i is None:
        return [[''.join([str(val) for val in col]) for col in row] for row in sudoku]
        #return pd.DataFrame([[''.join([str(val) for val in col]) for col in row] for row in sudoku])
        #this second version looks better but requires pandas
    else:
        return ([[isitthere(col, i) for col in row] for row in sudoku])
    


sudoku =    [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]


# Medium difficulty from websudoku.com
sudoku =    [
            [0, 0, 0, 0, 0, 5, 6, 4, 0], 
            [8, 0, 0, 0, 0, 0, 0, 3, 5], 
            [0, 0, 7, 3, 0, 0, 0, 2, 8], 
            [0, 0, 1, 7, 5, 0, 0, 0, 0], 
            [0, 0, 0, 4, 0, 8, 0, 0, 0], 
            [0, 0, 0, 0, 3, 6, 9, 0, 0], 
            [1, 7, 0, 0, 0, 3, 4, 0, 0], 
            [5, 9, 0, 0, 0, 0, 0, 0, 7], 
            [0, 4, 2, 6, 0, 0, 0, 0, 0]]

sudoku = [[[cell] if cell>0 else [1,2,3,4,5,6,7,8,9] for cell in row ] for row in sudoku]

sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)

sudoku = [[cell[0] if len(cell)==1 else 0 for cell in row] for row in sudoku]



#Evil difficulty from websudoku.com
sudoku =    [
            [0, 0, 0, 5, 0, 0, 7, 9, 0], 
            [0, 8, 0, 0, 0, 0, 0, 3, 0], 
            [7, 0, 3, 0, 0, 0, 0, 0, 2], 
            [4, 0, 0, 0, 8, 7, 2, 0, 0], 
            [6, 0, 0, 0, 0, 0, 0, 0, 7], 
            [0, 0, 7, 6, 9, 0, 0, 0, 5], 
            [9, 0, 0, 0, 0, 0, 5, 0, 4], 
            [0, 3, 0, 0, 0, 0, 0, 2, 0], 
            [0, 5, 4, 0, 0, 2, 0, 0, 0]]


#sudoku = [[[cell] if cell>0 else [] for cell in row ] for row in sudoku]

sudoku = [[[cell] if cell>0 else [1,2,3,4,5,6,7,8,9] for cell in row ] for row in sudoku]


sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)

sudoku[4][6]=[3,9]
sudoku[3][8]=[3,9]
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)

sudoku[7][3]=[4,7]
sudoku[7][4]=[4,5,7]
sudoku[7][5] = [4,5]
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)
sudoku[8][6] = [3,6]
sudoku[8][8] = [3,6]
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)
sudoku = fillcells(sudoku)
sudoku = findknowns(sudoku)

sudoku = [[cell[0] if len(cell)==1 else 0 for cell in row] for row in sudoku]



