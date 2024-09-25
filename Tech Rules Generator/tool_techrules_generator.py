import tkinter as tk
from tkinter import messagebox, filedialog
import pyperclip
import os
import configparser
import re

class TechRulesGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TechRules Generator")
        self.geometry("1000x1200")  # Increased window size for better layout

        # Initialize configuration
        self.config_file = "config.ini"
        self.config = configparser.ConfigParser()
        self.load_config()

        # Step 1: Select Mod Root (mod.rules File)
        self.setup_mod_root_selection()

        # Step 2: Generate TechRules File
        self.setup_generate_techrules_button()

        # Step 3: Select TechRules and Part Files
        self.setup_file_selection()

        # Step 4: Parse Part File for ID and EditorGroups
        self.setup_part_parsing()

        # Step 5: Choose Unlock Type
        self.setup_unlock_type_selection()

        # Placeholder for dynamic fields
        self.dynamic_fields = {}

        # Load previously saved paths and author name if available
        self.load_saved_paths()

        # Button to show TechRules readout
        self.setup_show_techrules_button()

        # Advanced Prerequisites Feature
        self.prerequisite_ids = []
        self.setup_advanced_prerequisites()

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config['Paths'] = {}
            self.config['Prerequisites'] = {}

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def setup_mod_root_selection(self):
        # Mod Root Selection
        self.mod_root_label = tk.Label(self, text="Select your mod.rules file (Mod Root Directory):")
        self.mod_root_label.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=(10, 0))

        self.mod_root_entry = tk.Entry(self, width=80)
        self.mod_root_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.mod_root_browse_button = tk.Button(self, text="Browse", command=self.browse_mod_root)
        self.mod_root_browse_button.grid(row=1, column=2, padx=10, pady=5)

        # Help text for Mod Root
        self.mod_root_help_label = tk.Label(self, text="Example: Select the mod.rules file located at your mod's root directory.")
        self.mod_root_help_label.grid(row=2, column=0, columnspan=3, sticky='w', padx=10)

    def setup_generate_techrules_button(self):
        self.generate_techrules_button = tk.Button(self, text="Generate techs.rules File", command=self.generate_techs_rules, state='disabled')
        self.generate_techrules_button.grid(row=3, column=0, columnspan=3, pady=10)

    def setup_file_selection(self):
        # TechRules File Selection
        self.techrules_label = tk.Label(self, text="Select the TechRules file:")
        self.techrules_label.grid(row=4, column=0, columnspan=3, sticky='w', padx=10, pady=(10, 0))

        self.techrules_entry = tk.Entry(self, width=80)
        self.techrules_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.techrules_browse_button = tk.Button(self, text="Browse", command=self.browse_techrules, state='disabled')
        self.techrules_browse_button.grid(row=5, column=2, padx=10, pady=5)

        # Help text for TechRules path
        self.techrules_help_label = tk.Label(self, text="Example: modes/career/techs.rules or any other .rules file")
        self.techrules_help_label.grid(row=6, column=0, columnspan=3, sticky='w', padx=10)

        # Part File Selection
        self.part_label = tk.Label(self, text="Select the Part file:")
        self.part_label.grid(row=7, column=0, columnspan=3, sticky='w', padx=10, pady=(20, 0))

        self.part_entry = tk.Entry(self, width=80)
        self.part_entry.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        self.part_browse_button = tk.Button(self, text="Browse", command=self.browse_part, state='disabled')
        self.part_browse_button.grid(row=8, column=2, padx=10, pady=5)

        # Help text for Part path
        self.part_help_label = tk.Label(self, text="Example: ships/terran/weapons/small/discordmissile/dm_launcher.rules")
        self.part_help_label.grid(row=9, column=0, columnspan=3, sticky='w', padx=10)

    def setup_part_parsing(self):
        # Labels for Part ID and EditorGroups
        self.part_id_label = tk.Label(self, text="Part ID (auto-generated from Part file):")
        self.part_id_label.grid(row=10, column=0, sticky='e', padx=10, pady=(20, 0))

        self.part_id_entry = tk.Entry(self, width=80, state='readonly')
        self.part_id_entry.grid(row=10, column=1, columnspan=2, padx=10, pady=(20, 0))

        self.editorgroups_label = tk.Label(self, text="Editor Groups:")
        self.editorgroups_label.grid(row=11, column=0, sticky='ne', padx=10, pady=(10, 0))

        self.editorgroups_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, width=60, height=10)
        self.editorgroups_listbox.grid(row=11, column=1, columnspan=2, padx=10, pady=(10, 0))

        self.editorgroups_help_label = tk.Label(self, text="Select one or more Editor Groups from the Part file.")
        self.editorgroups_help_label.grid(row=12, column=0, columnspan=3, sticky='w', padx=10)

    def setup_unlock_type_selection(self):
        # Unlock Type Selection
        self.type_label = tk.Label(self, text="Is this a Part or a Toggle Choice unlock?")
        self.type_label.grid(row=13, column=0, columnspan=3, sticky='w', padx=10, pady=(20, 0))

        self.part_button = tk.Button(self, text="Part", width=20, command=lambda: self.setup_fields('Part'), state='disabled')
        self.part_button.grid(row=14, column=0, padx=10, pady=10)

        self.togglechoice_button = tk.Button(self, text="Toggle Choice", width=20, command=lambda: self.setup_fields('ToggleChoice'), state='disabled')
        self.togglechoice_button.grid(row=14, column=1, padx=10, pady=10)

        self.reset_button = tk.Button(self, text="Reset", width=20, command=self.reset_fields)
        self.reset_button.grid(row=14, column=2, padx=10, pady=10)

    def setup_show_techrules_button(self):
        self.show_techrules_button = tk.Button(self, text="Show TechRules Readout", command=self.show_techrules, state='disabled')
        self.show_techrules_button.grid(row=15, column=0, columnspan=3, pady=20)

    def setup_advanced_prerequisites(self):
        self.advanced_prereq_button = tk.Button(self, text="Advanced Prerequisite Selection", command=self.open_prerequisite_dialog, state='disabled')
        self.advanced_prereq_button.grid(row=16, column=0, columnspan=3, pady=10)

    def load_saved_paths(self):
        if self.config.has_section('Paths'):
            if self.config.has_option('Paths', 'mod_root'):
                mod_root = self.config.get('Paths', 'mod_root')
                self.mod_root_entry.insert(0, os.path.join(mod_root, 'mod.rules'))
                # Enable dependent buttons
                self.generate_techrules_button.config(state='normal')
                self.techrules_browse_button.config(state='normal')
                self.part_browse_button.config(state='normal')
                self.part_button.config(state='normal')
                self.togglechoice_button.config(state='normal')
                self.show_techrules_button.config(state='normal')
                self.advanced_prereq_button.config(state='normal')
            if self.config.has_option('Paths', 'techrules_path'):
                self.techrules_entry.insert(0, self.config.get('Paths', 'techrules_path'))
            if self.config.has_option('Paths', 'part_id'):
                self.part_id_entry.config(state='normal')
                self.part_id_entry.delete(0, tk.END)
                self.part_id_entry.insert(0, self.config.get('Paths', 'part_id'))
                self.part_id_entry.config(state='readonly')
            if self.config.has_option('Paths', 'editorgroups'):
                # Populate the listbox with saved editor groups
                editorgroups = self.config.get('Paths', 'editorgroups').split(',')
                for group in editorgroups:
                    self.editorgroups_listbox.insert(tk.END, group)
                # Select all editor groups by default
                self.editorgroups_listbox.select_set(0, tk.END)

    def browse_mod_root(self):
        file_path = filedialog.askopenfilename(
            title="Select mod.rules File",
            filetypes=[("Rules Files", "mod.rules"), ("All Files", "*.*")]
        )
        if file_path:
            if not os.path.basename(file_path).lower() == 'mod.rules':
                messagebox.showerror("Error", "Selected file is not 'mod.rules'. Please select the correct file.")
                return
            mod_root = os.path.dirname(os.path.abspath(file_path))
            self.mod_root_entry.delete(0, tk.END)
            self.mod_root_entry.insert(0, file_path)
            self.config['Paths']['mod_root'] = mod_root
            self.save_config()
            # Enable dependent buttons
            self.generate_techrules_button.config(state='normal')
            self.techrules_browse_button.config(state='normal')
            self.part_browse_button.config(state='normal')
            self.part_button.config(state='normal')
            self.togglechoice_button.config(state='normal')
            self.show_techrules_button.config(state='normal')
            self.advanced_prereq_button.config(state='normal')

    def browse_techrules(self):
        mod_root = self.config.get('Paths', 'mod_root', fallback=None)
        initial_dir = mod_root if mod_root else '/'
        file_path = filedialog.askopenfilename(
            title="Select TechRules File",
            filetypes=[("Rules Files", "*.rules"), ("All Files", "*.*")],
            initialdir=initial_dir
        )
        if file_path:
            self.techrules_entry.delete(0, tk.END)
            self.techrules_entry.insert(0, file_path)
            self.config['Paths']['techrules_path'] = file_path
            self.save_config()

    def browse_part(self):
        mod_root = self.config.get('Paths', 'mod_root', fallback=None)
        initial_dir = mod_root if mod_root else '/'
        file_path = filedialog.askopenfilename(
            title="Select Part File",
            filetypes=[("Rules Files", "*.rules"), ("All Files", "*.*")],
            initialdir=initial_dir
        )
        if file_path:
            self.part_entry.delete(0, tk.END)
            self.part_entry.insert(0, file_path)
            self.parse_part_file()

    def parse_part_file(self):
        """Parse the selected Part file to extract ID and EditorGroups."""
        part_path = self.part_entry.get()
        if not part_path:
            return

        if not os.path.exists(part_path):
            messagebox.showerror("Error", f"Part file does not exist at: {part_path}")
            return

        try:
            with open(part_path, 'r') as file:
                content = file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Part file: {e}")
            return

        # Parse Part ID
        part_id = self.extract_field(content, 'ID')
        if part_id:
            self.part_id_entry.config(state='normal')
            self.part_id_entry.delete(0, tk.END)
            self.part_id_entry.insert(0, part_id)
            self.part_id_entry.config(state='readonly')
            self.config['Paths']['part_id'] = part_id
            self.save_config()
        else:
            messagebox.showerror("Error", "Failed to extract 'ID' from Part file.")
            return

        # Parse EditorGroups
        editorgroups = self.extract_editorgroups(content)
        if editorgroups:
            self.editorgroups_listbox.delete(0, tk.END)
            for group in editorgroups:
                self.editorgroups_listbox.insert(tk.END, group)
            # Save editor groups to config
            self.config['Paths']['editorgroups'] = ','.join(editorgroups)
            self.save_config()
            # Select all editor groups by default
            self.editorgroups_listbox.select_set(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to extract 'EditorGroup' or 'EditorGroups' from Part file.")

    def extract_field(self, content, field_name):
        """Extract the value of a given field from the content."""
        pattern = rf"^\s*{field_name}\s*=\s*\"?([^\n\"]+)\"?"
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            # Return the first match, stripping any comments or trailing content
            value = matches[0].split('//')[0].strip()
            return value
        return None

    def extract_editorgroups(self, content):
        """Extract EditorGroup or EditorGroups from the Part file content."""
        # Try to find EditorGroups array
        pattern_plural = r"EditorGroups\s*=\s*\[([^\]]+)\]"
        match_plural = re.search(pattern_plural, content, re.IGNORECASE)
        if match_plural:
            groups = match_plural.group(1).split(',')
            groups = [grp.strip().strip('"').split('//')[0].strip() for grp in groups]
            return groups

        # Try to find single EditorGroup
        pattern_singular = r"EditorGroup\s*=\s*\"?([^\n\"]+)\"?"
        match_singular = re.search(pattern_singular, content, re.IGNORECASE)
        if match_singular:
            group = match_singular.group(1).split('//')[0].strip()
            return [group]

        return []

    def setup_fields(self, unlock_type):
        self.clear_dynamic_fields()

        if unlock_type == 'Part':
            self.setup_part_fields()
        elif unlock_type == 'ToggleChoice':
            self.setup_togglechoice_fields()

    def setup_part_fields(self):
        # Prerequisite IDs
        self.dynamic_fields['prerequisites_label'] = tk.Label(self, text="Prerequisite IDs (comma-separated):")
        self.dynamic_fields['prerequisites_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['prerequisites_label'].grid(row=17, column=0, sticky='e', padx=10, pady=(20, 0))
        self.dynamic_fields['prerequisites_entry'].grid(row=17, column=1, columnspan=2, padx=10, pady=(20, 0))

        # Cost
        self.dynamic_fields['cost_label'] = tk.Label(self, text="Cost:")
        self.dynamic_fields['cost_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['cost_label'].grid(row=18, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['cost_entry'].grid(row=18, column=1, columnspan=2, padx=10, pady=(10, 0))

        # Generate Button
        self.dynamic_fields['generate_button'] = tk.Button(self, text="Generate Part Code", command=self.generate_part_code)
        self.dynamic_fields['generate_button'].grid(row=19, column=0, columnspan=3, pady=20)

    def setup_togglechoice_fields(self):
        # NameKey
        self.dynamic_fields['namekey_label'] = tk.Label(self, text="NameKey:")
        self.dynamic_fields['namekey_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['namekey_label'].grid(row=17, column=0, sticky='e', padx=10, pady=(20, 0))
        self.dynamic_fields['namekey_entry'].grid(row=17, column=1, columnspan=2, padx=10, pady=(20, 0))

        # DescriptionKey
        self.dynamic_fields['descriptionkey_label'] = tk.Label(self, text="DescriptionKey:")
        self.dynamic_fields['descriptionkey_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['descriptionkey_label'].grid(row=18, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['descriptionkey_entry'].grid(row=18, column=1, columnspan=2, padx=10, pady=(10, 0))

        # Icon Path
        self.dynamic_fields['icon_label'] = tk.Label(self, text="Icon Path:")
        self.dynamic_fields['icon_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['icon_label'].grid(row=19, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['icon_entry'].grid(row=19, column=1, columnspan=2, padx=10, pady=(10, 0))

        # EditorGroups Path
        self.dynamic_fields['editorgroups_label'] = tk.Label(self, text="EditorGroups Path:")
        self.dynamic_fields['editorgroups_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['editorgroups_label'].grid(row=20, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['editorgroups_entry'].grid(row=20, column=1, columnspan=2, padx=10, pady=(10, 0))

        # Parts Unlocked
        self.dynamic_fields['partsunlocked_label'] = tk.Label(self, text="Parts Unlocked (comma-separated):")
        self.dynamic_fields['partsunlocked_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['partsunlocked_label'].grid(row=21, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['partsunlocked_entry'].grid(row=21, column=1, columnspan=2, padx=10, pady=(10, 0))

        # ToggleChoicesUnlocked
        self.dynamic_fields['togglechoicesunlocked_label'] = tk.Label(self, text="ToggleChoicesUnlocked (format: [[choice, value]]):")
        self.dynamic_fields['togglechoicesunlocked_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['togglechoicesunlocked_label'].grid(row=22, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['togglechoicesunlocked_entry'].grid(row=22, column=1, columnspan=2, padx=10, pady=(10, 0))

        # Cost
        self.dynamic_fields['cost_label'] = tk.Label(self, text="Cost:")
        self.dynamic_fields['cost_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['cost_label'].grid(row=23, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['cost_entry'].grid(row=23, column=1, columnspan=2, padx=10, pady=(10, 0))

        # UpgradedFrom
        self.dynamic_fields['upgradedfrom_label'] = tk.Label(self, text="Upgraded From (comma-separated):")
        self.dynamic_fields['upgradedfrom_entry'] = tk.Entry(self, width=80)
        self.dynamic_fields['upgradedfrom_label'].grid(row=24, column=0, sticky='e', padx=10, pady=(10, 0))
        self.dynamic_fields['upgradedfrom_entry'].grid(row=24, column=1, columnspan=2, padx=10, pady=(10, 0))

        # Generate Button
        self.dynamic_fields['generate_button'] = tk.Button(self, text="Generate ToggleChoice Code", command=self.generate_togglechoice_code)
        self.dynamic_fields['generate_button'].grid(row=25, column=0, columnspan=3, pady=20)

    def generate_part_code(self):
        techrules_path = self.techrules_entry.get()
        part_path = self.part_entry.get()
        part_id = self.part_id_entry.get()

        prerequisites = self.dynamic_fields['prerequisites_entry'].get().strip()
        cost = self.dynamic_fields['cost_entry'].get().strip()

        if not all([techrules_path, part_path, part_id, cost]):
            messagebox.showerror("Error", "Please ensure all required fields are filled.")
            return

        # Compute relative path from TechRules directory to Part file
        techrules_dir = os.path.dirname(techrules_path)
        try:
            relative_path = os.path.relpath(part_path, techrules_dir).replace("\\", "/")
        except Exception as e:
            messagebox.showerror("Error", f"Error computing relative path: {e}")
            return

        # Handle EditorGroups
        selected_indices = self.editorgroups_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one Editor Group.")
            return

        if len(selected_indices) == 1:
            # Single Editor Group selected
            index = selected_indices[0]
            editorgroup_field = f"EditorGroup = &<{relative_path}>/Part/EditorGroups/{index}"
        else:
            # Multiple Editor Groups selected
            editorgroup_field = f"EditorGroups = &<{relative_path}>/Part/EditorGroups"

        # Format PartsUnlocked
        parts_unlocked = [part_id]
        parts_unlocked_formatted = f"[{', '.join(parts_unlocked)}]"

        # Format Prerequisites
        prerequisites_formatted = ""
        if prerequisites:
            prerequisites_list = [prereq.strip() for prereq in prerequisites.split(',') if prereq.strip()]
            prerequisites_formatted = f"    Prerequisites = [{', '.join(prerequisites_list)}]\n"

        # Final Output
        formatted_output = f"""
{{
    ID = {part_id}
    NameKey = &<{relative_path}>/Part/NameKey
    DescriptionKey = &<{relative_path}>/Part/DescriptionKey
    Icon = &<{relative_path}>/Part/EditorIcon
    {editorgroup_field}
    PartsUnlocked = {parts_unlocked_formatted}
{prerequisites_formatted}    Cost = {cost}
}}
"""
        self.display_output(formatted_output.strip())

    def generate_togglechoice_code(self):
        techrules_path = self.techrules_entry.get()
        part_path = self.part_entry.get()
        part_id = self.part_id_entry.get()

        namekey = self.dynamic_fields['namekey_entry'].get().strip()
        descriptionkey = self.dynamic_fields['descriptionkey_entry'].get().strip()
        icon = self.dynamic_fields['icon_entry'].get().strip()
        editorgroups = self.dynamic_fields['editorgroups_entry'].get().strip()
        parts_unlocked = self.dynamic_fields['partsunlocked_entry'].get().strip()
        togglechoices_unlocked = self.dynamic_fields['togglechoicesunlocked_entry'].get().strip()
        cost = self.dynamic_fields['cost_entry'].get().strip()
        upgradedfrom = self.dynamic_fields['upgradedfrom_entry'].get().strip()

        if not all([techrules_path, part_path, part_id, namekey, descriptionkey, icon, editorgroups, parts_unlocked, togglechoices_unlocked, cost]):
            messagebox.showerror("Error", "Please ensure all required fields are filled.")
            return

        # Compute relative path from TechRules directory to Part file
        techrules_dir = os.path.dirname(techrules_path)
        try:
            relative_path = os.path.relpath(part_path, techrules_dir).replace("\\", "/")
        except Exception as e:
            messagebox.showerror("Error", f"Error computing relative path: {e}")
            return

        # Handle EditorGroups (assumed to be plural and already handled)
        editorgroup_field = f"EditorGroups = {editorgroups}"

        # Format PartsUnlocked
        parts_unlocked_list = [part.strip() for part in parts_unlocked.split(',') if part.strip()]
        parts_unlocked_formatted = f"[{', '.join(parts_unlocked_list)}]"

        # Format UpgradedFrom
        upgradedfrom_formatted = ""
        if upgradedfrom:
            upgradedfrom_list = [upg.strip() for upg in upgradedfrom.split(',') if upg.strip()]
            upgradedfrom_formatted = f"    UpgradedFrom = [{', '.join(upgradedfrom_list)}]\n"

        # Final Output
        formatted_output = f"""
{{
    ID = {part_id}
    NameKey = {namekey}
    DescriptionKey = {descriptionkey}
    Icon = {icon}
    {editorgroup_field}
    PartsUnlocked = {parts_unlocked_formatted}
    ToggleChoicesUnlocked = {togglechoices_unlocked}
{upgradedfrom_formatted}    Cost = {cost}
}}
"""
        self.display_output(formatted_output.strip())

    def wrap_rules_path(self, path):
        """Wrap only the part of the path that ends with .rules in < >."""
        if ".rules" in path:
            base_path, sub_path = path.split(".rules", 1)
            return f"<{base_path}.rules>{sub_path}"
        return path

    def display_output(self, formatted_output):
        # Create or clear the output text box
        if 'output_text' not in self.dynamic_fields:
            self.dynamic_fields['output_text'] = tk.Text(self, height=25, width=120)
            self.dynamic_fields['output_text'].grid(row=26, column=0, columnspan=3, padx=10, pady=10)
        else:
            self.dynamic_fields['output_text'].delete(1.0, tk.END)

        # Insert the formatted output
        self.dynamic_fields['output_text'].insert(tk.END, formatted_output)

        # Create or enable Copy and Save buttons
        if 'copy_button' not in self.dynamic_fields:
            self.dynamic_fields['copy_button'] = tk.Button(self, text="Copy to Clipboard", command=lambda: self.copy_to_clipboard(formatted_output))
            self.dynamic_fields['copy_button'].grid(row=27, column=0, pady=10)

        if 'save_button' not in self.dynamic_fields:
            self.dynamic_fields['save_button'] = tk.Button(self, text="Save as File", command=lambda: self.save_to_file(formatted_output))
            self.dynamic_fields['save_button'].grid(row=27, column=1, pady=10)

    def reset_fields(self):
        # Clear all entries
        self.mod_root_entry.delete(0, tk.END)
        self.techrules_entry.delete(0, tk.END)
        self.part_entry.delete(0, tk.END)
        self.part_id_entry.config(state='normal')
        self.part_id_entry.delete(0, tk.END)
        self.part_id_entry.config(state='readonly')
        self.editorgroups_listbox.delete(0, tk.END)
        self.clear_dynamic_fields()

        # Clear configuration
        if self.config.has_section('Paths'):
            self.config.remove_section('Paths')
            self.save_config()

        # Disable dependent buttons
        self.generate_techrules_button.config(state='disabled')
        self.techrules_browse_button.config(state='disabled')
        self.part_browse_button.config(state='disabled')
        self.part_button.config(state='disabled')
        self.togglechoice_button.config(state='disabled')
        self.show_techrules_button.config(state='disabled')
        self.advanced_prereq_button.config(state='disabled')

        # Remove output fields if they exist
        if 'output_text' in self.dynamic_fields:
            self.dynamic_fields['output_text'].grid_forget()
            del self.dynamic_fields['output_text']
        if 'copy_button' in self.dynamic_fields:
            self.dynamic_fields['copy_button'].grid_forget()
            del self.dynamic_fields['copy_button']
        if 'save_button' in self.dynamic_fields:
            self.dynamic_fields['save_button'].grid_forget()
            del self.dynamic_fields['save_button']

    def clear_dynamic_fields(self):
        for widget in self.dynamic_fields.values():
            widget.grid_forget()
        self.dynamic_fields.clear()

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Text copied to clipboard!")

    def save_to_file(self, text):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(text)
                messagebox.showinfo("Saved", f"File saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def show_techrules(self):
        techrules_path = self.techrules_entry.get()

        if not techrules_path:
            messagebox.showerror("Error", "Please select the TechRules file first.")
            return

        # Compute absolute path of TechRules file
        techrules_abs = os.path.abspath(techrules_path)
        if not os.path.exists(techrules_abs):
            messagebox.showerror("Error", f"TechRules file does not exist at: {techrules_abs}")
            return

        # Read TechRules file
        try:
            with open(techrules_abs, 'r') as file:
                content = file.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read TechRules file: {e}")
            return

        # Display the content in a new window
        popup = tk.Toplevel(self)
        popup.title("Current TechRules Readout")
        popup.geometry("1000x800")

        text_box = tk.Text(popup, wrap='word')
        text_box.pack(expand=True, fill='both', padx=10, pady=10)

        text_box.insert(tk.END, content)

    def open_prerequisite_dialog(self):
        """Open a dialog that allows users to select prerequisite IDs from a list."""
        # Ensure mod root is determined
        mod_root = self.config.get('Paths', 'mod_root', fallback=None)
        if not mod_root:
            messagebox.showerror("Error", "Mod root could not be determined. Please select the mod.rules file first.")
            return

        # Check if prerequisite IDs are already loaded
        if not self.prerequisite_ids:
            self.load_prerequisite_ids(mod_root)

        if not self.prerequisite_ids:
            messagebox.showerror("Error", "No Part IDs found in the mod.")
            return

        # Create a new pop-up window
        popup = tk.Toplevel(self)
        popup.title("Select Prerequisite IDs")
        popup.geometry("400x500")

        # Instructions
        instructions = tk.Label(popup, text="Select Prerequisite IDs from your mod:")
        instructions.pack(pady=10)

        # Listbox with multiple selection
        self.prereq_listbox = tk.Listbox(popup, selectmode=tk.MULTIPLE, width=50, height=20)
        self.prereq_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Populate the listbox
        for idx, prereq in enumerate(self.prerequisite_ids):
            self.prereq_listbox.insert(tk.END, prereq)

        # Pre-select already selected prerequisites
        current_prereq = self.dynamic_fields.get('prerequisites_entry', tk.Entry(self)).get().strip()
        if current_prereq:
            selected = [pr.strip() for pr in current_prereq.split(',') if pr.strip()]
            for i, prereq in enumerate(self.prerequisite_ids):
                if prereq in selected:
                    self.prereq_listbox.select_set(i)

        # Buttons
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        select_button = tk.Button(button_frame, text="Select", command=lambda: self.set_prerequisites(popup))
        select_button.pack(side=tk.LEFT, padx=5)

        refresh_button = tk.Button(button_frame, text="Refresh", command=lambda: self.refresh_prerequisite_ids(popup))
        refresh_button.pack(side=tk.LEFT, padx=5)

    def load_prerequisite_ids(self, mod_root):
        """Scan all .rules files in the mod root to collect Part IDs."""
        part_ids = []
        for root, dirs, files in os.walk(mod_root):
            for file in files:
                if file.endswith(".rules"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                    except:
                        continue

                    # Check if file defines a Part
                    if re.search(r'^\s*Part\s*:', content, re.MULTILINE):
                        # Extract Part IDs
                        ids = re.findall(r'^\s*ID\s*=\s*\"?([^\n\"]+)\"?', content, re.MULTILINE)
                        for id_value in ids:
                            id_value = id_value.split('//')[0].strip()
                            part_ids.append(id_value)

        self.prerequisite_ids = sorted(set(part_ids))
        # Save to config
        self.config['Prerequisites']['part_ids'] = ','.join(self.prerequisite_ids)
        self.save_config()

    def refresh_prerequisite_ids(self, popup):
        """Refresh the list of prerequisite IDs."""
        mod_root = self.config.get('Paths', 'mod_root', fallback=None)
        if not mod_root:
            messagebox.showerror("Error", "Mod root could not be determined.")
            return

        self.load_prerequisite_ids(mod_root)

        # Update the listbox
        self.prereq_listbox.delete(0, tk.END)
        for prereq in self.prerequisite_ids:
            self.prereq_listbox.insert(tk.END, prereq)

    def set_prerequisites(self, popup):
        """Set the selected prerequisites in the prerequisites entry."""
        selected_indices = self.prereq_listbox.curselection()
        selected_ids = [self.prerequisite_ids[i] for i in selected_indices]
        prerequisites_str = ', '.join(selected_ids)

        # Set the prerequisites in the entry field
        self.dynamic_fields['prerequisites_entry'].delete(0, tk.END)
        self.dynamic_fields['prerequisites_entry'].insert(0, prerequisites_str)

        # Close the pop-up
        popup.destroy()

    def generate_techs_rules(self):
        mod_root = self.config.get('Paths', 'mod_root', fallback=None)
        if not mod_root:
            messagebox.showerror("Error", "Mod root is not set. Please select your mod.rules file first.")
            return

        # Define the path for techs.rules
        techs_rules_dir = os.path.join(mod_root, 'modes', 'career')
        techs_rules_path = os.path.join(techs_rules_dir, 'techs.rules')

        # Check if techs.rules already exists
        if os.path.exists(techs_rules_path):
            messagebox.showwarning("Warning", f"techs.rules already exists at: {techs_rules_path}. It will not be overwritten.")
            return

        # Create modes/career/ directory if it doesn't exist
        os.makedirs(techs_rules_dir, exist_ok=True)

        # Define the scaffolding content
        scaffolding = """//AutoGenerated by TechRulesGenerator

//Instructions: Uncomment and add the following snippet to your mod.rules file to activate this file:
// Adding Tech to Career Mode
/*{
    Action = AddMany
    AddTo = "<./Data/modes/career/techs.rules>/Techs"
    ManyToAdd = &<modes/career/techs.rules>/Techs
}*/

Techs
[


    /*
//Example Category

    {
        ID = author.part2
        NameKey = &<../../example/examplepart/part.rules>/Part/NameKey
        DescriptionKey = &<../../example/examplepart/part.rules>/Part/DescriptionKey
        Icon = &<../../example/examplepart/part.rules>/Part/EditorIcon
        EditorGroup = &<../../example/examplepart/part.rules>/Part/EditorGroups/0
        PartsUnlocked = [author.part2]
        //Prerequisites = [author.part1]
        Cost = 500
    }
    */
//Energy Weapons Category

//Projectile Weapons Category

//Defenses Category

//Flight Category

//Crew Category

//Power Category

//Production Category

//Storage Category

//Utilities Category

//Structure Category
]
"""

        # Write the scaffolding to techs.rules
        try:
            with open(techs_rules_path, 'w') as file:
                file.write(scaffolding)
            messagebox.showinfo("Success", f"techs.rules has been created at: {techs_rules_path}")
            # Automatically populate the techrules_entry field
            self.techrules_entry.delete(0, tk.END)
            self.techrules_entry.insert(0, techs_rules_path)
            self.config['Paths']['techrules_path'] = techs_rules_path
            self.save_config()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create techs.rules file: {e}")

if __name__ == "__main__":
    app = TechRulesGenerator()
    app.mainloop()
