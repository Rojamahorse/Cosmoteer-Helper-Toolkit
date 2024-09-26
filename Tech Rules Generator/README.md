# Tech.rules Generator

## Overview

The TechRules Generator is a Python script with a graphical user interface (GUI) designed to help you quickly generate techrules formatted code for use in your mod files. The script allows you to input various fields, generates the corresponding code, and provides options to copy the code to the clipboard or save it as a `.txt` file.

## Requirements

Before you can use the TechRules Generator, ensure that you have the following installed on your machine:

1. **Python 3.x** - You can download Python from the official website: [python.org](https://www.python.org/).
2. **Python `tkinter` Library** - This library is included with most standard Python installations.
3. **Python `pyperclip` Module** - This module is required for clipboard operations.

## Setup Instructions

### 1. Install Python

If you haven't already, download and install Python from [python.org](https://www.python.org/). Make sure to add Python to your system PATH during the installation process.

### 2. Install Required Python Modules

To install the `pyperclip` module, follow these steps:

1. Open a command prompt (Windows) or terminal (Mac/Linux).
2. Run the following command:

   ```sh
   pip install pyperclip
   ```

### 3. Running the Script

Once you've installed the required dependencies, you can run the TechRules Generator script:

1. Navigate to the directory where the script is located. For example:

   ```sh
   cd "C:\Users\YourUsername\Saved Games\Cosmoteer\76561197993324838\Mods\Star-Wars-A-Cosmos-Divided"
   ```

2. Run the script using Python:

   ```sh
   python tool_techrules_generator.py
   ```

### 4. Using the TechRules Generator

#### Step 1: Enter the Relative Path to `tech.rules`

- **What is a relative path?**
  - A relative path is a way to specify the location of a file or directory relative to the current directory. For example, if your `tech.rules` file is located two directories up from the root of your mod, you might enter `..\..\tech.rules`.
  
- **How to find the relative path?**
  - Determine the location of your `tech.rules` file relative to the root directory of your mod. If `tech.rules` is in the `MyMod/modes/career/` directory, you're mod's root is `MyMod` directory, the relative path would be `modes/career/tech.rules`.

#### Step 2: Choose Unlock Type

- Select whether the unlock is for a **Part** or a **Toggle Choice**.

#### Step 3: Fill in the Fields

- Enter the required fields such as **Part ID**, **Cost**, **Prerequisite IDs**, etc.
- The script will automatically calculate the necessary path prefixes based on the relative path to `tech.rules` you provided earlier.

#### Step 4: Generate the Code

- Click the "Generate" button to create the techrules formatted code.
- Use the "Copy to Clipboard" button to copy the generated code or the "Save as File" button to save it as a `.txt` file.

## Troubleshooting

- If you encounter an error like `ModuleNotFoundError: No module named 'pyperclip'`, make sure you've installed the `pyperclip` module using the `pip install pyperclip` command.

## License

This tool is provided as-is, without any warranty. Use it at your own risk.

## Contribution

I do this for fun and don't need the support but if you'd like to contribute, feel free to make a donation to your favorite charity, or better yet fork the repository, submit a pull request, and help me make this tool even better! If you still feel compelled to contribute to me directly you can [venmo me a coffee](https://www.venmo.com/u/Rojamahorse)"# Tech.rules Generator" 
