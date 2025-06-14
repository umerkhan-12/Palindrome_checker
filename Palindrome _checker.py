import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import threading
import time
import winsound  # Use pygame if you are on Linux/Mac
from time import sleep

# --- Setup ---
root = ttk.Window(themename="superhero")
root.title("PDA Palindrome Checker")
root.geometry("1200x900")
root.resizable(False, False)

dark_mode = False
mode = tk.StringVar(value="standard")

# --- Functions ---

def is_valid_input(s):
    if mode.get() == "numeric":
        return all(c in '0123456789' for c in s)
    return all(c in 'ab' for c in s)

def show_length_stats(s):
    length = len(s)
    if length > 10:
        return "Long string (10+ chars)"
    elif length > 5:
        return "Medium string (6-10 chars)"
    else:
        return "Short string (≤5 chars)"

def play_sound(is_palindrome):
    try:
        if is_palindrome:
            winsound.Beep(1000, 300)
        else:
            winsound.Beep(400, 300)
    except:
        pass  # Avoid crash on non-Windows systems

def add_to_history(input_str, is_palindrome):
    status = "✓" if is_palindrome else "✗"
    history_listbox.insert(0, f"{status} {input_str}")

def export_results():
    with open("palindrome_results.txt", "w", encoding="utf-8") as f:
        for i in range(history_listbox.size()):
            f.write(history_listbox.get(i) + "\n")
    status_bar.config(text="All history exported to palindrome_results.txt")



def show_help():
    help_text = """Palindrome Checker Help:
    
1. Enter a string containing 'a' and 'b' or numbers (0-9).
2. Check is automatic while typing.
3. View stack operations animated below.
4. Use Export button to save results.
5. Toggle Dark Mode if preferred.
"""
    messagebox.showinfo("Help", help_text)

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    theme = "superhero" if dark_mode else "flatly"
    root.style.theme_use(theme)

def animate_stack_operations(input_str):
    stack_output.delete(1.0, tk.END)
    stack_output.insert(tk.END, "Starting animation...\n\n")
    root.update()
    
    stack = []
    n = len(input_str)
    
    # Push animation
    for i in range(n // 2):
        stack.append(input_str[i])
        stack_output.insert(tk.END, f"→ Pushed '{input_str[i]}'\n")
        root.update()
        sleep(0.3)
    
    # Compare animation
    start = n // 2 if n % 2 == 0 else (n // 2 + 1)
    palindrome = True
    for i in range(start, n):
        if stack and stack[-1] == input_str[i]:
            popped = stack.pop()
            stack_output.insert(tk.END, f"← Popped '{popped}' (Matches '{input_str[i]}')\n")
        else:
            palindrome = False
            stack_output.insert(tk.END, f"✗ Mismatch at position {i}\n")
        root.update()
        sleep(0.3)

    # Length stats
    stack_output.insert(tk.END, f"\nLength Analysis: {show_length_stats(input_str)}\n")

    result_label.config(text="Palindrome ✓" if palindrome else "Not a Palindrome ✗")
    add_to_history(input_str, palindrome)
    play_sound(palindrome)

def simulate():
    input_str = entry.get().strip()
    cleaned_input = input_str.replace(" ", "").lower()

    if not cleaned_input:
        result_label.config(text="Enter input.")
        return
    
    if not is_valid_input(cleaned_input):
        result_label.config(text="Invalid input for current mode!")
        return

    start_time = time.perf_counter()
    threading.Thread(target=animate_stack_operations, args=(cleaned_input,)).start()
    end_time = time.perf_counter()
    status_bar.config(text=f"Processed in {(end_time-start_time)*1000:.2f} ms")

def on_key_release(event):
    input_str = entry.get().strip()
    if input_str:
        simulate()
    else:
        result_label.config(text="")
        stack_output.delete(1.0, tk.END)

# --- Widgets ---

# Title
ttk.Label(root, text="PDA Palindrome Checker", font=("Helvetica", 22)).pack(pady=10)

# Entry
entry = ttk.Entry(root, font=("Helvetica", 18), width=30)
entry.pack(pady=10)
entry.bind("<KeyRelease>", on_key_release)

# Mode selection
ttk.Label(root, text="Mode:").pack(pady=2)
ttk.Radiobutton(root, text="Standard (a/b)", variable=mode, value="standard").pack()
ttk.Radiobutton(root, text="Numeric (0-9)", variable=mode, value="numeric").pack()

# Result label
result_label = ttk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=10)

# Stack output
stack_output = tk.Text(root, height=12, width=50, font=("Courier", 12))
stack_output.pack(pady=10)

# History Listbox
ttk.Label(root, text="History:").pack(pady=5)
history_listbox = tk.Listbox(root, height=5, width=50)
history_listbox.pack(pady=5)

# Buttons Frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Export Results", command=export_results).pack(side=LEFT, padx=5)
ttk.Button(button_frame, text="Toggle Dark Mode", command=toggle_dark_mode).pack(side=LEFT, padx=5)
ttk.Button(button_frame, text="Help", command=show_help).pack(side=LEFT, padx=5)

# Status Bar
status_bar = ttk.Label(root, text="Ready", font=("Helvetica", 10), anchor="w")
status_bar.pack(side=BOTTOM, fill=X)

# --- Mainloop ---
root.mainloop()
