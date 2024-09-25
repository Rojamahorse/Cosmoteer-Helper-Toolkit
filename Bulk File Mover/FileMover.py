import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def select_folder(title):
    folder_selected = filedialog.askdirectory(title=title)
    return folder_selected

def move_files(target_folder, backup_folder, file_names):
    # Check if the backup folder exists, if not, create it
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    
    file_names = [file.strip() for file in file_names.split(",")]  # Strip any extra spaces and split by comma
    for root, _, files in os.walk(target_folder):
        for file in files:
            if file in file_names:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(backup_folder, file)
                
                # Handle duplicate files by renaming
                if os.path.exists(destination_file):
                    base_name, ext = os.path.splitext(file)
                    count = 1
                    new_file_name = f"{base_name}_{count}{ext}"
                    while os.path.exists(os.path.join(backup_folder, new_file_name)):
                        count += 1
                        new_file_name = f"{base_name}_{count}{ext}"
                    destination_file = os.path.join(backup_folder, new_file_name)
                
                shutil.move(source_file, destination_file)
                print(f"Moved {source_file} to {destination_file}")
    
    messagebox.showinfo("Success", "Files moved successfully!")

def start_process():
    target_folder = select_folder("Select Target Folder")
    if not target_folder:
        return
    
    backup_folder = select_folder("Select Backup Folder")
    if not backup_folder:
        return
    
    file_names = simpledialog.askstring("File Names", "Enter file names with extensions, separated by commas:")
    if not file_names:
        return
    
    move_files(target_folder, backup_folder, file_names)

# Create the GUI window
root = tk.Tk()
root.title("File Mover")
root.geometry("300x150")

# Create buttons
select_button = tk.Button(root, text="Start Process", command=start_process)
select_button.pack(pady=20)

# Start the Tkinter loop
root.mainloop()
