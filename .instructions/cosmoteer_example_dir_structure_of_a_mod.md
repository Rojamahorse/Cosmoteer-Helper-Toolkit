Below is the directory structure summary for the **SuperArmor** mod. This layout follows the standard modding conventions for Cosmoteer and includes useful explanations for modders.

---

### **Basic Directory Structure for the SuperArmor Mod**

```plaintext
SuperArmorMod/                  # Root folder of the mod
│
├── mod.rules                   # Main mod configuration file
├── control_room_small_components.rules  # Custom component rule file
├── logo.png                    # Logo for the mod (optional)
│
├── strings/                    # Folder for localization strings
│   └── en.rules                # English localization strings
│
├── roof_decals/                # Folder for custom roof decals
│   └── squiggle.png            # Example custom roof decal image
│
├── roof_textures/              # Folder for custom roof textures
│   └── flowers.png             # Example custom roof texture image
│
├── ships/                      # Folder for ships
│   └── Arclight.ship.png       # Example ship file (Arclight ship)
│
├── super_armor/                # Folder for the SuperArmor part
│   ├── armor.png               # Armor texture (undamaged)
│   ├── armor_33.png            # Armor texture (33% health)
│   ├── armor_66.png            # Armor texture (66% health)
│   ├── blueprints.png          # Blueprint image for the SuperArmor part
│   ├── icon.png                # Icon for the SuperArmor part in the UI
│   ├── roof.png                # Roof texture
│   ├── roof_33.png             # Damaged roof texture (33%)
│   ├── roof_66.png             # Damaged roof texture (66%)
│   ├── roof_normals.png        # Normals file for roof texture (undamaged)
│   ├── roof_normals_33.png     # Normals file for roof texture (33% health)
│   ├── roof_normals_66.png     # Normals file for roof texture (66% health)
│   └── super_armor.rules       # Rule file defining the SuperArmor part
│
├── super_armor_wedge/          # Folder for the SuperArmorWedge part
│   ├── armor.png               # Armor texture (undamaged)
│   ├── armor_33.png            # Armor texture (33% health)
│   ├── armor_66.png            # Armor texture (66% health)
│   ├── blueprints.png          # Blueprint image for the SuperArmorWedge part
│   ├── external_wall_normals.png    # Normals file for external wall (undamaged)
│   ├── external_wall_normals_33.png # Normals file for external wall (33% health)
│   ├── external_wall_normals_66.png # Normals file for external wall (66% health)
│   ├── floor.png               # Floor texture
│   ├── floor_33.png            # Floor texture (33%)
│   ├── floor_66.png            # Floor texture (66%)
│   ├── icon.png                # Icon for the SuperArmorWedge part in the UI
│   ├── roof.png                # Roof texture
│   ├── roof_33.png             # Roof texture (33%)
│   ├── roof_66.png             # Roof texture (66%)
│   ├── roof_normals.png        # Roof normals file (undamaged)
│   ├── roof_normals_33.png     # Roof normals file (33%)
│   ├── roof_normals_66.png     # Roof normals file (66%)
│   └── super_armor_wedge.rules # Rule file defining the SuperArmorWedge part
```

---

### **Explanation of Key Directories and Files**

1. **SuperArmorMod (Root Directory)**
   - This is the top-level directory where all mod files are organized. The name should reflect the mod (e.g., **SuperArmorMod**).

2. **mod.rules (Main Mod Configuration)**
   - This file contains the core mod settings, including the mod's ID, name, version, and actions that define how the mod interacts with the game. It points to the other files in the structure and applies changes to the game.
   - It also includes references to other assets such as icons, strings, and part definitions.

3. **strings/ (Localization)**
   - The **strings** folder is where localized text is stored. Each language (e.g., **en.rules** for English) has its own file that defines strings such as the name, description, and other text related to the mod.
   - For the **SuperArmor** mod, the **en.rules** file would contain descriptions and names for the SuperArmor part in English.

4. **ships/ (Part Data and Assets)**
   - The **ships** folder contains data related to the modded ship parts. The **super_armor/** folder specifically stores the rules and assets for the SuperArmor part.
   - **super_armor.rules** defines the part’s attributes, while textures like **armor.png** and **armor_33.png** handle the visual states of the armor depending on damage levels.
   - **blueprints.png** is the image used for the part's blueprint when constructing ships.

5. **icons/ (Editor and UI Icons)**
   - This folder stores icons used in the in-game editor and UI.
   - The **Parts/** subfolder contains the specific icon for the **SuperArmor** part, displayed in the editor when adding or selecting the part.
   - The **Misc/** folder could contain additional icons for other UI purposes, although it is optional.

---

### **Example: mod.rules File**

```plaintext
ID = cosmoteer.super_armor_mod
Name = "Super Armor Mod"
Version = 1.0.0
CompatibleGameVersions = ["0.27.2"]
ModifiesGameplay = true
Author = "Walternate Realities"
Description = "Adds a Super Armor part with enhanced durability for your ships."

Actions
[
    {
        Action = Add
        AddTo = "<ships/terran/terran.rules>/Terran/Parts"
        ManyToAdd
        [
            &<ships/super_armor/super_armor.rules>/Part
        ]
    }
]

StringsFolder = "strings"
```

### **Example: en.rules File**

```plaintext
__Name = "English"
__DebugOnly = false

Parts/SuperArmor = "Super Armor"
Parts/SuperArmorDesc = "A highly durable armor part with double the strength of standard armor."
Parts/SuperArmorIcon = "Super Armor Icon"
```

---

### **Key Points for Modders**
- **File Organization**: Each type of asset (rules, textures, icons, etc.) should be organized into appropriate subdirectories to keep the mod clean and easy to maintain.
- **Localization Support**: Including a **strings** folder with language files ensures that your mod is readable in different languages, making it more accessible.
- **Asset Referencing**: The paths in your **mod.rules** file should correctly point to the assets in the **ships/** and **icons/** directories (e.g., `&<ships/super_armor/super_armor.rules>/Part`).
- **Textures and Damage Levels**: Make sure to include textures for different damage levels (e.g., 33%, 66%) to give the armor a more dynamic appearance as it takes damage.

---
