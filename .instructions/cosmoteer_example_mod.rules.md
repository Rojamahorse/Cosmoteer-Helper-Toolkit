---

### **Summary**

This guide explains how to create a basic `mod.rules` file for Cosmoteer. It introduces key concepts like setting up mod identifiers, creating actions to modify the game, and referencing game data. Each section includes examples to help you understand how to apply these elements in your mod. The `mod.rules` file acts as the starting point for your modding journey.

---

### **1. Basic Mod Information**

Every mod must include basic information to identify itself and ensure compatibility with the game.

#### **1.1 Mod ID and Name**
- **ID**: Each mod requires a unique ID in the format `author_name.mod_name`. This avoids conflicts with other mods.
  - Example: `ID = cosmoteer.example_mod`
- **Name**: This is the human-readable name that appears in the UI.
  - Example: `Name = "Example Mod"`

#### **1.2 Version and Compatibility**
- **Version**: Specify the mod version for display purposes (optional).
  - Example: `Version = 1.0.0`
- **CompatibleGameVersions**: List compatible Cosmoteer versions to warn players if the mod might not work with their game version.
  - Example: `CompatibleGameVersions = ["0.27.2"]`

#### **1.3 Mod Author and Description**
- **Author**: Specify the mod creator’s name (optional).
  - Example: `Author = "Walternate Realities"`
- **Description**: Provide a detailed description of your mod’s features (optional).
  - Example:
    ```plaintext
    Description = "This mod increases starting money and rewards on Builder difficulty."
    ```

#### **1.4 Additional Settings**
- **ModifiesGameplay**: Set to `true` if the mod changes gameplay.
  - Example: `ModifiesGameplay = true`
- **Logo**: Display a logo for the mod in the UI (optional).
  - Example: `Logo = "logo.png"`

---

### **2. Language Strings**

Mods can define their own localized text by creating string files for different languages.

- **StringsFolder**: Set the folder containing per-language string files, like `en.rules` for English. Each language must have its own file using the two-letter language code.
  - Example: `StringsFolder = "strings"`

---

### **3. Modifying Game Data with Actions**

Actions allow mods to modify game data without permanently altering the game’s core files. Here are the basic actions you can use:

#### **3.1 Replace Action**
- **Purpose**: Replace a value in the game’s data.
- **Example**: Increase starting funds on Builder difficulty to 200,000.
  ```plaintext
  Action = Replace
  Replace = "<modes/career/career.rules>/EconDifficultyLevels/1/StartingMoney"
  With = 200000
  ```

#### **3.2 Overrides Action**
- **Purpose**: Modify or add multiple named data fields.
- **Example**: Increase money and fame rewards on Builder difficulty to 300%.
  ```plaintext
  Action = Overrides
  OverrideIn = "<modes/career/career.rules>/EconDifficultyLevels/1"
  Overrides
  {
      MoneyRewardFactor = 300%
      FameRewardFactor = 300%
  }
  ```

#### **3.3 Remove Action**
- **Purpose**: Remove a data field from the game.
- **Example**: Remove the collateral damage effect from small reactors.
  ```plaintext
  Action = Remove
  Remove = "<ships/terran/reactor_small/reactor_small.rules>/Part/Components/DestroyedEffects/HitEffects"
  ```

#### **3.4 RemoveMany Action**
- **Purpose**: Remove multiple data fields.
- **Example**: Remove command points from cannons and railguns.
  ```plaintext
  Action = RemoveMany
  RemoveMany
  [
      "<ships/terran/cannon_med/cannon_med.rules>/Part/Components/CommandConsumer"
      "<ships/terran/railgun_loader/railgun_loader.rules>/Part/Components/CommandConsumer"
  ]
  ```

#### **3.5 Add Action**
- **Purpose**: Add a new data field to an existing list or group.
- **Example**: Add the "Arclight" ship to spawn in Career mode.
  ```plaintext
  Action = Add
  AddTo = "<builtin_ships/builtins.rules>/Ships"
  ToAdd
  {
      File = "ships/Arclight.ship.png"
      Faction = cabal
      Tags = [combat]
      Tier = 3
      Difficulty = 2
  }
  ```

---

### **4. Advanced Actions**

#### **4.1 AddMany Action**
- **Purpose**: Add multiple data fields at once.
- **Example**: Add "super armor" parts to the list.
  ```plaintext
  Action = AddMany
  AddTo = "<ships/terran/terran.rules>/Terran/Parts"
  ManyToAdd
  [
      &<super_armor/super_armor.rules>/Part
      &<super_armor_wedge/super_armor_wedge.rules>/Part
  ]
  ```

#### **4.2 AddBase Action**
- **Purpose**: Add a reference to the inheritance list of an existing group.
- **Example**: Add thrusters to control rooms by inheriting components.
  ```plaintext
  Action = AddBase
  AddBaseTo = "<ships/terran/control_room_small/control_room_small.rules>/Part/Components"
  BaseToAdd = &<control_room_small_components.rules>
  ```

---

### **5. Adding Custom Assets**

You can also add new decals, textures, and ship libraries to the game.

#### **5.1 Custom Roof Decals**
- **Example**: Add a custom roof decal.
  ```plaintext
  Action = Add
  AddTo = "<roof_decals/roof_decals.rules>/Groups/1/Folders"
  ToAdd = "roof_decals"
  ```

#### **5.2 Custom Ship Textures**
- **Example**: Add custom ship textures.
  ```plaintext
  Action = Add
  AddTo = "<ships/terran/terran.rules>/Terran/Roofs/RoofTexturesFolders"
  ToAdd = "roof_textures"
  ```

#### **5.3 Ship Libraries**
- **Example**: Add a new root folder to the Ship Library.
  ```plaintext
  ShipLibraries
  [
      {
          Folder = "ships"
          NameKey = "ExampleModShips"
          TooltipKey = "ExampleModShipsTip" // Optional
      }
  ]
  ```

---

### **6. General Tips**
- **Avoiding Errors**: Check the `.txt` log if the game crashes due to a mod.
- **Combining Actions**: You can often combine actions like `Replace` and `Overrides` for simpler code.
- **Named vs. Unnamed Fields**: Use `Overrides` for named fields and `Replace` for unnamed fields (like lists).

---