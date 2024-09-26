import tkinter as tk
from tkinter import colorchooser
from PIL import Image, ImageDraw

def choose_color():
    color_code = colorchooser.askcolor(title ="Choose color")
    return color_code[1]

def generate_tile(shape, inner_color, border_color, rivet_colors, rivet_shadow_color):
    # Placeholder function to generate the armor tile
    # Implement the drawing logic here using the colors provided by the UI
    pass

def create_ui():
    root = tk.Tk()
    root.title("Armor Tile Generator")

    # Shape selection
    tk.Label(root, text="Select Shape").grid(row=0, column=0)
    shape_var = tk.StringVar(value="shape1")
    tk.OptionMenu(root, shape_var, "shape1", "shape2", "shape3").grid(row=0, column=1)

    # Inner edge color
    tk.Label(root, text="Inner Edge Color").grid(row=1, column=0)
    inner_color_btn = tk.Button(root, text="Choose", command=lambda: choose_color())
    inner_color_btn.grid(row=1, column=1)

    # Border color
    tk.Label(root, text="2px Border Color").grid(row=2, column=0)
    border_color_btn = tk.Button(root, text="Choose", command=lambda: choose_color())
    border_color_btn.grid(row=2, column=1)

    # Rivet color
    tk.Label(root, text="Rivet Color").grid(row=3, column=0)
    rivet_color_btn = tk.Button(root, text="Choose", command=lambda: choose_color())
    rivet_color_btn.grid(row=3, column=1)

    # Rivet shadow color
    tk.Label(root, text="Rivet Shadow Color").grid(row=4, column=0)
    rivet_shadow_color_btn = tk.Button(root, text="Choose", command=lambda: choose_color())
    rivet_shadow_color_btn.grid(row=4, column=1)

    # Button to generate the tile
    tk.Button(root, text="Generate Tile", command=lambda: generate_tile(
        shape_var.get(),
        inner_color_btn['bg'],  # Use selected colors
        border_color_btn['bg'],
        rivet_color_btn['bg'],
        rivet_shadow_color_btn['bg']
    )).grid(row=5, column=0, columnspan=2)

    root.mainloop()

create_ui()
