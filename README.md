# Sudoku-Solver
This program is able to sovle any kind (simple, difficult versions, and even totally blank Sudoku) in a second.
The basic idea is to keep finding out the blank space with the least number of available numbers and fill out it (if at least two numbers are available, try one by one).
The most difficult part of trying is once you try the first several blank spaces, you may find out that you are in the wrong path, and then you need to move back to try the other numbers. This is achieved by the combination of a 'while' function and a informative dictionary.
