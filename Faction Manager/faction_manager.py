import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json

CONFIG_FILE = "config.json"

class FactionManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Faction Manager")

        self.config = self.load_config()
        self.builtin_ships_folder = self.config.get("builtin_ships_folder", "")
        self.templates = self.config.get("templates", {
            "civilian": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Tags : ~/Tags [trade] }}\n',
            "combat": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Difficulty=2; Tags=[combat] }}\n',
            "defense": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Difficulty=1; }}\n',
            "station_trade": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Tags : ~/Tags [trade_station]; StasisIcon="PLACEHOLDER.PNG" }}\n',
            "station_military": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  SpawnTier=3; Tags : ~/Tags [military_station]; StasisIcon="PLACEHOLDER.PNG" }}\n',
        })

        self.unlisted_ships = {}

        # UI Elements
        self.settings_button = tk.Button(root, text="Settings", command=self.open_settings)
        self.settings_button.pack()

        self.scan_button = tk.Button(root, text="Scan for New Ships", command=self.scan_for_new_ships, state=tk.NORMAL if self.builtin_ships_folder else tk.DISABLED)
        self.scan_button.pack()

        self.ship_listbox = tk.Listbox(root, width=80, height=20)
        self.ship_listbox.pack()

        self.create_entries_button = tk.Button(root, text="Create Entries for Selected Ships", command=self.create_entries, state=tk.DISABLED)
        self.create_entries_button.pack()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        # Directory Selection
        directory_frame = tk.LabelFrame(settings_window, text="Directory")
        directory_frame.pack(fill="x", padx=5, pady=5)

        self.default_path_label = tk.Label(directory_frame, text=f"Default Path: {self.builtin_ships_folder}")
        self.default_path_label.pack()

        select_directory_button = tk.Button(directory_frame, text="Select Directory", command=self.select_builtin_ships_folder)
        select_directory_button.pack()

        # Template Editor
        template_frame = tk.LabelFrame(settings_window, text="Templates")
        template_frame.pack(fill="x", padx=5, pady=5)

        self.template_vars = {}
        for template_name, template_value in self.templates.items():
            frame = tk.Frame(template_frame)
            frame.pack(fill="x", padx=5, pady=2)
            
            label = tk.Label(frame, text=f"{template_name.capitalize()}:")
            label.pack(side="left")
            
            entry_var = tk.StringVar(value=template_value)
            self.template_vars[template_name] = entry_var
            entry = tk.Entry(frame, textvariable=entry_var, width=100)
            entry.pack(side="left", fill="x", expand=True)
        
        save_button = tk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        self.config["builtin_ships_folder"] = self.builtin_ships_folder
        for template_name, template_var in self.template_vars.items():
            self.templates[template_name] = template_var.get()

        self.config["templates"] = self.templates
        self.save_config()

        messagebox.showinfo("Settings Saved", "Settings have been successfully saved.")

    def select_builtin_ships_folder(self):
        self.builtin_ships_folder = filedialog.askdirectory(title="Select Builtin Ships Folder")
        if self.builtin_ships_folder:
            self.default_path_label.config(text=f"Default Path: {self.builtin_ships_folder}")
            self.save_settings()

    def scan_for_new_ships(self):
        self.unlisted_ships = self.get_unlisted_ships()
        self.ship_listbox.delete(0, tk.END)
        if self.unlisted_ships:
            for faction, ships in self.unlisted_ships.items():
                for ship_info in ships:
                    ship, rules_file = ship_info
                    self.ship_listbox.insert(tk.END, f"{faction} - {ship} (in {rules_file})")
            self.create_entries_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("No New Ships", "All ships are already listed in the .rules files.")

    def get_unlisted_ships(self):
        unlisted_ships = {}
        if not self.builtin_ships_folder:
            return unlisted_ships

        for faction in os.listdir(self.builtin_ships_folder):
            faction_path = os.path.join(self.builtin_ships_folder, faction)
            if os.path.isdir(faction_path):
                for root, dirs, files in os.walk(faction_path):
                    rules_files = [f for f in files if f.endswith(".rules")]

                    if not rules_files:
                        continue

                    for ship_file in [f for f in files if f.endswith(".png") and ".ship" in f]:
                        ship_listed = False
                        for rules_file in rules_files:
                            with open(os.path.join(root, rules_file), "r") as f:
                                rules_content = f.read()
                                if f'File="{ship_file}"' in rules_content:
                                    ship_listed = True
                                    break
                        if not ship_listed:
                            relative_rules_file_path = os.path.relpath(os.path.join(root, rules_files[0]), faction_path) if rules_files else None
                            if faction not in unlisted_ships:
                                unlisted_ships[faction] = []
                            unlisted_ships[faction].append((ship_file, relative_rules_file_path))

        return unlisted_ships

    def create_entries(self):
        selected_ships = [self.ship_listbox.get(idx) for idx in self.ship_listbox.curselection()]

        if not selected_ships:
            messagebox.showwarning("No Ships Selected", "Please select at least one ship to create entries.")
            return

        for ship_info in selected_ships:
            try:
                faction, ship_details = ship_info.split(" - ", 1)
                if " (in " in ship_details:
                    ship, rules_file = ship_details.split(" (in ")
                    rules_file = rules_file.rstrip(")")
                else:
                    raise ValueError(f"Unexpected format for ship details: {ship_details}")

                entry = self.create_entry(faction, rules_file, ship)

                self.append_to_rules_file(faction, rules_file, entry)
            except ValueError as e:
                messagebox.showerror("Error", f"Failed to process entry for: {ship_info}\nError: {str(e)}")

        messagebox.showinfo("Entries Created", "Entries for selected ships have been created.")
        self.scan_for_new_ships()

    def create_entry(self, faction, rules_file, ship):
        rules_file_path = os.path.join(self.builtin_ships_folder, faction, rules_file)
        with open(rules_file_path, "r") as f:
            content = f.read()

        if "Tags = [civilian]" in content:
            return self.templates["civilian"].format(ship=ship)
        elif "Tags = [defense]" in content:
            return self.templates["defense"].format(ship=ship)
        elif "Tags = [station]" in content:
            if "military" in rules_file.lower():
                return self.templates["station_military"].format(ship=ship)
            else:
                return self.templates["station_trade"].format(ship=ship)
        else:  # Default to combat tags if none of the above matches
            return self.templates["combat"].format(ship=ship)

    def append_to_rules_file(self, faction, rules_file, entry):
        rules_file_path = os.path.join(self.builtin_ships_folder, faction, rules_file)

        with open(rules_file_path, "r") as f:
            content = f.readlines()

        insertion_index = None
        for i, line in enumerate(content):
            if "Ships" in line:
                insertion_index = i + 2
                break

        if insertion_index is None:
            messagebox.showerror("Error", f"Could not find the 'Ships' section in {rules_file_path}")
            return

        content.insert(insertion_index, entry)

        with open(rules_file_path, "w") as f:
            f.writelines(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = FactionManagerApp(root)
    root.mainloop()
