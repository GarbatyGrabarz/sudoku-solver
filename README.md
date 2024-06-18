# Sudoku solver

## How to use it
Download and install [Python](https://www.python.org/downloads/)

Download the program
1. Click on green button "<> Code"
2. Click on "Download ZIP"
3. Unpack the downloaded .zip

Create a text file which name starts with sudoku. The program supports multiple files so you can make as many as you want.
<br>Example: `sudoku.txt`, `sudoku_test.txt` or `sudoku board.txt`
<br>The file should be placed in the same directory as `solver.py`

Fill the text file with input data so that you have 9 lines, 9 characters each. For empty field you can use any character that is not a space. Can be `.` or `0` if you want. 
So that this...
```
.2...43..
9...2...8
...6.9.5.
........1
.725.368.
6........
.8.2.5...
1...9...3
..98...6.
```
...gives this (in the image below there will always be dots even if you used a different character):
```
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┓
┃ .  2  . ┃ .  .  4 ┃ 3  .  . ┃
┃ 9  .  . ┃ .  2  . ┃ .  .  8 ┃
┃ .  .  . ┃ 6  .  9 ┃ .  5  . ┃
┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫
┃ .  .  . ┃ .  .  . ┃ .  .  1 ┃
┃ .  7  2 ┃ 5  .  3 ┃ 6  8  . ┃
┃ 6  .  . ┃ .  .  . ┃ .  .  . ┃
┣━━━━━━━━━╋━━━━━━━━━╋━━━━━━━━━┫
┃ .  8  . ┃ 2  .  5 ┃ .  .  . ┃
┃ 1  .  . ┃ .  9  . ┃ .  .  3 ┃
┃ .  .  9 ┃ 8  .  . ┃ .  6  . ┃
┗━━━━━━━━━┻━━━━━━━━━┻━━━━━━━━━┛
```

Run the `solver.py` by double clicking it.

Follow the instructions in the terminal
