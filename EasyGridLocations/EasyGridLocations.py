import tkinter as tk
from tkinter import messagebox

# Step 1: Initialize the Tkinter window with larger size and centered layout
root = tk.Tk()
root.title("Cosmoteer Modding Tool")
root.geometry('600x400')  # Set a bigger window size

# Create labels and entry fields for X and Y size inputs
label_x = tk.Label(root, text="X Size:", font=("Arial", 12))
label_x.grid(row=0, column=0, padx=20, pady=10, sticky="w")
entry_x = tk.Entry(root, font=("Arial", 12))
entry_x.grid(row=0, column=1, padx=20, pady=10)

label_y = tk.Label(root, text="Y Size:", font=("Arial", 12))
label_y.grid(row=1, column=0, padx=20, pady=10, sticky="w")
entry_y = tk.Entry(root, font=("Arial", 12))
entry_y.grid(row=1, column=1, padx=20, pady=10)

# Button to submit the size and create the grid
def submit_size():
    try:
        x_size = int(entry_x.get())
        y_size = int(entry_y.get())
        create_grid(x_size, y_size)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers for X and Y size.")

submit_button = tk.Button(root, text="Submit Size", command=submit_size, font=("Arial", 12), bg="lightblue")
submit_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

# Step 2: Create a grid with perimeter for door locations and show a key
def create_grid(x_size, y_size):
    # Create a new window for the grid
    grid_window = tk.Toplevel(root)
    grid_window.title(f"Grid Editor for {x_size}x{y_size} Part")

    # Get the screen dimensions and center the window
    screen_width = grid_window.winfo_screenwidth()
    screen_height = grid_window.winfo_screenheight()
    window_width = 100 * (x_size + 2)
    window_height = 100 * (y_size + 3)
    pos_x = (screen_width // 2) - (window_width // 2)
    pos_y = (screen_height // 2) - (window_height // 2)
    grid_window.geometry(f"{window_width}x{window_height}+{pos_x}+{pos_y}")  # Centered window

    # Create a list to hold the button states for blocked cells and doors
    grid_buttons = [[None for _ in range(x_size + 2)] for _ in range(y_size + 2)]

    # Create the buttons for each grid cell
    for y in range(y_size + 2):
        for x in range(x_size + 2):
            if x == 0 or x == x_size + 1 or y == 0 or y == y_size + 1:
                # Edge cells (door locations)
                display_x = x - 1  # Adjust label for correct coordinate system
                display_y = y - 1
                btn_door = tk.Button(grid_window, text=f"[{display_x},{display_y}]", bg="green", width=8, height=2,
                                     command=lambda x=x, y=y: toggle_door(x, y, grid_buttons))
                btn_door.grid(row=y, column=x)
                grid_buttons[y][x] = btn_door
            else:
                # Internal cells (blocked or unblocked)
                btn_block = tk.Button(grid_window, text=f"[{x-1},{y-1}]", bg="white", width=8, height=2,
                                      command=lambda x=x, y=y: toggle_block(x, y, grid_buttons))
                btn_block.grid(row=y, column=x)
                grid_buttons[y][x] = btn_block

    # Button to generate the final code after grid interaction
    generate_button = tk.Button(grid_window, text="Generate Code", command=lambda: generate_code(x_size, y_size, grid_buttons))
    generate_button.grid(row=y_size + 2, column=0, columnspan=x_size + 2)

    # Add a color key at the bottom of the grid window
    key_text = """
    Color Key:
    - White: Internal cell (unblocked)
    - Gray: Blocked travel cell (non-traversable)
    - Green: Enabled door location
    - Red: Disabled door location
    """
    key_label = tk.Label(grid_window, text=key_text, font=("Arial", 10), justify="left", anchor="w")
    key_label.grid(row=y_size + 3, column=0, columnspan=x_size + 2, sticky="w", padx=10, pady=10)

# Step 3: Toggle block state (internal cells)
def toggle_block(x, y, grid_buttons):
    btn = grid_buttons[y][x]
    if btn.cget("bg") == "white":
        btn.config(bg="gray")  # Blocked travel cell
    else:
        btn.config(bg="white")  # Unblocked travel cell

# Step 4: Toggle door state (perimeter cells)
def toggle_door(x, y, grid_buttons):
    btn = grid_buttons[y][x]
    if btn.cget("bg") == "green":
        btn.config(bg="red")  # Disabled door location
    else:
        btn.config(bg="green")  # Enabled door location

# Step 5: Generate the output code based on user interaction
def generate_code(x_size, y_size, grid_buttons):
    # Initialize empty lists for the arrays
    blocked_cells = []
    door_locations = []
    phys_rect = f"size = [{x_size}, {y_size}]"

    # Process the blocked travel cells
    for y in range(1, y_size + 1):
        for x in range(1, x_size + 1):
            if grid_buttons[y][x].cget("bg") == "gray":
                blocked_cells.append(f"[{x - 1}, {y - 1}]")
            else:
                blocked_cells.append(f"/* [{x - 1}, {y - 1}] */")  # Commented out by default

    # Process door locations for all perimeter cells
    for x in range(x_size + 2):
        if grid_buttons[0][x].cget("bg") == "green":
            door_locations.append(f"[{x - 1}, -1]")  # Top edge
        if grid_buttons[y_size + 1][x].cget("bg") == "green":
            door_locations.append(f"[{x - 1}, {y_size}]")  # Bottom edge

    for y in range(1, y_size + 1):
        if grid_buttons[y][0].cget("bg") == "green":
            door_locations.append(f"[-1, {y - 1}]")  # Left edge
        if grid_buttons[y][x_size + 1].cget("bg") == "green":
            door_locations.append(f"[{x_size}, {y - 1}]")  # Right edge

    # Generate the final output code
    output_code = f"""
size = [{x_size}, {y_size}]

BlockedTravelCells
[
    {" ".join(blocked_cells)}
]

AllowedDoorLocations
[
    {" ".join(door_locations)}
]

PhysRects
[
    {phys_rect}
]
"""
    # Display the output code in a message box
    messagebox.showinfo("Generated Code", output_code)

# Run the Tkinter main loop
root.mainloop()
