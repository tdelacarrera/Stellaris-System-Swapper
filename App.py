import re
import tkinter as tk
from tkinter import filedialog, messagebox

#extract the galactic_objects block
def extract_galactic_object_block(content):
    match = re.search(pattern=r'galactic_object\s*=\s*\{(.*?)\n\}', string= content, flags = re.DOTALL)
    if not match:
        raise ValueError("Galactic Object block not found")
    start, end = match.span(1)
    return start, end, content[start:end]

#extract the precursors flags
def extract_precursor_flags(system):
    match = re.search(pattern=r'(flags\s*=\s*\{.*?\})', string=system, flags=re.DOTALL)
    if not match:
        return None
    flags_block = match.group(1)
    precursor_flags = dict(re.findall(pattern=r'(precursor_[^\s=]+)=([0-9]+)', string=flags_block))
    return precursor_flags

#extract hyperlane block
def extract_hyperlane_block(system):
    start_match = re.search(pattern=r'hyperlane\s*=\s*\{', string=system)
    if not start_match:
        return None

    start_index = start_match.start()
    brace_open = 0
    index = start_match.end()

    while index < len(system):
        char = system[index]
        if char == '{':
            brace_open += 1
        elif char == '}':
            if brace_open == 0:
                return system[start_index:index+1]
            brace_open -= 1
        index += 1
    return None


#extract the arm of the system
def extract_arm(system):
    match = re.search(pattern=r'\barm=([0-9]+)', string=system)
    if not match:
        return None
    return match.group(1)

#extract the index of the system
def extract_index(system):
    match = re.search(pattern=r'\bindex=([0-9]+)', string=system)
    if not match:
        return None
    return match.group(1)

#extract the coordinates of the system
def extract_coordinates(system):
    match = re.search(pattern=r'coordinate\s*=\s*\{\s*[^}]*?x=([-\d\.]+)\s+y=([-\d\.]+)', string=system, flags=re.DOTALL)
    if not match:
        raise ValueError("Coordinates not found.")
    x, y = match.groups()
    return x, y

#replace the hyperlane block between the systems
def replace_hyperlane_block(system: str, new_hyperlane_block: str) -> str:
    start = system.find('hyperlane=')
    if start == -1:
        return system

    index = start + len('hyperlane=')
    while index < len(system) and system[index].isspace():
        index += 1

    if index >= len(system) or system[index] != '{':
        return system

    brace_count = 1
    index += 1
    end = index

    while index < len(system) and brace_count > 0:
        if system[index] == '{':
            brace_count += 1
        elif system[index] == '}':
            brace_count -= 1
        index += 1

    end = index
    old_block = system[start:end]
    return system.replace(old_block, new_hyperlane_block)

#replace coordinates
def replace_coordinates(system, new_x, new_y):
    system = re.sub(pattern=r'(x=)([-\d\.]+)', repl=lambda m: f'{m.group(1)}{new_x}', string=system)
    system = re.sub(pattern=r'(y=)([-\d\.]+)', repl=lambda m: f'{m.group(1)}{new_y}', string=system)
    return system

#replace index
def replace_index(system, new_index):
    system = re.sub(pattern=r'\bindex\s*=\s*-?\d+(?:\.\d+)?', repl=f'index={new_index}', string=system)
    return system

#replace arm
def replace_arm(system, new_arm):
    system = re.sub(pattern=r'\barm\s*=\s*-?\d+(?:\.\d+)?', repl=f'arm={new_arm}', string=system)
    return system



def replace_precursor_flags(system: str, new_flags: dict) -> str:
    def repl(match):
        original_flags = match.group(1)
        lines = original_flags.splitlines()

        # Clean all precursor flags
        cleaned_lines = [
            line for line in lines if not re.search(pattern=r'\bprecursor_[^\s=]+', string=line)
        ]

        # Add new precursor flags
        if new_flags:
            new_lines = [f'\t\t\t{k}={v}' for k, v in new_flags.items()]
            cleaned_lines += new_lines

        # Rebuild block
        result = 'flags=\n\t\t{\n' + '\n'.join(cleaned_lines) + '\n\t\t}'
        return result

    return re.sub(pattern=r'flags\s*=\s*\{(.*?)\}', repl=repl, string=system, flags=re.DOTALL)

#get all the block of a system by id
def get_system_by_id(block: str, id: int) -> str:
    pattern = rf'\b{id}\s*=\s*\{{'
    match = re.search(pattern, block)
    if not match:
        raise ValueError(f"System with id {id} not found")

    start = match.start()
    index = match.end()
    brace_count = 1

    while index < len(block):
        char = block[index]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                return block[start:index + 1]
        index += 1

    raise ValueError(f"System block for id {id} not properly closed")

#update the hyperlane connetions of all systems connected to the two systems
def update_connected_hyperlanes(block: str, id1: str, id2: str) -> str:
    index = 0
    updated_block = block

    while index < len(updated_block):
        match = re.search(r'\b(\d+)\s*=\s*\{', updated_block[index:])
        if not match:
            break

        start = index + match.start()
        brace_index = start + match.group(0).find('{') + 1
        brace_count = 1
        i = brace_index

        while i < len(updated_block) and brace_count > 0:
            if updated_block[i] == '{':
                brace_count += 1
            elif updated_block[i] == '}':
                brace_count -= 1
            i += 1

        system_block = updated_block[start:i]

        hyperlane_match = re.search(pattern=r'(hyperlane\s*=\s*\{)', string=system_block)
        if hyperlane_match:
            h_start = hyperlane_match.start()
            hl_brace_index = h_start + hyperlane_match.group(1).find('{') + 1
            brace_count = 1
            j = hl_brace_index

            while j < len(system_block) and brace_count > 0:
                if system_block[j] == '{':
                    brace_count += 1
                elif system_block[j] == '}':
                    brace_count -= 1
                j += 1

            hyperlane_block = system_block[h_start:j]

            temp_1 = "TO_TEMP_1"
            temp_2 = "TO_TEMP_2"
            block_temp = re.sub(pattern=rf'\bto={id1}\b', repl=f'to={temp_1}', string=hyperlane_block)
            block_temp = re.sub(pattern=rf'\bto={id2}\b', repl=f'to={temp_2}', string=block_temp)
            block_temp = re.sub(pattern=rf'\bto={temp_1}\b', repl=f'to={id2}', string=block_temp)
            block_temp = re.sub(pattern=rf'\bto={temp_2}\b', repl=f'to={id1}', string=block_temp)

            system_block = system_block[:h_start] + block_temp + system_block[j:]

        updated_block = updated_block[:start] + system_block + updated_block[i:]
        index = start + len(system_block)

    return updated_block

def swap_system_data(block, id1, id2):
    #extract system blocks
    system1 = get_system_by_id(block, id1)
    system2 = get_system_by_id(block, id2)

    #extract the systems values
    x1, y1 = extract_coordinates(system1)
    x2, y2 = extract_coordinates(system2)
    index1 = extract_index(system1)
    index2 = extract_index(system2)
    arm1 = extract_arm(system1)
    arm2 = extract_arm(system2)
    precursors1 = extract_precursor_flags(system1)
    precursors2 = extract_precursor_flags(system2)
    hyperlane1 = extract_hyperlane_block(system1)
    hyperlane2 = extract_hyperlane_block(system2)

    #replace systems values
    system1_modified = replace_coordinates(system1, x2, y2)
    system2_modified = replace_coordinates(system2, x1, y1)
    system1_modified = replace_index(system1_modified, index2)
    system2_modified = replace_index(system2_modified, index1)
    system1_modified = replace_arm(system1_modified, arm2)
    system2_modified = replace_arm(system2_modified, arm1)
    system1_modified = replace_precursor_flags(system1_modified, precursors2)
    system2_modified = replace_precursor_flags(system2_modified, precursors1)
    system1_modified = replace_hyperlane_block(system1_modified, hyperlane2)
    system2_modified = replace_hyperlane_block(system2_modified, hyperlane1)

    updated_block = block.replace(system1, system1_modified).replace(system2, system2_modified)
    updated_block = update_connected_hyperlanes(updated_block, id1, id2)

    return updated_block

def swap(id1, id2):
    global FILE_CONTENT
    # extract galactic object block
    start, end, block = extract_galactic_object_block(FILE_CONTENT)
    # Swap data from the blocks
    updated_block = swap_system_data(block, id1, id2)
    # update content
    FILE_CONTENT = FILE_CONTENT[:start] + updated_block + FILE_CONTENT[end:]
#
def on_browse_input():
    global FILE_CONTENT
    filename = filedialog.askopenfilename(
        title="Select the gamestate",
        filetypes=[("All files", "*.*")])
    if filename:
        with open(filename, "r", encoding="utf-8") as f:
            FILE_CONTENT = f.read()
        input_path_var.set(filename)
        output_path_var.set(filename + "_new")

def on_browse_output():
    filename = filedialog.asksaveasfilename(
        title="Select directory",
        filetypes=[("All files", "*.*")])
    if filename:
        output_path_var.set(filename)

def on_swap():
    global FILE_CONTENT
    output_path = output_path_var.get()
    id1 = id1_var.get().strip()
    id2 = id2_var.get().strip()

    if not FILE_CONTENT or not output_path or not id1 or not id2:
        messagebox.showerror(title="Error", message="Complete all fields.")
        return
    elif not not id1 == id2:
        messagebox.showerror(title="Error", message="The systems ID cannot be the same.")
        return
    try:
        swap(id1, id2)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(FILE_CONTENT)
        messagebox.showinfo(title="Éxito", message=f"Systems swapped")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error :\n{e}")


FILE_CONTENT = None

width = 450
height = 270
root = tk.Tk()
root.withdraw()
root.title("System Swapper")
root.iconbitmap("icon.ico")
root.resizable(width= False, height=False)
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

input_path_var = tk.StringVar()
output_path_var = tk.StringVar()
id1_var = tk.StringVar()
id2_var = tk.StringVar()

# Input file
tk.Label(root, text="Input file").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=input_path_var, width=50).grid(row=0, column=1, padx=5)
tk.Button(root, text="Open", command=on_browse_input).grid(row=0, column=2, padx=5)

# Output file
tk.Label(root, text="Output file").grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=output_path_var, width=50).grid(row=1, column=1, padx=5)
tk.Button(root, text="Save", command=on_browse_output).grid(row=1, column=2, padx=5)

# System 1
tk.Label(root, text="ID System 1").grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=id1_var).grid(row=2, column=1, sticky="w", padx=5)

# System 2
tk.Label(root, text="ID System 2").grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=id2_var).grid(row=3, column=1, sticky="w", padx=5)

# Swap system button
tk.Button(root, text="Swap", command=on_swap, bg="#347aeb", fg="white", font=("Arial", 12)).grid(row=4, column=0, columnspan=3, pady=20)

root.deiconify()
root.mainloop()