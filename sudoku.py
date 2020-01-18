
# Sudokus from websudoku.com
# For some documentation on this, 
# visit https://medium.com/@guylipman/solve-sudokus-automatically-and-naturally-6c3b5e5ef148

import itertools


def whatcanitbe(row, col):
    if sudoku[row][col]==0:    
        rowvals = set(sudoku[row])
        colvals = {row[col] for row in sudoku}
        boxrow = int(row/3)*3
        boxcol = int(col/3)*3
        boxvals = [row[boxcol:boxcol+3] 
                        for row in sudoku[boxrow:boxrow+3]]
        boxvals = set(boxvals[0] + boxvals[1] + boxvals[2])
        return list({1,2,3,4,5,6,7,8,9} 
                      - rowvals - colvals - boxvals)
    else:
        return [sudoku[row][col]]


def preparesudoku():
    global sudoku
    sudoku = [[whatcanitbe(row, col) 
                 for col in range(9) ]
                    for row in range(9)]

def maxdigits():
    return max([max([len(col) for col in row]) for row in sudoku])

def printsudoku():
    collength='{{:{}}}'.format(maxdigits())
    string = '\n'.join(
                    [' '.join(
                        [collength.format(''.join(
                            ['{}'.format(s) for s in col]))  
                        for col in row]) 
                     for row in sudoku])
    print(string + '\n')    

def isitthere(cell, i):
    if i in cell:
        if len(cell)==1:
            return '*'
        else:
            return '+'
    else:
        return '-'
        
def printfornum(i):
    return ([[isitthere(col, i) for col in row] for row in sudoku])


def getgroup(rowcolbox, num):
    temp = [[(sudoku[i][j], i, j) 
                for j in range(9) ] 
                    for i in range(9)]
    if rowcolbox=='row':
        return temp[num]
    elif rowcolbox=='col':
        return [row[num] for row in temp]
    elif rowcolbox == 'box':
        startrow = int(num/3)*3
        startcol = (num%3)*3
        group = [row[startcol:startcol+3] 
                 for row in temp[startrow:startrow+3]]
        return group[0] + group[1] + group[2]
    else:
        raise Exception

def cleanarray(rowcolbox, num, size, audit=1):
    global sudoku
    array = getgroup(rowcolbox, num)
    combs = list(itertools.combinations(array, size))
    combs2 = [set.union(*[set(c[0]) 
                     for c in comb]) 
                         for comb in combs]
    combs3 = [len(comb) for comb in combs2]
    assert min(combs3)>=size
    combs3 = [(comb==size) for comb in combs3]
    for i in range(len(combs)):
        if combs3[i]==1:
            vals = list(combs2[i])
            inlocs = [(comb[1], comb[2]) for comb in combs[i]]
            for item in array:
                if (item[1],item[2]) not in inlocs:
                    for val in vals:
                        if val in item[0]:
                            if audit>=1:
                                print('{} cannot be in cell {},{} '
                                      'because it is in group {} in '
                                      'that {} '.format(val, 
                                                        item[1]+1, 
                                                        item[2]+1, 
                                                        combs2[i], 
                                                        rowcolbox))
                            sudoku[item[1]][item[2]].remove(val)  
                            if audit>=2:
                                printsudoku()

def cleanarrays(maxsize, audit=1):
    for size in range(1, maxsize+1):
        for iteration in range(10):
            if maxdigits()==1:
                break
            else:
                for num in range(9):
                    cleanarray('row', num, size, audit)
                    cleanarray('col', num, size, audit)
                    cleanarray('box', num, size, audit)    
                    
def cleanboxes(audit=1):
    global sudoku
    rowcolbox = 'col'
    temp = [
            [sudoku[0][col] + sudoku[1][col] + sudoku[2][col], 
             sudoku[3][col] + sudoku[4][col] + sudoku[5][col],
             sudoku[6][col] + sudoku[7][col] + sudoku[8][col]]
             for col in range(9)]    
    for num in range(1,9):        
        tempfornum = [[int(num in col) for col in row] for row in temp]
        for i in range(3):
            t = tempfornum[3*i:3*i+3]
            for row in range(3):
                for col in range(3):
                    if (t[0][col] + t[1][col] + t[2][col] - t[row][col] == 0):
                        for col2 in range(3):
                            if col2 != col:
                                if t[row][col2] == 1:
                                    for i2 in range(3):
                                        if num in sudoku[col2*3 + i2][3*i + row]:
                                            if audit >= 1:
                                                print('{} cannot be in {},{} as it is needed in another block in this {}'.format(num, col2*3 + i2 + 1, 3*i + row + 1, rowcolbox ))
                                            sudoku[col2*3 + i2][3*i + row].remove(num)
                                            if audit >= 2:
                                                printsudoku()
    rowcolbox = 'row'
    temp = [[row[0] + row[1] + row[2], row[3] + row[4] + row[5], row[6] + row[7] + row[8] ] for row in sudoku]
    for num in range(1,9):        
        tempfornum = [[int(num in col) for col in row] for row in temp]
        for i in range(3):
            t = tempfornum[3*i:3*i+3]
            for row in range(3):
                for col in range(3):
                    if (t[0][col] + t[1][col] + t[2][col] - t[row][col] == 0):
                        for col2 in range(3):
                            if col2 != col:
                                if t[row][col2] == 1:
                                    for i2 in range(3):
                                        if num in sudoku[row][3*col2 + i2]:
                                            if audit>=1:
                                                print('remove {} from {},{} as it is needed in another block in this {}'.format(num, row, 3*col2 + i2, rowcolbox ))
                                            sudoku[row][3*col2 + i2].remove(num)
                                            if audit>=2:
                                                printsudoku()
        

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

sudoku = [
         [2, 0, 0, 1, 7, 0, 0, 3, 0],
         [0, 3, 0, 0, 0, 6, 0, 0, 0],
         [0, 0, 8, 3, 0, 0, 9, 0, 0],
         [9, 0, 0, 0, 0, 0, 0, 1, 0],
         [3, 0, 0, 0, 6, 0, 0, 0, 7],
         [0, 2, 0, 0, 0, 0, 0, 0, 9],
         [0, 0, 5, 0, 0, 4, 8, 0, 0],
         [0, 0, 0, 6, 0, 0, 0, 9, 0],
         [0, 8, 0, 0, 5, 1, 0, 0, 6]]


sudoku = [
         [0, 0, 9, 3, 8, 0, 0, 0, 0],
         [8, 0, 1, 4, 0, 9, 7, 6, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [2, 0, 3, 0, 0, 0, 0, 8, 6],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [4, 8, 0, 0, 0, 0, 3, 0, 2],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 7, 8, 2, 0, 5, 1, 0, 4],
         [0, 0, 0, 0, 7, 1, 8, 0, 0]]



preparesudoku()
printsudoku() 
for j in range(4):
    cleanarrays(maxsize=5)
    printsudoku()
    if maxdigits()==1:
        break
    cleanboxes()                
    printsudoku()
    if maxdigits()==1:
        break
  

if maxdigits()==1:
    sudoku = [[col[0] for col in row] for row in sudoku]




    
