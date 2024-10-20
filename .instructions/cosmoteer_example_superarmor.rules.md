---

### **Summary**

This part configuration defines the "SuperArmor" piece in Cosmoteer. Like the "SuperArmorWedge," it inherits from a base armor part, but there are notable differences in attributes such as health, penetration resistance, and how the graphics layers are handled. This breakdown will highlight key components, provide observations on differences from the previous example, and offer instructional insights to guide modders.

---

### **1. Part Header Information**

The header provides basic identifiers and metadata for the part, following the same structure as the previous example.

```plaintext
Part : <./Data/ships/terran/base_part_terran.rules>/Part
{
    NameKey = "Parts/SuperArmor"
    IconNameKey = "Parts/SuperArmorIcon"
    ID = cosmoteer.super_armor
```

- **Part Inheritance**: Like the previous example, this part inherits from the same base part (`base_part_terran.rules`).
- **ID**: The ID is unique (`cosmoteer.super_armor`), and again, modders should avoid using "cosmoteer" to prevent conflicts with future official parts.

---

### **2. General Attributes**

Here we see similarities and some differences in attributes like health and size between the SuperArmor and SuperArmorWedge.

```plaintext
    EditorGroup = "Defenses"
    DescriptionKey = "Parts/SuperArmorDesc"
    Resources = [ [steel, 24] ]
    AIValueFactor = 0
    Size = [1, 1]
    MaxHealth = 8000
    ExplosiveDamageAbsorption = 100%
    ExplosiveDamageResistance = 50%
```

- **Resources**: This part costs **24 steel**, which is double the amount required by the SuperArmorWedge (12 steel).
- **MaxHealth**: The SuperArmor has **8,000 health**, significantly higher than the SuperArmorWedge's 4,000. This reflects the part's role as a heavier armor piece.
- **Size**: Both parts are 1x1 in size.
- **ExplosiveDamageAbsorption** and **ExplosiveDamageResistance**: These remain the same as the wedge part.

#### **Key Observation**: The increased health and steel cost make this part a stronger, more durable armor piece compared to the wedge.

---

### **3. Buffs and Penetration Resistance**

This section controls how the part interacts with buffs and penetration attacks, with only slight differences from the wedge.

```plaintext
    InitialPenetrationResistance = 7
    ContinuingPenetrationResistance = &InitialPenetrationResistance
    ReceivableBuffs : ^/0/ReceivableBuffs []
```

- **Penetration Resistance**: This part has **7 penetration resistance**, which is higher than the wedge’s 5. This means it can better resist attacks that attempt to penetrate the armor.
- **ReceivableBuffs**: Like the previous example, the part can receive buffs through inheritance (`^/0`).

#### **Key Observation**: The higher penetration resistance further emphasizes this part's role as a tougher armor piece compared to the SuperArmorWedge.

---

### **4. Wall and Door Properties**

The wall and door properties are nearly identical to the wedge example, but a couple of differences stand out.

```plaintext
    IsWalled = true
    AllowedDoorLocations = []
    GeneratorRequiresDoor = false
    IgnoreRotationForMirroredSelection = true
```

- **IsWalled**: This part also has walls, similar to the wedge.
- **AllowedDoorLocations** and **GeneratorRequiresDoor**: Like the wedge, this part doesn’t require doors.
- **IgnoreRotationForMirroredSelection**: This is **new** and specific to this part. It ensures that mirrored selection ignores the part’s rotation, providing more flexibility in building designs.

#### **Key Observation**: The addition of `IgnoreRotationForMirroredSelection` is unique to this part, which allows more control when using the part in mirrored layouts.

---

### **5. Graphics and Colliders**

As with the wedge, this section handles the visuals and collision behavior, but the graphics layers are more straightforward here.

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
        Graphics
        {
            Floor { ... }
            Walls { ... }
            Roof { ... }
        }
    }
```

- **EditorIcon**: The part uses a 32x32 icon, just like the wedge.
- **Graphics Layers**: The **Floor**, **Walls**, and **Roof** sections use simpler graphics compared to the wedge, which had more complex wall placement (external and internal). This part uses the general **"walls"** layer instead of the **"external_walls"** and **"internal_walls"** used in the wedge.

#### **Key Observation**: The graphical representation of the SuperArmor is simpler compared to the wedge, with fewer specific wall placements and a focus on overall coverage.

---

### **6. EMP and Components**

The EMP absorption component remains similar, but with higher absorption values.

```plaintext
        EmpAbsorber
        {
            Type = ExplosiveResourceDrainSink
            ResourceType = battery
            AbsorbsResourceDrain = 1000
            RecoveryRate = (&AbsorbsResourceDrain) * 0.1
        }
```

- **EmpAbsorber**: This part can absorb **1,000 units of battery drain**, double the absorption rate of the wedge (500). The recovery rate is 10% of the absorbed value, the same as before.

#### **Key Observation**: The higher EMP absorption rate aligns with the stronger, more durable nature of the SuperArmor compared to the SuperArmorWedge.

---

### **7. Destroyed Effects**

```plaintext
        DestroyedEffects
        {
            Type = DeathEffects
            MediaEffects = &/COMMON_EFFECTS/SmallPartDestroyedDry
            Location = [.5, .5]
        }
```

- **DestroyedEffects**: The same destruction effects are used here as in the wedge, triggering when the part is destroyed.

#### **Key Observation**: No differences in destruction behavior between the two parts.

---

### **8. Blueprints and Stats**

Like the previous example, this section defines how the part appears in blueprints and calculates dynamic stats.

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

- **Blueprints**: The blueprint uses a simple sprite like the wedge.
- **Stats (EMPResist)**: The EMP resistance is dynamically calculated based on the part’s absorption rate, divided by 1000. Since this part absorbs 1000 units of battery drain, its EMP resistance will be `1.0`.

#### **Key Observation**: The EMP resistance for this part is higher than the wedge due to its higher absorption rate.

---

### **Comparative Observations**
1. **Health and Resistance**: The SuperArmor is a much stronger part than the wedge, with double the health and higher penetration resistance.
2. **Resource Cost**: The SuperArmor also costs more (24 steel compared to 12 for the wedge), reflecting its higher durability.
3. **Graphics Complexity**: The SuperArmor has simpler graphics layers compared to the wedge, with less distinction between internal and external walls.
4. **Mirroring Flexibility**: The SuperArmor includes the `IgnoreRotationForMirroredSelection` attribute, offering greater flexibility in building layouts when using mirrored selections.
5. **EMP Absorption**: The EMP absorption rate is higher for the SuperArmor (1000 vs. 500), making it more resistant to EMP attacks.

---

### **General Tips for Modders**
- **Choose Attributes Based on Role**: Parts like the SuperArmor have higher health and resistance, making them ideal for defensive roles, whereas parts like the SuperArmorWedge can offer more flexible placement due to their rotateability and wall structure.
- **Mirrored Selection**: If you're creating parts intended for symmetrical ship designs, consider using the `IgnoreRotationForMirroredSelection` option to allow more control over how parts behave during mirrored building.
- **Graphical Simplicity**: Not all parts require complex graphical distinctions between internal and external walls. Decide based on how the part is intended to function.
