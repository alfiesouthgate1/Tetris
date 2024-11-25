from tetris import Piece
from settings import cell_size, canvas_height, canvas_width
from tkinter import *
from shapes import *
import random
import json

class TetrisGame:
    def __init__(self, root, falling_timer, player_name):
        self.root = root
        self.score = IntVar()
        self.score.set(0)
        self.canvas = None
        self.current_piece = None
        self.grid = [[None for _ in range(10)] for _ in range(18)]
        self.falling = False
        self.falling_timer = falling_timer
        self.soft_lock_active = False
        self.soft_lock_time = 500
        self.game_over_flag = False
        self.player_name = player_name
        self.is_paused = False

    def set_canvas(self, canvas):
        self.canvas = canvas

    def create_piece(self, blocks):
        self.current_piece = Piece(self.canvas, blocks)
    
    def increase_score1(self, num_rows):
        self.score.set(self.score.get()+1000*num_rows)
        self.update_score()

    def increase_score(self):
        self.score.set(self.score.get()+10)
        self.update_score()
    
    def increase_score2(self, amount):
        self.score.set(self.score.get()+amount)
        self.update_score()

    def update_score(self):
        if self.canvas:
            self.canvas.delete("score")
            self.canvas.create_text(200, 60, text=f"{self.score.get()}", font=("Arial", 40), tags="score")

    def can_move(self, dx, dy):
        for block in self.current_piece.blocks:
            if block.rect is None or not self.canvas.find_withtag(block.rect):
                print(f"Warning: Block {block} has an invalid or missing rect.")
                return False
            
            x1, y1, x2, y2 = self.canvas.coords(block.rect)
            new_x1 = x1+dx
            new_y1 = y1+dy
            if new_x1 < 0 or new_x1 + cell_size > canvas_width:
                return False
            if new_y1 + cell_size > canvas_height:
                return False
            new_col = int(new_x1/ cell_size)
            new_row = int(new_y1/cell_size)
            if 0<= new_row < 18 and 0 <= new_col < 10:
                if self.grid[new_row][new_col] is not None:
                    return False 
        return True
    
    def check_game_state(self):
        if self.game_over_flag:
            return
        self.lock_piece(self.current_piece)
        self.clear_lines()
        self.create_new_piece()
        self.fall()

        #Lock the current piece in place

    def lock_piece(self, piece):
        for block in piece.blocks:
            x1, y1, x2, y2 = self.canvas.coords(block.rect)
            col = int(x1/cell_size)
            row = int((y1/cell_size))
            if 0 <= col < 10 and 0<= row < 18:
                self.grid[row][col] = block
                if row < 5:
                    self.game_over()
                    return
            else:
                print(f"Invalid grid position: (row={row}, col={col})")

    def create_new_piece(self):
        if self.game_over_flag:
            return
        if self.falling_timer > 400:
            self.falling_timer = self.falling_timer-1
        self.falling = True
        num = random.randint(0,6)
        if num == 0:
            new_block = create_square(self.canvas)
        elif num == 1:
            new_block = create_lshape1(self.canvas)
        elif num == 2:
            new_block = create_rectangle(self.canvas)
        elif num == 3:
            new_block = create_tshape(self.canvas)
        elif num == 4:
            new_block = create_zshape1(self.canvas)
        elif num == 5:
            new_block = create_lshape2(self.canvas)
        elif num == 6:
            new_block = create_zshape2(self.canvas)
        self.create_piece(new_block)

    def clear_lines(self):
        """Clear all filled lines and shift remaining blocks down."""
        cleared_rows = []

        # Identify full rows
        for row in range(18):
            if all(self.grid[row][col] is not None for col in range(10)):
                self.clear_line(row)
                cleared_rows.append(row)

        if cleared_rows:
            self.increase_score1(len(cleared_rows))
            self.shift_lines_down(cleared_rows)

    def end_soft_lock(self):
        if not self.can_move(0, cell_size):
            self.lock_piece(self.current_piece)
            self.falling = False
            self.check_game_state()
        self.soft_lock_active = False

    def shift_lines_down(self, cleared_rows):
        """
        Shift rows above cleared rows down by the total number of cleared rows.
        Handles multiple cleared rows correctly.
        """
        # Sort cleared rows in ascending order
        cleared_rows = sorted(cleared_rows)

        # Start from the highest row on the grid and move down
        for row in range(max(cleared_rows), -1, -1):
            # Calculate how many rows below have been cleared
            shift_by = sum(1 for cleared_row in cleared_rows if cleared_row > row)

            for col in range(10):
                block = self.grid[row][col]
                if block:
                    # Move block down by 'shift_by' rows
                    self.canvas.move(block.rect, 0, shift_by * cell_size)
                    # Update grid
                    self.grid[row + shift_by][col] = block
                    self.grid[row][col] = None


    def clear_line(self, row):
        """Clear the blocks in a row and remove them from the grid."""
        for col in range(10):
            block = self.grid[row][col]
            if block:  # If the cell contains a block
                self.canvas.delete(block.rect)  # Remove the block from the canvas
                self.grid[row][col] = None  # Remove the block from the grid

    def fall(self):
        if self.is_paused:
            return
        if self.falling:
            if self.can_move(0, cell_size):
                self.current_piece.move(0, cell_size)
                self.root.after(self.falling_timer, self.fall)
                self.increase_score()
            else:
                if not self.soft_lock_active:
                    self.soft_lock_active = True
                    self.root.after(self.soft_lock_time, self.end_soft_lock)
                else:
                    self.lock_piece(self.current_piece)
                    self.falling = False
                    self.root.after(100,self.check_game_state())

    def continuefalling(self):
        self.fall()
        self.falling = False
    
    def game_over(self):
        self.save_to_leaderboard(self.player_name, self.score.get())
        self.falling = False
        self.canvas.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text = "GAME OVER",
            font = ("Arial", 50),
            fill = "red",
            tags = "game_over"
        )
        self.root.after_cancel(self.falling_timer)  # Cancel the active timer
    
        # Disable input controls
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<Down>")
        self.root.unbind("<Up>")
        self.root.unbind("<space>")
        self.game_over_flag = True
        def switch_to_start_screen():
            from gui import create_start_gui
            canvas = self.root.winfo_children()  # This will get all the widgets in the root window
            for widget in canvas:
                if isinstance(widget, Canvas):
                    widget.destroy()  # Destroy the current canvas if it exists
            create_start_gui(self.root)
        self.root.after(3000, switch_to_start_screen)
        

    def save_to_leaderboard(self, player_name, score):
        """Saves the player's name and score to the leaderboard.json"""
        # Read the current leaderboard
        try:
            with open('leaderboard.json', 'r') as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = []  # If the file doesn't exist, start with an empty leaderboard

        # Add the new player's score to the leaderboard
        leaderboard.append({'name': player_name, 'score': score})

        # Sort the leaderboard by score in descending order
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)

        # Write the updated leaderboard back to the JSON file
        with open('leaderboard.json', 'w') as file:
            json.dump(leaderboard, file, indent=4)
    def pause_game(self):

        if not hasattr(self, "is_paused"):
            self.is_paused = False

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.root.after_cancel(self.falling_timer)
            # Create a pause overlay on the canvas
            self.pause_overlay = self.canvas.create_text(
                canvas_width // 2, 
                canvas_height // 2, 
                text="PAUSED", 
                font=("Arial", 50), 
                fill="red",
                tags="pause_text"
            )
        else:
            self.fall()
            self.canvas.delete("pause_text")
    def clear(self):
        """Clear all blocks from the grid and canvas without changing the score."""
        # Remove all blocks from the grid
        for row in range(18):
            for col in range(10):
                block = self.grid[row][col]
                if block:
                    self.canvas.delete(block.rect)  # Remove the block from the canvas
                    self.grid[row][col] = None  # Remove the block from the grid


