import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import shutil

CONFIG_FILE = "config.json"

class FactionManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Faction Manager")

        self.config = self.load_config()
        self.builtin_ships_folder = self.config.get("builtin_ships_folder", "")
        self.tradeships_file = self.config.get("tradeships_file", "")
        self.tier_ranges = self.config.get("tier_ranges", [
            [1, 9, 50, 40],
            [3, 12, 60, 50],
            [6, 18, 70, 60],
            [12, 18, 80, 70]
        ])
        self.templates = self.config.get("templates", {
            "civilian": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Tags : ~/Tags [trade] }}\n',
            "combat": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Difficulty=2; Tags=[combat] }}\n',
            "defense": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Difficulty=1; }}\n',
            "station_trade": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  Tags : ~/Tags [trade_station]; StasisIcon="PLACEHOLDER.PNG" }}\n',
            "station_military": '\t:~{{ File="{ship}"; \t\t\t\tTier=1;  SpawnTier=3; Tags : ~/Tags [military_station]; StasisIcon="PLACEHOLDER.PNG" }}\n',
        })

        self.template_vars = {key: tk.StringVar(value=value) for key, value in self.templates.items()}
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

        self.sync_tradeships_button = tk.Button(root, text="Sync Trade Ships", command=self.sync_tradeships)
        self.sync_tradeships_button.pack()

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

        # Tradeships File Selection
        tradeships_file_frame = tk.LabelFrame(settings_window, text="Tradeships File")
        tradeships_file_frame.pack(fill="x", padx=5, pady=5)

        self.tradeships_file_label = tk.Label(tradeships_file_frame, text=f"Tradeships File: {self.tradeships_file}")
        self.tradeships_file_label.pack()

        select_tradeships_file_button = tk.Button(tradeships_file_frame, text="Select Tradeships File", command=self.select_tradeships_file)
        select_tradeships_file_button.pack()

        # Tier Ranges Editor
        tier_ranges_frame = tk.LabelFrame(settings_window, text="Tier Ranges (Format: min,max,StasisSpeed,StasisTradeTime)")
        tier_ranges_frame.pack(fill="x", padx=5, pady=5)

        self.tier_ranges_vars = []
        for i, tier_range in enumerate(self.tier_ranges):
            frame = tk.Frame(tier_ranges_frame)
            frame.pack(fill="x", padx=5, pady=2)

            label = tk.Label(frame, text=f"Range {i + 1}:")
            label.pack(side="left")

            range_var = tk.StringVar(value=f"{tier_range[0]},{tier_range[1]},{tier_range[2]},{tier_range[3]}")
            self.tier_ranges_vars.append(range_var)
            entry = tk.Entry(frame, textvariable=range_var, width=40)
            entry.pack(side="left", fill="x", expand=True)

        add_range_button = tk.Button(tier_ranges_frame, text="Add Tier Range", command=self.add_tier_range)
        add_range_button.pack(pady=5)

        save_button = tk.Button(settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def add_tier_range(self):
        frame = tk.Frame(self.tier_ranges_frame)
        frame.pack(fill="x", padx=5, pady=2)

        label = tk.Label(frame, text=f"Range {len(self.tier_ranges_vars) + 1}:")
        label.pack(side="left")

        range_var = tk.StringVar(value="0,0,0,0")
        self.tier_ranges_vars.append(range_var)
        entry = tk.Entry(frame, textvariable=range_var, width=40)
        entry.pack(side="left", fill="x", expand=True)

    def save_settings(self):
        self.config["builtin_ships_folder"] = self.builtin_ships_folder
        self.config["tradeships_file"] = self.tradeships_file
        self.tier_ranges = [list(map(int, var.get().split(','))) for var in self.tier_ranges_vars]
        self.config["tier_ranges"] = self.tier_ranges

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

    def select_tradeships_file(self):
        self.tradeships_file = filedialog.askopenfilename(title="Select Tradeships File", filetypes=[("Rules Files", "*.rules")])
        if self.tradeships_file:
            self.tradeships_file_label.config(text=f"Tradeships File: {self.tradeships_file}")
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

    def sync_tradeships(self):
        tradeships_manager = TradeShipsManager(self.config)
        tradeships_manager.compare_and_sync()
        messagebox.showinfo("Sync Complete", "Trade ships have been synchronized.")

class TradeShipsManager:
    def __init__(self, config):
        self.config = config
        self.tradeships_file = self.config.get("tradeships_file", "")
        self.tier_ranges = self.config.get("tier_ranges", [])
        self.civilian_ships_lists = self.load_civilian_ships_lists()
        self.tradeships_data = self.load_tradeships_list()

    def load_civilian_ships_lists(self):
        civilian_ships = {}
        if not self.config["builtin_ships_folder"]:
            return civilian_ships

        for faction in os.listdir(self.config["builtin_ships_folder"]):
            faction_path = os.path.join(self.config["builtin_ships_folder"], faction)
            if os.path.isdir(faction_path):
                for root, dirs, files in os.walk(faction_path):
                    for rules_file in [f for f in files if f.endswith(".rules")]:
                        with open(os.path.join(root, rules_file), "r") as f:
                            content = f.read()
                            if "Tags = [civilian]" in content:
                                faction_ships = []
                                lines = content.splitlines()
                                for line in lines:
                                    if "Tags : ~/Tags [trade]" in line:
                                        ship_name = line.split('File="')[1].split('";')[0]
                                        ship_name = ship_name.replace(".ship.png", "")  # Remove .ship.png for tradeships list
                                        tier = int(line.split('Tier=')[1].split(';')[0])
                                        faction_ships.append((ship_name, tier))
                                civilian_ships[faction] = faction_ships

        return civilian_ships

    def load_tradeships_list(self):
        tradeships_data = {}
        if not self.tradeships_file or not os.path.exists(self.tradeships_file):
            return tradeships_data

        with open(self.tradeships_file, "r") as file:
            content = file.read()
            lines = content.splitlines()
            current_faction = None
            for line in lines:
                if "// " in line:
                    current_faction = line.split("// ")[1].strip()
                    tradeships_data[current_faction] = []
                elif "ShipID=" in line and current_faction is not None:
                    ship_id = line.split('ShipID="')[1].split('"')[0]
                    tier_range = list(map(int, line.split('TierRange=[')[1].split(']')[0].split(',')))
                    tradeships_data[current_faction].append((ship_id, tier_range))

        return tradeships_data

    def compare_and_sync(self):
        missing_ships = self.find_missing_ships()
        if missing_ships:
            preview_changes = self.preview_changes(missing_ships)
            if preview_changes:
                self.create_backup()
                self.assign_tier_ranges(missing_ships)
                self.generate_and_append_entries(missing_ships)
        else:
            messagebox.showinfo("No Missing Ships", "All trade ships are already in the tradeships list.")

    def create_backup(self):
        if os.path.exists(self.tradeships_file):
            backup_file = self.tradeships_file.replace(".rules", "_backup.rules")
            shutil.copy(self.tradeships_file, backup_file)
            messagebox.showinfo("Backup Created", f"Backup created at {backup_file}")

    def preview_changes(self, missing_ships):
        preview_window = tk.Toplevel()
        preview_window.title("Preview Changes")

        preview_text = tk.Text(preview_window, wrap="word")
        preview_text.pack(fill="both", expand=True)

        for faction, ships in missing_ships.items():
            preview_text.insert(tk.END, f"Faction: {faction}\n")
            for ship, tier_range in ships:
                preview_text.insert(tk.END, f"  Ship: {ship}, Proposed TierRange: {tier_range}\n")

        confirm_button = tk.Button(preview_window, text="Confirm", command=preview_window.destroy)
        confirm_button.pack(pady=10)

        preview_window.wait_window(preview_window)

        return messagebox.askyesno("Apply Changes?", "Do you want to apply these changes?")

    def find_missing_ships(self):
        missing_ships = {}
        for faction, ships in self.civilian_ships_lists.items():
            if faction not in self.tradeships_data:
                missing_ships[faction] = ships
            else:
                existing_ship_ids = {ship[0] for ship in self.tradeships_data[faction]}
                missing_ships[faction] = [ship for ship in ships if ship[0] not in existing_ship_ids]

        return missing_ships

    def assign_tier_ranges(self, missing_ships):
        for faction, ships in missing_ships.items():
            for i, ship in enumerate(ships):
                tier = ship[1]
                best_range = self.get_best_tier_range(faction, tier)
                ships[i] = (ship[0], best_range)

    def get_best_tier_range(self, faction, tier):
        best_range = None
        min_count = float('inf')

        for tier_range in self.tier_ranges:
            if tier_range[0] <= tier <= tier_range[1]:
                count = sum(1 for ship in self.tradeships_data.get(faction, []) if ship[1] == tier_range)
                if count < min_count:
                    min_count = count
                    best_range = tier_range

        return best_range

    def generate_and_append_entries(self, missing_ships):
        with open(self.tradeships_file, "a") as file:
            for faction, ships in missing_ships.items():
                for i, (ship_name, tier_range) in enumerate(ships):
                    id_prefix = faction.split('.')[1].lower()[:3]
                    tier_max = tier_range[1]
                    next_letter = chr(97 + i % 26) + (chr(97 + i // 26) if i >= 26 else "")
                    ship_id = f"{id_prefix}_{tier_max}{next_letter}"

                    stasis_speed = tier_range[2]
                    stasis_trade_time = tier_range[3]

                    entry = f'\t{ship_id} : <./Data/modes/career/career.rules>/BaseTradeShip {{ ShipID="{ship_name}"; Faction={faction}; TierRange=[{tier_range[0]}, {tier_range[1]}]; StasisSpeed={stasis_speed}; StasisTradeTime={stasis_trade_time}; }}\n'
                    file.write(f'\t// {faction}\n' if i == 0 else "")
                    file.write(entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = FactionManagerApp(root)
    root.mainloop()
