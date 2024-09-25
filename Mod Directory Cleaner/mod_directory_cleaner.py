import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def move_folders(target_folder, destination_folder, folder_names):
    for root, dirs, files in os.walk(target_folder):
        for dir_name in dirs:
            if dir_name.lower() in folder_names:
                src_dir = os.path.join(root, dir_name)
                base_name = dir_name
                dest_dir = os.path.join(destination_folder, base_name)
                
                count = 1
                while os.path.exists(dest_dir):
                    dest_dir = os.path.join(destination_folder, f"{base_name}_{count}")
                    count += 1

                shutil.move(src_dir, dest_dir)
                print(f"Moved '{src_dir}' to '{dest_dir}'")
    
    messagebox.showinfo("Operation Complete", "Folders moved successfully!")

def select_target_folder():
    target_folder.set(filedialog.askdirectory())

def select_destination_folder():
    destination_folder.set(filedialog.askdirectory())

def start_moving():
    if not target_folder.get() or not destination_folder.get():
        messagebox.showwarning("Input Required", "Please select both target and destination folders.")
        return
    
    move_folders(target_folder.get(), destination_folder.get(), set(folder_names.get().lower().split(',')))

def set_folder_names():
    folder_list = simpledialog.askstring("Set Folder Names", "Enter folder names to search for, separated by commas:")
    if folder_list:
        folder_names.set(folder_list)
    else:
        folder_names.set("backup,backups,concept,concepts")

# Set up the main window
root = tk.Tk()
root.title("Move Specified Folders")
root.geometry("450x250")

target_folder = tk.StringVar()
destination_folder = tk.StringVar()
folder_names = tk.StringVar(value="backup,backups,concept,concepts")

# Target Folder
tk.Label(root, text="Target Folder:").pack(pady=5)
tk.Entry(root, textvariable=target_folder, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=select_target_folder).pack(pady=5)

# Destination Folder
tk.Label(root, text="Destination Folder:").pack(pady=5)
tk.Entry(root, textvariable=destination_folder, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=select_destination_folder).pack(pady=5)

# Folder Names
tk.Label(root, text="Folder Names to Search:").pack(pady=5)
tk.Entry(root, textvariable=folder_names, width=50).pack(pady=5)
tk.Button(root, text="Set Folder Names", command=set_folder_names).pack(pady=5)

# Start Button
tk.Button(root, text="Start Moving", command=start_moving).pack(pady=20)

root.mainloop()
