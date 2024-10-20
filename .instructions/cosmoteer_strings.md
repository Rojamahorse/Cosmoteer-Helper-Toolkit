Instructions on syntax and structure of cosmoteer strings files "en.rules", "es.rules", "de.rules", "it.rules", "fr.rules", "zh-cn.rules", "jp.rules", "ru.rules", etc

---

### **File Structure Example**

```plaintext
__Name = "English"
__DebugOnly = false

// Required lines for new language mods; skip for mods adding to existing languages.
```

#### **Parts Example:**
```plaintext
parts 
{
    partAname = "examplename"
    partAdesc = "exampledescription"
    partAicon = "particonname"
}
```

---

### **General Layout & Syntax Rules**
- **Section Layout**:
  ```plaintext
  SECTION
  {
      Key = "Value"
  }
  ```

- **General Layout Tricks**:
  - `\` outside quotes: string continues on the next line.
  - `\n` inside quotes: line break.
  - `&xxxx` copies the value of another string (outside quotes).
    - Example: `partA = &partB`

---

### **Formatting and Special Symbols**
- **Text Styles**:
  - `<b>bold</b>`
  - `<i>italics</i>`
  - `<u>underlined</u>`
  - `<s##>TEXT SIZE</s##>` 
    - *Game uses size 12 as standard, 24 as large text.*

- **Number Reference Replacer**:
  - `{0}`: first value reference. Use `{1}`, `{2}` for subsequent values.
  - Format numbers with precision: `{0:0.00}` (e.g., 1 turns into 1.00).
  - Optional decimal: `{1:0.00#}` (1 → 1.00, 0.333 → 0.334).
  - Insert commas: `{2:n0}` turns 10000 → 10,000.

---

### **Text Colors**
Use the following color tags to display colored text:

| Color | Tag | Example |
|-------|-----|---------|
| Rich Green | `<good></good>` | `<good>Text</good>` |
| Dark Red | `<bad></bad>` | `<bad>Text</bad>` |
| Grey | `<gray></gray>` | `<gray>Text</gray>` |
| White | `<white></white>` | `<white>Text</white>` |
| Cyan | `<cyan></cyan>` | `<cyan>Text</cyan>` |
| Magenta | `<magenta></magenta>` | `<magenta>Text</magenta>` |
| Yellow | `<yellow></yellow>` | `<yellow>Text</yellow>` |
| Orange | `<orange></orange>` | `<orange>Text</orange>` |
| Money Color | `<money_color></money_color>` | `<money_color>Text</money_color>` |

---

### **Advanced Text Formatting**
- **Escape Characters**:
  - Use `\"` to escape quotation marks within strings.
  - Bullet points: `"● BULLET POINT LISTS.\n"`
  - Special characters: `- \u200b` (zero-width space).
    - Example: `"Hyper-\u200bCoil"`, `"Tri-\u200bSteel"`.

- **Dynamic String Insertion**:
  - **String Copy**:
    - `&xxxx` copies string content into another string.
    - Example: `StarshipEngineDesc = "Provides thrust. &CommonDescription"`
  
  - **String Reference**:
    - `<string id='...'/>'` inserts another string’s content.
    - Example: `LaserCannonDesc = "Advanced weapon. <string id='WeaponDesc'/>"`

---

### **Image and Button Insertions**
- **Image Insertion**:
  ```plaintext
  <img name='sort'/>
  <image name='star_system'/>
  <img name='money' colored='true'/>
  <ins_money>{0:n0}</ins_money>
  ```

- **Button Insertion**:
  ```plaintext
  <btn id='Game.xxx'/>
  ```

---

### **Usage Examples**
- **Bullet Point Usage**:
  ```plaintext
  "● BULLET POINT LISTS.\n"
  ```

- **Crew Accessibility Example**:
  ```plaintext
  "<good>✓ Nearest Crew: {0}m</good>"
  "<bad>✘ No Crew Access</bad>"
  ```

- **Warnings**:
  ```plaintext
  "<yellow>⚠️ Nearest {0}: {1}m</yellow>"
  ```

- **Indented Bullet**:
  ```plaintext
  "<yellow> ⮡ </yellow>"
  ```

---

### **Notes on Copying String Keys**
- **Method 1: Using `&xxxx`**:
  - Directly copy the value of another string.
  - Example:
    ```plaintext
    CommonDescription = "Essential for all starships."
    StarshipEngineDesc = "Provides thrust. &CommonDescription"
    ```

- **Method 2: Using `<string id='...'/>`**:
  - Dynamically insert the value of another string.
  - Example:
    ```plaintext
    WeaponDesc = "High damage at long range."
    LaserCannonDesc = "Advanced weapon system. <string id='WeaponDesc'/>"
    ```

- **Best Practice**:
  - Use `&xxxx` for simple string concatenation.
  - Use `<string id='...'/>` for modularity and flexibility.

---