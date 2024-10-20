---

### **Summary**

These two mods—**Huge Crews** and **Huge Ships**—demonstrate how you can modify the existing vanilla game structure in Cosmoteer. By using the `mod.rules` file, you can override default game settings to introduce significant changes, such as increasing the maximum crew size or expanding the maximum ship size. Both mods follow the basic structure of modding as explained in the initial mod.rules example, using `Overrides` actions to alter specific game attributes.

---

### **Mod 1: Huge Crews**

#### **1.1 Basic Mod Information**
```plaintext
ID = cosmoteer.huge_crews
Name = "Huge Crews"
Version = 1.0.0
CompatibleGameVersions = ["0.27.2"]
ModifiesGameplay = true
Author = "Walternate Realities"
Description = "Increases the maximum crew in Career mode to 100000 regardless of fame.\n\n"\
              "<red>WARNING: Your computer probably can't handle crews this large! Use with caution!</red>"
```

- **ID and Name**: As with all mods, the **ID** must be unique, using the format `author_name.mod_name`. Here, the mod’s ID is `cosmoteer.huge_crews`, and the **Name** is "Huge Crews."
- **Version** and **CompatibleGameVersions**: This mod is versioned `1.0.0` and is compatible with Cosmoteer version `0.27.2`.
- **ModifiesGameplay**: Since this mod directly affects gameplay by changing crew limits, it is set to `true`.
- **Description**: The description gives an important warning to users that increasing crew sizes could cause performance issues, adding a red text warning using `<red></red>` tags.

#### **1.2 MAX_CREW Definition**
```plaintext
MAX_CREW = 100000
```

- **MAX_CREW**: A custom variable `MAX_CREW` is defined here to store the value `100,000`, representing the maximum crew size that the mod will use. This is a convenient way to reference the same value multiple times in the mod, as seen in the subsequent actions.

#### **1.3 Actions: Overriding Crew Limits**
The core functionality of this mod is to override the default crew scarcity levels to set the maximum crew to 100,000.

```plaintext
Actions
[
    {
        Action = Overrides
        OverrideIn = "<modes/career/career.rules>/CrewScarcityLevels/0"
        Overrides
        {
            CrewFamePrereqCountRange = [&~/MAX_CREW, &~/MAX_CREW]
        }
    }
    // Repeated for levels 1-3...
]
```

- **Action = Overrides**: This mod uses the **Overrides** action to modify specific data fields within the vanilla game’s `.rules` files.
- **OverrideIn**: The mod targets `CrewScarcityLevels` for each career mode level (0–3). These levels correspond to different levels of crew availability based on player fame.
- **CrewFamePrereqCountRange**: This is the key field that controls the range of fame needed to unlock additional crew. By setting it to `&~/MAX_CREW`, the mod ensures that all levels allow up to **100,000 crew members**, regardless of fame.

#### **Key Observations**
1. **Structure**: The mod’s structure is simple and consistent. It repeats the same override for four levels of crew scarcity, ensuring that the `MAX_CREW` variable is applied to all levels.
2. **Use of Variables**: The mod efficiently uses a custom-defined variable (`MAX_CREW`) to avoid repeating the same value multiple times, making it easier to update if needed.
3. **Mod.rules Reference**: This mod is a clear application of the `Overrides` action from the mod.rules example, which allows multiple named data fields to be updated. Here, we are overriding specific crew limits in a list structure.

---

### **Mod 2: Huge Ships**

#### **2.1 Basic Mod Information**
```plaintext
ID = cosmoteer.huge_ships
Name = "Huge Ships"
Version = 1.0.0
CompatibleGameVersions = ["0.27.2"]
ModifiesGameplay = true
Author = "Walternate Realities"
Description = "Increases the maximum ship size from 120x120 to 1000x1000\n\n"\
              "<red>WARNING: Your computer probably can't handle ships this large! Use with caution!</red>"
```

- **ID and Name**: The mod **ID** is `cosmoteer.huge_ships`, and the **Name** is "Huge Ships."
- **Description**: Similar to the previous mod, a warning is included in red text to notify users of potential performance issues when using such large ships.

#### **2.2 Actions: Overriding Ship Size Limits**
This mod increases the maximum ship size from 120x120 to 1000x1000.

```plaintext
Actions
[
    {
        Action = Overrides
        OverrideIn = "<ships/base_ship.rules>"
        Overrides
        {
            MaxBorders
            {
                Left = -500
                Right = 500
                Top = -500
                Bottom = 500
            }
        }
    }
]
```

- **Action = Overrides**: Like the Huge Crews mod, this mod uses the **Overrides** action to modify game data. However, here it is targeting a ship-related file rather than career mode settings.
- **OverrideIn**: The file being modified is `<ships/base_ship.rules>`, which contains the core settings for ship structures in the game.
- **MaxBorders**: This is the key field that controls the boundaries of ship size. The default size in the game is 120x120 (or a range of -60 to 60 for both axes). In this mod, the range is significantly increased to **1000x1000**, or -500 to 500 on both axes.

#### **Key Observations**
1. **Single Modification**: Unlike the Huge Crews mod, which overrides multiple values, this mod changes only one key setting, the `MaxBorders` for ships. This simplicity makes it a good example for modders looking to understand how to modify a single aspect of the game.
2. **Impact on Gameplay**: Increasing ship sizes dramatically changes the gameplay experience, as ships can be much larger than intended by default. This mirrors the significant change in crew size in the previous mod.
3. **Performance Considerations**: Both mods include a warning in the description about the potential performance impact of such large changes, which is a good practice for modders making similarly dramatic alterations.

---

### **General Tips for Modders**

1. **Use of `Overrides`**: Both mods rely heavily on the `Overrides` action, which is one of the core tools for modding in Cosmoteer. This allows you to modify specific named fields in the game’s data files without permanently altering the base game.
2. **Define Variables for Repeated Values**: In the Huge Crews mod, the use of `MAX_CREW` as a variable simplifies the process of modifying multiple values and makes future changes easier. This is a useful technique whenever the same value is used repeatedly in a mod.
3. **Warnings and Performance**: Including warnings in your mod’s description when making large-scale changes (like ship size or crew limits) is important, as these modifications can significantly impact game performance, especially on lower-end systems.

