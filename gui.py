from tkinter import *
from PIL import Image, ImageTk
from settings import cell_size, canvas_width, canvas_height, border_thickness
from game import *
from tkinter import *
from PIL import Image, ImageTk
from settings import cell_size, canvas_width, canvas_height, border_thickness

def create_start_gui(root):
    # Set the background color of the window to white
    root.configure(bg='white')

    # Create the canvas widget (fixed size, 410x730) and center it in the window
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#3B413C")
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the canvas in the window

    # Add text to the canvas
    canvas.create_text(
        canvas_width // 2, 80,  # Centered at the top
        text="Tetris",
        font=("Arial", 72, "bold"),
        fill="#94D1BE"
    )

    # Function to create buttons on the canvas
    def create_button(text, text_colour, command):
        button = Button(
            canvas, text=text, font=("Arial", 18),
            width=7,  # Reduced width to match title
            height=2,
            bg="#DAF0EE", fg=text_colour,
            activebackground="#A0D9C6", activeforeground="black",
            relief="flat",
            command=command
        )
        return button
    
    def ask_for_name(difficulty):
        # Create a new top-level window
        name_window = Toplevel(root)
        name_window.title("Enter Your Name")
        
        # Add a label and text entry widget
        Label(name_window, text="Enter your name:").pack(padx=20, pady=10)
        name_entry = Entry(name_window, width=20)
        name_entry.pack(padx=20, pady=10)
        
        # Define a variable to store the name
        player_name = ""
        
        # Function to confirm the name and start the game
        def on_start_game():
            nonlocal player_name  # Access the player_name variable outside the scope
            player_name = name_entry.get()
            if player_name:  # Ensure a name was entered
                name_window.destroy()  # Close the name input window
                start_game(player_name, difficulty)  # Call start_game with the player name
            else:
                Label(name_window, text="Please enter a name!", fg="red").pack(padx=20, pady=10)
        
        # Add a button to confirm the name and start the game
        start_button = Button(name_window, text="Start Game", command=on_start_game)
        start_button.pack(pady=10)

        name_window.mainloop()  # Start the Tkinter event loop for the name window

    def start_game(player_name, difficulty):
        if difficulty == "easy":
            falling_timer = 1000
        if difficulty == "medium":
            falling_timer = 800
        if difficulty == "hard":
            falling_timer = 600
        game = TetrisGame(root, falling_timer, player_name)
        create_game_gui(root, game, difficulty)
        game.falling = True
        game.create_new_piece()
        game.fall()
        canvas.place_forget()
    def show_leaderboard():
        canvas.place_forget()
        leaderboard_gui(root)
    def show_controls():
        canvas.place_forget()
        controls_gui(root)
    
    # Create buttons
    easy_button = create_button("Easy", "green", lambda: ask_for_name("easy"))
    medium_button = create_button("Medium", "orange", lambda: ask_for_name("medium"))
    hard_button = create_button("Hard", "red", lambda: ask_for_name("hard"))
    leaderboard_button = create_button("Leaderboard", "blue", show_leaderboard)
    controls_button = create_button("Controls", "purple", show_controls)

    # Function to center buttons
    def center_buttons():
        # Calculate button positions with spacing
        total_height = canvas_height
        button_height = 70  # Fixed height for each button
        button_width = 250  # Width matching title's approximate width
        spacing = 20  # Space between buttons

        # Calculate starting Y to center the buttons vertically
        total_buttons_height = 5 * button_height + 4 * spacing
        start_y = (total_height - total_buttons_height) // 2 + 50  # Shifted down by 50 pixels
        button_x = (canvas_width - button_width) // 2  # Center buttons horizontally

        easy_button.place(x=button_x, y=start_y, width=button_width, height=button_height)
        medium_button.place(x=button_x, y=start_y + button_height + spacing, width=button_width, height=button_height)
        hard_button.place(x=button_x, y=start_y + 2 * (button_height + spacing), width=button_width, height=button_height)
        leaderboard_button.place(x=button_x, y=start_y + 3 * (button_height + spacing), width=button_width, height=button_height)
        controls_button.place(x=button_x, y=start_y + 4 * (button_height + spacing), width=button_width, height=button_height)

    # Call center_buttons initially
    center_buttons()

    # Optional: Add a resize event handler if you want additional responsiveness
    def on_resize(event):
        center_buttons()
    
    root.bind("<Configure>", on_resize)

def create_game_gui(root, game, difficulty):

    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#3B413C")
    canvas.pack(padx=border_thickness, pady=border_thickness)
    
    # Create border around the canvas
    canvas.create_rectangle(
        -border_thickness, -border_thickness,
        canvas_width + border_thickness, canvas_height + border_thickness,
        outline="black", width=border_thickness
    )

    # Set up the game canvas and bind the game object
    game.set_canvas(canvas)
    
    # Draw UI elements


    # Draw the red line as a placeholder
    draw_red_line(canvas)

    # Set up key bindings for movement
    setup_key_bindings(root, game)



def draw_red_line(canvas):
    canvas.create_line(0, 200, 500, 200, fill="red", width=2)

def setup_key_bindings(root, game):
    def move_left(event):
        if game.can_move(-cell_size, 0):
            game.current_piece.move(-cell_size, 0)

    def move_right(event):
        if game.can_move(cell_size, 0): 
            game.current_piece.move(cell_size, 0)

    def move_down(event):
        if game.can_move(0, cell_size):
            game.current_piece.move(0, cell_size)
        else:
            game.check_game_state()

    def rotate_piece(event):
        if game.current_piece and hasattr(game.current_piece, 'rotate'):
            game.current_piece.rotate(game.grid)
    def pause(event):
        game.pause_game()
    def open_textbox(event):
        # Create a new top-level window for the text box
        textbox_window = Toplevel(root)
        textbox_window.title("Enter Command")
        
        # Add a label and text entry widget
        Label(textbox_window, text="Cheatcode").pack(padx=20, pady=10)
        command_entry = Entry(textbox_window, width=30)
        command_entry.pack(padx=20, pady=10)
        
        # Function to handle the submission of the command
        def submit_command():
            command = command_entry.get().strip()
            if command.lower() == "scoreadd":
                game.increase_score2(2000)  # Increase the score by 2000
                print("Score increased by 2000!")
            if command.lower() == "clear":
                game.clear()
            textbox_window.destroy()  # Close the text box window

        # Button to submit the command
        submit_button = Button(textbox_window, text="Submit", command=submit_command)
        submit_button.pack(pady=10)
        
        textbox_window.mainloop()

    def toggle_image(event):
        if not hasattr(game, 'image_shown'):  # Check if the attribute exists
            game.image_shown = False  # Initialize it if it doesn't exist

        if game.image_shown:
            # Close the image and unpause the game
            game.image_shown = False
            game.pause_game()  # Unpause the game
            game.canvas.delete("image")  # Remove the image from the canvas
        else:
            # Open the image and pause the game
            game.image_shown = True
            game.pause_game()  # Pause the game

            # Load and display the image
            img_path = "emailimage.webp"  # Path to your image file
            img = Image.open(img_path)
            img = img.resize((canvas_width, canvas_height))  # Resize image to canvas size
            img_tk = ImageTk.PhotoImage(img)

            # Create the image on the canvas
            game.canvas.create_image(canvas_width // 2, canvas_height // 2, image=img_tk, anchor=CENTER, tags="image")
            game.canvas.image = img_tk  # Keep a reference to the image to prevent garbage collection

    # Bind keys based on user-defined controls
    def load_controls():
        try:
            with open('controls.json', 'r') as json_file:
                controls = json.load(json_file)
            return controls
        except Exception as e:
            print(f"Error loading controls: {e}")
            return {}
    controls = load_controls()
    root.bind(controls.get("rotate", ""), rotate_piece)
    root.bind(controls.get("left", ""), move_left)
    root.bind(controls.get("right", ""), move_right)
    root.bind(controls.get("boss_key", ""), toggle_image)
    root.bind(controls.get("down", ""), move_down)
    root.bind(controls.get("pause", ""), pause)
    root.bind(controls.get("cheat_code", ""), open_textbox)



def leaderboard_gui(root):
    # Load leaderboard data from the JSON file
    try:
        with open("leaderboard.json", "r") as file:
            leaderboard_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard_data = []  # Default to an empty list if the file is missing or invalid

    # Sort the data by score in descending order
    sorted_leaderboard = sorted(leaderboard_data, key=lambda x: x["score"], reverse=True)

    # Get the top 10 entries
    top_10 = sorted_leaderboard[:10]


    # Create a canvas with the specified size
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="#3B413C")
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Add the title to the canvas
    canvas.create_text(205, 50, text="TOP 10", font=("Arial", 72, "bold"), fill="#94D1BE")

    # Display the top 10 scores on the canvas
    y_position = 120  # Starting y-position for the leaderboard entries
    for rank, entry in enumerate(top_10, start=1):
        name = entry["name"].upper()
        score = entry["score"]

        # Draw the rank, name, and score in separate columns
        canvas.create_text(50, y_position, text=f"{rank}.", font=("Atari", 18), fill="#94D1BE", anchor="w")  # Rank
        canvas.create_text(120, y_position, text=f"{name}", font=("Atari", 18), fill="#94D1BE", anchor="w")  # Name
        canvas.create_text(330, y_position, text=f"{score}", font=("Atari", 18), fill="#94D1BE", anchor="e")  # Score

        y_position += 55  # Move down for the next entry
    y_position = 120 + (len(top_10) * 55) + 20
    def go_back():
        # Destroy all widgets related to the leaderboard screen
        canvas.destroy()  # Remove the leaderboard canvas entirely
        for widget in root.winfo_children():
            if isinstance(widget, Button):
                widget.destroy()  # Remove any lingering buttons

        # Return to the start screen
        create_start_gui(root)

    back_button = Button(root, text="Back", font=("Arial", 14), command=go_back)
    back_button.place(relx=0.5, y=y_position, anchor=CENTER)

    # Bind resize event to reposition button
    def on_resize(event):
        # Recalculate Y position based on canvas position
        canvas_y = canvas.winfo_rooty() - root.winfo_rooty()
        new_y_position = canvas_y + 120 + (len(top_10) * 55) + 20
        back_button.place(relx=0.5, y=new_y_position, anchor=CENTER)

    root.bind("<Configure>", on_resize)

def controls_gui(root):
    # Create a frame with the same size as the canvas
    controls_frame = Frame(root, bg="#3B413C", width=canvas_width, height=canvas_height)
    controls_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center it in the root window

    # Title
    Label(controls_frame, text="Controls", font=("Arial", 24, "bold")).pack(pady=(20, 10))

    # Control labels and entry fields
    controls = [
        {"name": "Rotate", "key": "Up"},
        {"name": "Down", "key": "Down"},
        {"name": "Left", "key": "Left"},
        {"name": "Right", "key": "Right"},
        {"name": "Boss Key", "key": "G"},
        {"name": "Pause", "key": "P"},
        {"name": "Cheat Code", "key": "U"}
    ]

    # Dictionary to store Entry widgets for control input
    entries = {}

    # Layout for controls
    for control in controls:
        frame = Frame(controls_frame, bg="white")
        frame.pack(pady=5, fill=X, padx=40)
        
        # Control label
        Label(frame, text=f"{control['name']}: ", font=("Arial", 18), bg="white", anchor="w").pack(side=LEFT, padx=(0, 10))
        
        # Entry field (pre-filled with current key)
        entry = Entry(frame, font=("Arial", 18), width=5, justify='center')
        entry.pack(side=RIGHT)
        
        # Save entry for later use
        entries[control["name"].lower().replace(" ", "_")] = entry

    # Function to save custom controls
    def save_controls():
        # Collect updated controls from the entries
        new_controls = {control: entry.get().strip() for control, entry in entries.items()}

        # Validate keys (e.g., ensure they are single characters)
        for key, value in new_controls.items():
            if len(value) != 1:  # Ensure single-character input
                Label(controls_frame, text="Invalid key for controls. Please enter single keys.",
                      font=("Arial", 12), fg="red", bg="white").pack()
                return
        
        # Update key bindings dynamically (if needed)
        # Example: Pass `new_controls` to a function that updates game key bindings
        update_key_bindings(new_controls)

        # Return to main menu
        go_back()

    # Save button
    Button(controls_frame, text="Save", font=("Arial", 14), command=save_controls).pack(pady=(20, 10))

    # Back button
    def go_back():
        # Destroy controls frame and return to the start screen
        controls_frame.destroy()
        create_start_gui(root)

    Button(controls_frame, text="Back", font=("Arial", 14), command=go_back).pack(pady=(0, 10))
    
    def update_key_bindings(new_controls):
        try:
            with open('controls.json', 'w') as json_file:
                json.dump(new_controls, json_file, indent=4)
            print("Key bindings successfully updated and saved to controls.json.")
        except Exception as e:
            print(f"Error saving key bindings: {e}")






