from tetris import Block
from game import *
from tkinter import *
from settings import *
def create_square(canvas):
    return [
        Block(canvas, 160, 0, "blue"),               # Top-left block
        Block(canvas, 160 + cell_size, 0, "blue"),   # Top-right block
        Block(canvas, 160, cell_size, "blue"),       # Bottom-left block
        Block(canvas, 160 + cell_size, cell_size, "blue")  # Bottom-right block
    ]
def create_rectangle(canvas):
    return [
        Block(canvas, 80, 0, "lightgreen"),               # Top-left block
        Block(canvas, 80 + cell_size, 0, "lightgreen"),   # Top-right block
        Block(canvas, 80+cell_size*2, 0, "lightgreen"),       # Bottom-left block
        Block(canvas, 80 + cell_size*3, 0, "lightgreen")
    ]
def create_zshape1(canvas):
    return [
        Block(canvas, 120, 0, "yellow"),               # Top-left block
        Block(canvas, 120 - cell_size, 0, "yellow"),   # Top-right block
        Block(canvas, 120-cell_size, cell_size, "yellow"),       # Bottom-left block
        Block(canvas, 120-cell_size*2, cell_size, "yellow")  # Bottom-right block
    ]
def create_zshape2(canvas):
    return [
        Block(canvas, 120, 0, "white"),               # Top-left block
        Block(canvas, 120 + cell_size, 0, "white"),   # Top-right block
        Block(canvas, 120+cell_size, cell_size, "white"),       # Bottom-left block
        Block(canvas, 120+cell_size*2, cell_size, "white")  # Bottom-right block
    ]
def create_lshape1(canvas):
    return [
        Block(canvas, 120, cell_size, "orange"),               # Top-left block
        Block(canvas, 120 + cell_size, cell_size, "orange"),   # Top-right block
        Block(canvas, 120+cell_size*2, cell_size, "orange"),       # Bottom-left block
        Block(canvas, 120, 0, "orange")  # Bottom-right block
    ]
def create_lshape2(canvas):
    return [
        Block(canvas, 120, cell_size, "pink"),               # Top-left block
        Block(canvas, 120 + cell_size, cell_size, "pink"),   # Top-right block
        Block(canvas, 120+cell_size*2, cell_size, "pink"),       # Bottom-left block
        Block(canvas, 120+cell_size*2, 0, "pink")  # Bottom-right block
    ]
def create_tshape(canvas):
    return [
        Block(canvas, 120, cell_size, "brown"),               # Top-left block
        Block(canvas, 120 + cell_size, cell_size, "brown"),   # Top-right block
        Block(canvas, 120+cell_size*2, cell_size, "brown"),       # Bottom-left block
        Block(canvas, 120+cell_size, 0, "brown")  # Bottom-right block
    ]