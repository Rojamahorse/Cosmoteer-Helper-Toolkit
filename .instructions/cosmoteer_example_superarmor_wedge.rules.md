---

### **Summary**

This file defines a new armor part for the Cosmoteer game, the "SuperArmorWedge." The structure of the file uses a combination of references, data fields, and components to define the part’s behavior, appearance, and interactions within the game. This instructional guide explains the purpose of each section and how it works, helping modders understand how to structure and modify parts in their mods.

---

### **1. Part Header Information**

The part starts by referencing a base part and providing key identifiers and metadata.

```plaintext
Part : <./Data/ships/terran/base_part_terran.rules>/Part
{
    NameKey = "Parts/SuperArmorWedge"
    IconNameKey = "Parts/SuperArmorWedgeIcon"
    ID = cosmoteer.super_armor_wedge
```

- **Part Inheritance**: `Part : <...>` means this part is inheriting properties from the base part located at the given path. It is a common practice to inherit from existing parts to reuse core attributes.
- **NameKey** and **IconNameKey**: Define the name and icon that will be displayed in the user interface for this part.
- **ID**: Each part must have a unique ID in the format `author_name.part_name`. This ensures the mod part doesn’t conflict with other mods or the base game.

---

### **2. General Attributes**

This section contains general attributes for the part, such as grouping, resources, health, and resistance.

```plaintext
    EditorGroup = "Defenses"
    DescriptionKey = "Parts/SuperArmorWedgeDesc"
    Resources = [ [steel, 12] ]
    AIValueFactor = 0
    Size = [1, 1]
    MaxHealth = 4000
    ExplosiveDamageAbsorption = 100%
    ExplosiveDamageResistance = 50%
```

- **EditorGroup**: The category under which the part will appear in the editor (e.g., defenses, weapons).
- **DescriptionKey**: Refers to the part’s description string in the language files.
- **Resources**: The cost of building this part, here it's defined as 12 units of steel.
- **AIValueFactor**: Defines how the AI values this part. Setting it to `0` makes the AI ignore it.
- **Size**: Specifies the part’s size in the game grid, here it is a 1x1 tile part.
- **MaxHealth**: Defines the part's total health.
- **ExplosiveDamageAbsorption**: Percentage of explosive damage absorbed.
- **ExplosiveDamageResistance**: Percentage of resistance against explosive damage.

---

### **3. Buffs and Penetration Resistance**

These attributes modify how the part behaves when interacting with buffs and incoming attacks.

```plaintext
    ReceivableBuffs : ^/0/ReceivableBuffs []
    InitialPenetrationResistance = 5
    ContinuingPenetrationResistance = &InitialPenetrationResistance
```

- **ReceivableBuffs**: Inherits buff information from the base part (indicated by the caret `^` symbol), allowing the part to receive buffs.
- **PenetrationResistance**: This defines how resistant the part is to penetration attacks. It uses the `InitialPenetrationResistance` as the base value, and then references that same value for `ContinuingPenetrationResistance` using the `&` symbol.

---

### **4. Wall and Door Properties**

These fields control the structural aspects of the part, such as wall positioning and door requirements.

```plaintext
    IsWalled = true
    ExternalWalls = [TopRight, Right, BottomRight, Bottom, BottomLeft]
    InternalWalls = [Left, TopLeft, Top]
    AllowedDoorLocations = []
    GeneratorRequiresDoor = false
```

- **IsWalled**: Indicates that the part has walls.
- **ExternalWalls/InternalWalls**: Specifies which sides of the part have walls, with external walls on the outer sides and internal walls on the inside.
- **AllowedDoorLocations**: No doors are allowed for this part.
- **GeneratorRequiresDoor**: Indicates whether a generator part requires a door (here it doesn’t).

---

### **5. Graphics and Colliders**

This section controls the visual appearance of the part and how it collides with other objects in the game.

```plaintext
    EditorIcon
    {
        Texture
        {
            File = "icon.png"
            SampleMode = Linear
        }
        Size = [32, 32]
    }
    Components : ^/0/Components
    {
        Collider
        {
            Type = PolygonCollider
            Vertices
            [
                [1, 0]
                [1, 1]
                [0, 1]
            ]
        }
    }
```

- **EditorIcon**: Defines the icon that appears in the editor for this part, using a `32x32` pixel texture.
- **Components**: This section inherits components from the base part. It includes the **Collider**, which defines the part's collision shape in the game. In this case, it uses a triangular polygon collider based on the listed vertices.

---

### **6. EMP and Graphics Components**

Additional components add specific behaviors like EMP absorption and define the graphical layers of the part.

```plaintext
        EmpAbsorber
        {
            Type = ExplosiveResourceDrainSink
            ResourceType = battery
            AbsorbsResourceDrain = 500
            RecoveryRate = (&AbsorbsResourceDrain) * 0.1
        }
```

- **EmpAbsorber**: Allows the part to absorb EMP (electromagnetic pulse) attacks by draining the `battery` resource, with a recovery rate based on `AbsorbsResourceDrain`.

```plaintext
        Graphics
        {
            Floor { ... }
            Walls { ... }
            Roof { ... }
        }
```

- **Graphics**: Controls how the part looks in the game. It includes layers for the floor, walls, and roof, each with different textures that change based on damage levels.

---

### **7. Destroyed Effects**

Defines what happens when the part is destroyed.

```plaintext
        DestroyedEffects
        {
            Type = DeathEffects
            MediaEffects = &/COMMON_EFFECTS/SmallPartDestroyedDry
            Location = [.5, .5]
        }
```

- **DestroyedEffects**: When the part is destroyed, it triggers effects from a common set of destruction effects, located at the specified coordinates.

---

### **8. Blueprints and Stats**

The **Blueprints** section defines how the part appears in blueprints, while **Stats** calculates dynamic values for specific attributes.

```plaintext
        Blueprints
        {
            Type = BlueprintSprite
            File = "blueprints.png"
            Size = [1, 1]
        }

        Stats
        {
            EMPResist = (&~/Part/Components/EmpAbsorber/AbsorbsResourceDrain) / 1000
        }
```

- **Blueprints**: Defines the blueprint sprite for the part.
- **Stats**: The part's EMP resistance is calculated based on the `AbsorbsResourceDrain` value, divided by 1000.

---

### **Observations on File Structure**

1. **Inheritance**: The part uses inheritance (`Part : <...>`) to reuse attributes from a base part and then extends or overrides certain properties.
2. **Reference Paths**: Paths like `&<path>` and `^/path` are used to reference or inherit values from other parts or components, making it easy to share values across parts.
3. **Components**: Each part can have multiple components, like colliders, graphics, and effects, which define its behavior and appearance in different contexts (e.g., visual layers, destruction effects).

---

### **General Tips for Modders**
- **Use Inheritance**: Inheriting from existing parts helps reduce redundancy and keeps your mod cleaner by reusing common attributes.
- **Reference Values**: When possible, use references (e.g., `&InitialPenetrationResistance`) to make your parts more modular and adaptable.
- **Graphics Layers**: Organize the graphical appearance of your parts by splitting the floor, wall, and roof into separate layers with damage textures for immersive visuals.
- **Debugging**: If the part doesn’t behave as expected, review the `log.txt` file to identify any issues with paths or inheritance.
