
---

### **FlipHRotate and FlipVRotate Explained**

In Cosmoteer, **FlipHRotate** and **FlipVRotate** are attributes used to control how a part rotates when it is flipped horizontally or vertically, such as in mirror mode or when using the copy/paste feature. These attributes are crucial for parts that are not perfectly symmetrical, as the game needs specific instructions on how to handle their rotation when mirrored or flipped.

### **Rotational Values and Their Meanings**

Each part in the game can have four possible rotations, which are represented as integers:

```plaintext
0 = Default (No rotation)
1 = 90 degrees clockwise (or 90 degrees counterclockwise, depending on your perspective)
2 = 180 degrees (flipped upside down)
3 = 270 degrees clockwise (or 90 degrees counterclockwise)
```

### **FlipHRotate and How It Works**

When a part is flipped **horizontally**, the game uses the **FlipHRotate** attribute to determine the new rotation of the part. For example:

```plaintext
FlipHRotate = [1, 0, 3, 2]
```

This tells the game how to adjust the part’s rotation after it has been flipped horizontally. Each value in the array corresponds to what the new rotation should be for each initial state.

#### **Example Breakdown**:
- **If the part's current rotation is 0**, its new rotation after flipping horizontally will be 1 (90 degrees).
- **If the part's current rotation is 1**, its new rotation will be 0 (default/no rotation).
- **If the part's current rotation is 2**, its new rotation will be 3 (270 degrees).
- **If the part's current rotation is 3**, its new rotation will be 2 (180 degrees).

### **FlipVRotate and How It Works**

Similarly, **FlipVRotate** handles flipping **vertically**, ensuring that the part rotates correctly in the vertical axis:

```plaintext
FlipVRotate = [new values]
```

This array works the same way as **FlipHRotate**, but specifically for vertical flips. If a part is symmetrical vertically, you might not need to specify **FlipVRotate**, as the game will automatically flip it correctly.

---

### **When Are These Needed?**

These attributes are only required for parts that are not perfectly symmetrical. For instance, wedge-shaped parts or those with specific orientations may require **FlipHRotate** and **FlipVRotate** values so that the game knows how to handle their rotation when flipped.

If a part is vertically or horizontally symmetrical, you won’t need to specify either attribute because the game can handle the rotation automatically without requiring additional instructions.

---

### **Practical Example: Armor Wedge**

Let’s say you’re modding an armor wedge part. Because the wedge shape isn’t symmetrical, you’ll need to define **FlipHRotate** to ensure it rotates properly when mirrored:

```plaintext
FlipHRotate = [1, 0, 3, 2]
```

- **0 (Default)** will rotate to **1** when flipped horizontally.
- **1 (90 degrees)** will rotate back to **0**.
- **2 (180 degrees)** will rotate to **3**.
- **3 (270 degrees)** will rotate to **2**.

In this way, the part maintains a consistent orientation even when flipped horizontally.

---

### **Summary for Modders**

- **FlipHRotate** and **FlipVRotate** control how parts rotate during horizontal and vertical flipping, respectively.
- These values are particularly important for non-symmetrical parts (like wedges), ensuring that the game correctly adjusts their orientation when mirrored.
- Use an array of four values to indicate how the part should rotate based on its current orientation.
- For symmetrical parts, the game handles rotation automatically, so these values are not needed.

---
