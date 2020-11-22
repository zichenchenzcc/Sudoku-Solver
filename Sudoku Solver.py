# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:05:33 2020

@author: czc
"""
#The structure of the dic_up is:
#{Index,(Index before ranking,[(Sudoku coordinate),Index of chosen number in available number list,Condition,Length of available number list,Index of last step])}      
import numpy as np 

#Given the Sudoku, return how many numbers you can fill in for each blank space (available_matrix)
#And also the number list you can fill for each blank space(solution_matrix)
def sudoku_support(Sudoku):           
    available_matrix = np.zeros([9,9])   
    solution_matrix = {}
    Sudoku_piece = []                            
    for i in range(3):
        for j in range(3):
            Sudoku_piece.append(Sudoku[(3*i):(3*i + 3), (3*j):(3*j + 3)])
    for i in range(9):
        for j in range(9):
            number_list = [1,2,3,4,5,6,7,8,9]
            if Sudoku[i,j] != 0:
                available_matrix[i,j] = 0
                solution_matrix[i,j] = []
            else:
                piece = Sudoku_piece[i//3*3 + j//3].reshape(9,1)
                for l in piece:
                    if l != 0:
                        number_list.remove(l)    
                number_appear = []
                for m in Sudoku[i,:]:
                    if m !=0:
                        number_appear.append(m)
                for n in Sudoku[:,j]:
                    if n !=0:
                        number_appear.append(n)
                for p in number_appear:
                    repeat=0
                    for q in number_list:
                        repeat = repeat + (q == p)
                    if repeat != 0:
                        number_list.remove(p)
                available_matrix[i,j] = len(number_list)
                solution_matrix[i,j] = number_list
    return available_matrix, solution_matrix

#While there are blank places that can only fill in one number, fill in those places and check whether there are other blank places that can fill in  only one number come out.  If yes, fill in all of them and keep doing.
def fill_only_value(Sudoku):   
    available_matrix, solution_matrix = sudoku_support(Sudoku) 
    while (np.sum(available_matrix==1)) !=0:                   
        for i in range(9):                                     
            for j in range(9):
                if available_matrix[i,j] == 1:
                    Sudoku[i,j] = solution_matrix[i,j][0]
                    available_matrix, solution_matrix = sudoku_support(Sudoku)
    return Sudoku

#Update the fourth element in dictionary which means how many numbers can be fill in the corresponding place
def update_dic(dic_up,solution_matrix):   
    for i in range(len(dic_up)):          
        dic_up[i][1][3] = len(solution_matrix[dic_up[i][1][0]])
    return dic_up

#If all the blank places have at least two choices, try each by each
def Sudoku_intermediate_solver(r,dic_up,copy,Sudoku):      
    available_matrix, solution_matrix = sudoku_support(Sudoku)
    for i in range(r,len(dic_up)):
        copy[i] = np.copy(Sudoku)
        if dic_up[i][1][3] != 0:
            for j in range(dic_up[i][1][3]):
                if dic_up[i][1][2] == 0:
                    Sudoku[dic_up[i][1][0]] = solution_matrix[dic_up[i][1][0]][j]
                    available_matrix, solution_matrix = sudoku_support(Sudoku)
                    Sudoku = fill_only_value(Sudoku)
                    available_matrix, solution_matrix = sudoku_support(Sudoku)
                    if np.sum(Sudoku==0)+np.sum(available_matrix==0) ==81:
                        dic_up[i][1][1] = j
                        dic_up[i][1][2] = 1
                        dic_up[i][1][4] = i
                        dic_up = update_dic(dic_up,solution_matrix)
                    else:
                        Sudoku = np.copy(copy[i])
                        available_matrix, solution_matrix = sudoku_support(Sudoku)
            if dic_up[i][1][2] == 0:
                dic_up[i][1][2] = 2
                dic_up[i][1][4] = dic_up[i-1][1][4]
                break
        else:
            dic_up[i][1][4] = dic_up[i-1][1][4]
    return i,dic_up,copy,Sudoku

def Sudoku_solver(Sudoku):
    available_matrix, solution_matrix = sudoku_support(Sudoku) 
    s = 0
    dic = {}
    copy = {}
    copy[-1] = np.copy(Sudoku)
    for i in range(9):
        for j in range(9):
            if Sudoku[i,j] == 0:
                dic[s] = [(i,j), 0, 0, len(solution_matrix[i,j]),0] 
                s= s + 1                        #Build dictionary (dic_up)
          
    dic_up= sorted(dic.items(), key=lambda d:d[1][3])      #Rank length of available number from smallest to largest
                                                           #Begin by trying the smallest
    i,dic_up,copy,Sudoku = Sudoku_intermediate_solver(0,dic_up,copy,Sudoku)    
    while dic_up[i][1][2] == 2:          #When there is error in continuing
        dic_up[i][1][2] = 0
        i = dic_up[i][1][4]                      
        Sudoku = np.copy(copy[i])
        available_matrix, solution_matrix = sudoku_support(Sudoku)
        dic_up = update_dic(dic_up,solution_matrix)
        while dic_up[i][1][1] >= dic_up[i][1][3] - 1:     #When there is no choice for that step, back to last step
            i = dic_up[i-1][1][4]
            Sudoku = np.copy(copy[i])
            available_matrix, solution_matrix = sudoku_support(Sudoku)
            dic_up = update_dic(dic_up,solution_matrix)
        Sudoku[dic_up[i][1][0]] = solution_matrix[dic_up[i][1][0]][dic_up[i][1][1] + 1]
        available_matrix, solution_matrix = sudoku_support(Sudoku)
        dic_up[i][1][1] = dic_up[i][1][1] + 1
        dic_up = update_dic(dic_up,solution_matrix)
        i,dic_up,copy,Sudoku = Sudoku_intermediate_solver(i+1,dic_up,copy,Sudoku) 
    solved_Sudoku = Sudoku.copy()
    return solved_Sudoku
# %%%% 
#Initial version (easy version)
Sudoku = np.array([[0,7,0,0,0,5,0,0,0],
                   [1,0,0,0,3,0,5,0,8],
                   [0,0,0,2,0,9,0,6,0],
                   [9,1,0,5,0,0,4,2,0],
                   [6,8,0,3,0,0,0,1,0],
                   [2,5,4,0,9,0,0,0,3],
                   [7,0,6,8,0,1,0,4,0],
                   [3,4,5,0,0,6,0,7,1],
                   [0,0,1,0,7,0,2,0,6]]) 

solved_Sudoku = Sudoku_solver(Sudoku)
print(solved_Sudoku)    
# %%%%    
#Difficult version
Sudoku = np.array([[0,7,0,0,0,5,0,0,0],                  
                   [0,0,0,0,3,0,5,0,8],
                   [0,0,0,2,0,9,0,6,0],
                   [0,1,0,5,0,0,4,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,5,4,0,9,0,0,0,3],
                   [0,0,6,8,0,1,0,4,0],
                   [0,0,5,0,0,6,0,7,1],
                   [0,0,1,0,0,0,0,0,6]])                   
  
solved_Sudoku = Sudoku_solver(Sudoku)
print(solved_Sudoku) 
# %%%%
# Just delete [0,1] which is 7 from the above Sudoku and have different solution
Sudoku = np.array([[0,0,0,0,0,5,0,0,0],                  
                   [0,0,0,0,3,0,5,0,8],
                   [0,0,0,2,0,9,0,6,0],
                   [0,1,0,5,0,0,4,0,0],
                   [0,0,0,0,0,0,0,0,0],
                   [0,5,4,0,9,0,0,0,3],
                   [0,0,6,8,0,1,0,4,0],
                   [0,0,5,0,0,6,0,7,1],                     
                   [0,0,1,0,0,0,0,0,6]])                   
  
solved_Sudoku = Sudoku_solver(Sudoku)
print(solved_Sudoku) 

#Blank Sudoku
#Sudoku = np.zeros([9,9])
#solved_Sudoku = Sudoku_solver(Sudoku)
#print(solved_Sudoku) 