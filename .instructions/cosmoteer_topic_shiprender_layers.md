To simplify the render layers and explain the order of precedence in this code, we can break it down into different categories and their rendering order from bottom to top. The "UniqueBucket" value determines which layer gets rendered first, with lower numbers being rendered first and higher numbers appearing on top. Here's a breakdown:
    1. Structure Layers (Rendered First, Bottom):
        ○ Structure (UniqueBucket = -800): The base structure of the ship, usually the lowest layer.
        ○ Construction Structure (UniqueBucket = -750): Represents construction phase visuals for the structure.
    2. Floor Layers:
        ○ Floors (UniqueBucket = -700): Represents the floor of the ship, appearing on top of the structure layer.
    3. Turrets and Doodads:
        ○ Turrets (UniqueBucket = -600): Basic turrets that are mounted on the ship, rendered above the floors.
        ○ Low-Level Doodads (UniqueBucket = -500): Small details or decorations that are part of the ship, but below the walls.
    4. Wall and Door Layers:
        ○ Walls Stencil (UniqueBucket = -400): Used for rendering stencil effects for walls.
        ○ External Walls (UniqueBucket = -300): Exterior walls of the ship, rendered higher than internal structures.
        ○ Walls (UniqueBucket = -200): General walls inside the ship, rendered on top of external walls.
        ○ Doors (UniqueBucket = -100): Ship doors, placed on top of walls but below other elements.
    5. Crew and Weapons Layers:
        ○ Weapons (UniqueBucket = 0): Weapons mounted on the ship, rendered after the crew is placed (though crew isn't defined here, they are mentioned as being rendered between doors and weapons).
    6. High-Level Doodads and Lighting:
        ○ High-Level Doodads (UniqueBucket = 100): Decorative objects placed higher in the rendering order, on top of weapons.
        ○ Additive Lights (UniqueBucket = 200): Lights that add glow or effects to the ship.
        ○ Fire (UniqueBucket = 300): Fire effects for damage or destruction, rendered above most objects.
    7. Roof and Roof Doodads (Rendered Later, Top Layers):
        ○ Roofs (UniqueBucket = 1000): Roofs of the ship, rendered on top of all interior elements.
        ○ Roof Doodads (UniqueBucket = 1100): Decorative elements on the roof, such as antennas or other details.
        ○ Roof Turrets (UniqueBucket = 1200): Turrets that are mounted on the roof.
        ○ Roof Lights (UniqueBucket = 1300): Advanced lighting effects applied on the roof, such as lights with specific blending.
    8. Indicators and Fire Alerts (Rendered Last, On Top of Everything):
        ○ Fire Indicators (UniqueBucket = 1900): Fire damage indicators that are drawn specifically for the player, appearing on top of all other layers.
Simplified Explanation:
    • Floor is rendered below walls and turrets.
    • Roofs are rendered on top of everything, so any image applied to anything prefixed with "roof" would would be displayed above the floors, walls, and turrets.
    • Lighting and indicators are rendered last, making them the highest layer.
