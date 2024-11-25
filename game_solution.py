from tkinter import *
from gui import *
from game import *
from tetris import *
from settings import cell_size
from shapes import *
def main():
    root = Tk()
    root.title("Tetris") #Title
    root.geometry("410x730") # Dimensions
    create_start_gui(root)
    root.mainloop()
if __name__ == "__main__":
    main()
