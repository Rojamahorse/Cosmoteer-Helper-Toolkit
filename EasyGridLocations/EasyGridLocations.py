import tkinter as tk
from tkinter import messagebox

# Step 1: Initialize the Tkinter window
root = tk.Tk()
root.title("Cosmoteer Modding Tool")

# Create labels and entry fields for X and Y size inputs
label_x = tk.Label(root, text="X Size:")
label_x.grid(row=0, column=0)
entry_x = tk.Entry(root)
entry_x.grid(row=0, column=1)

label_y = tk.Label(root, text="Y Size:")
label_y.grid(row=1, column=0)
entry_y = tk.Entry(root)
entry_y.grid(row=1, column=1)

# Button to submit the size and create the grid
def submit_size():
    try:
        x_size = int(entry_x.get())
        y_size = int(entry_y.get())
        create_grid(x_size, y_size)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid integers for X and Y size.")

submit_button = tk.Button(root, text="Submit Size", command=submit_size)
submit_button.grid(row=2, column=0, columnspan=2)

def create_grid(x_size, y_size):
    # Create a new window for the grid
    grid_window = tk.Toplevel(root)
    grid_window.title(f"Grid Editor for {x_size}x{y_size} Part")

    # Create a list to hold the button states for blocked cells and doors
    grid_buttons = [[None for _ in range(x_size)] for _ in range(y_size)]

    # Create the buttons for each grid cell
    for y in range(y_size):
        for x in range(x_size):
            # Create a button for the travel cells (blocked or unblocked)
            btn_block = tk.Button(grid_window, text=f"[{x},{y}]",
                                  bg="white", width=10, height=2,
                                  command=lambda x=x, y=y: toggle_block(x, y, grid_buttons))
            btn_block.grid(row=y, column=x)

            # Save the button reference
            grid_buttons[y][x] = btn_block

    # Button to generate the final code after grid interaction
    generate_button = tk.Button(grid_window, text="Generate Code", command=lambda: generate_code(x_size, y_size, grid_buttons))
    generate_button.grid(row=y_size, column=0, columnspan=x_size)

def toggle_block(x, y, grid_buttons):
    # Toggle the button color and state to indicate block or unblocked
    btn = grid_buttons[y][x]
    if btn.cget("bg") == "white":
        btn.config(bg="gray")  # Blocked travel cell
    else:
        btn.config(bg="white")  # Unblocked travel cell

def generate_code(x_size, y_size, grid_buttons):
    # Initialize empty lists for the arrays
    blocked_cells = []
    door_locations = []
    phys_rect = f"size = [{x_size}, {y_size}]"

    # Process the blocked travel cells
    for y in range(y_size):
        for x in range(x_size):
            if grid_buttons[y][x].cget("bg") == "gray":
                blocked_cells.append(f"[{x}, {y}]")
            else:
                blocked_cells.append(f"/* [{x}, {y}] */")  # Commented out by default

    # Process door locations (all edges enabled by default)
    for x in range(x_size):
        door_locations.append(f"[{x}, 0]")  # Top edge
        door_locations.append(f"[{x}, {y_size-1}]")  # Bottom edge

    for y in range(1, y_size - 1):
        door_locations.append(f"[0, {y}]")  # Left edge
        door_locations.append(f"[{x_size-1}, {y}]")  # Right edge

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
