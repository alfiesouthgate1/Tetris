from tkinter import Canvas
from settings import cell_size

class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color)

    def move(self, dx, dy):
        self.canvas.move(self.rect, dx, dy)

class Piece:
    def __init__(self, canvas, blocks):
        self.canvas = canvas
        self.blocks = blocks

    def move(self, dx, dy):
        for block in self.blocks:
            block.move(dx, dy)

    def rotate(self, grid):
        # Get the coordinates of the center block (pivot point)
        center_x, center_y = self.canvas.coords(self.blocks[0].rect)[:2]

        # Compute the new positions for all blocks after rotation
        new_positions = []
        for block in self.blocks:
            x, y = self.canvas.coords(block.rect)[:2]
            new_x = center_x - (y - center_y)
            new_y = center_y + (x - center_x)
            new_positions.append((new_x, new_y))

        # Check if the new positions are valid
        for new_x, new_y in new_positions:
            new_col = int(new_x // cell_size)
            new_row = int(new_y // cell_size)

            # Check if the position is out of bounds
            if new_col < 0 or new_col >= len(grid[0]) or new_row < 0 or new_row >= len(grid):
                return  # Cancel rotation if out of bounds

            # Check if the position is occupied by another block
            if grid[new_row][new_col] is not None:
                return  # Cancel rotation if position is occupied

        # Apply the rotation if all positions are valid
        for block, (new_x, new_y) in zip(self.blocks, new_positions):
            self.canvas.coords(
                block.rect,
                new_x,
                new_y,
                new_x + cell_size,
                new_y + cell_size
            )

