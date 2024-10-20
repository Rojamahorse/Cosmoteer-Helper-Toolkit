### **Summary**

This document explains how to work with paths, inheritance, and references when configuring `.rules` files in Cosmoteer. It provides detailed guidelines on referencing files, using inheritance, and applying special notations for flexible modding. The document covers basic path structures, the difference between copy-references and actual references, inheritance operations, and advanced referencing techniques. These guidelines ensure proper file organization and behavior when modifying or creating new game content in the Cosmoteer modding environment.

---

### **1. Paths and Referencing in Cosmoteer**

#### **1.1 Basic Path Structure**
- Paths in Cosmoteer work similarly to file paths in an operating system but offer additional complexity to enhance mod flexibility.
- **Example Path**: `./Data/ships/terran/armor/icon.png`
- **Quotation Marks Usage**:
  - When referencing paths in `.rules` files (e.g., `NormalsFile = "silver_normals.png"`).
  - When paths contain special characters or spaces.
  - General best practice in complex modding scenarios.

#### **1.2 Path Components and Notation**
- **&**: Indicates that the path is within a `.rules` file.
- **<>**: Encapsulates regular file paths.
- **{}**: Denotes a node within a file.
- **[]**: Denotes a list within a file (indexed starting at 0).
- **~**: Indicates value copy from the referenced path.
  
#### **1.3 Special Path Notations**
- `./`: Starts at the top level of the game’s data files.
- `../`: Moves up one level from the current node or file.
- `~/`: Starts at the top of the current `.rules` file.
- `^/`: References data inherited from another node (useful for non-list data).

---

### **2. Substitution and Code References**

#### **2.1 Ampersand (&) Usage**
- The `&` symbol copies the data from the specified path, creating a copy-reference.
  
#### **2.2 Copy-Reference vs. Actual Reference**
- **Copy-Reference (`&`)**:
  - Data is copied into your file.
  - **Analogy**: Like copying a Wikipedia article into a document—your copy remains unchanged if the original changes.
- **Actual Reference (No `&`)**:
  - Creates a dynamic link to the original data.
  - **Analogy**: Like pasting a Wikipedia URL into a document—if the article changes, the linked content will update.
  
#### **2.3 Example**
- **Copy-Reference**: `&<super_armor/super_armor.rules>/Part`
- **Actual Reference**: `<super_armor/super_armor.rules>/Part`

---

### **3. Inheritance in Cosmoteer**

#### **3.1 Inheritance Syntax**
- **::**: Denotes an inheritance operation, creating a new node by inheriting properties from another node. Must be followed by `{}` to define modifications.

#### **3.2 Example of Inheritance Error**
- **Issue**: Missing `{}` after inheritance operation.
- **Fix**: Add `{}` after `::` or replace `::` with `=`.

---

### **4. Common Path Syntax Examples**
- **Setting a Stack Size**:
  ```plaintext
  MaxStackSize = (&<./Data/resources/carbon/carbon.rules>/MaxStackSize)
  ```
- **Referencing a File**:
  ```plaintext
  NormalsFile = "silver_normals.png"
  ```

---

### **5. Advanced Inheritance and Referencing in Cosmoteer**

#### **5.1 Multiple Inheritance**
- A node can inherit from multiple sources, separating sources with commas.
- **Order of Inheritance**: The last listed node takes precedence over previous ones.
  ```yaml
  NodeA : NodeB, NodeC
  ```
  - **Example**: If both `NodeB` and `NodeC` share the same property, `NodeB` takes precedence.
  
#### **5.2 Using Caret (^) for Relative Referencing**
- **Caret Notation**: The `^` symbol references a parent node's inherited properties.
  - **Example**: `NodeB : ^/0/NodeF` references the first inherited node.
  - **Path Navigation**: You can use relative paths with caret notation:
    ```plaintext
    NodeB : ^/0/../NodeE
    ```

#### **5.3 Complex Path Resolution**
- **Node Inheritance in Nested Structures**: When inheriting within nested nodes, use both caret notation and relative paths.
  ```plaintext
  NodeG: &../^/0/NodeF
  ```

#### **5.4 Avoiding Errors**
- Be cautious with caret notation, as incorrect paths like `NodeB : ^/0/NodeF` can cause "path not found" errors.

---

### **6. Additional Examples for Clarification**

#### **6.1 Multiple Inheritance Example**
```yaml
NodeA : NodeB, NodeC
```
- `NodeA` inherits from `NodeB` first, then `NodeC`. Properties from `NodeB` take precedence.

#### **6.2 Complex Referencing Example**
- Using caret notation to reference an inherited node's property:
  ```plaintext
  NodeB : ^/0/../NodeE
  ```
- Copying a deeply nested path:
  ```plaintext
  NodeG: &../^/0/NodeF
  ```

---
