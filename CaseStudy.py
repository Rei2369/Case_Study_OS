import tkinter as tk
from tkinter import font, messagebox
import random

# Algorithm
def generate_reference_string(min_length=7, max_length=20, page_range=10):
    length = random.randint(min_length, max_length)
    return [random.randint(0, page_range - 1) for _ in range(length)]

# FIFO
def fifo(pages, frames):
    memory, page_faults = [], 0
    for page in pages:
        if page not in memory:
            if len(memory) >= frames:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
    return page_faults

# LRU
def lru(pages, frames):
    memory, recent, page_faults = [], [], 0
    for page in pages:
        if page not in memory:
            if len(memory) >= frames:
                memory.remove(recent.pop(0))
            memory.append(page)
            page_faults += 1
        else:
            recent.remove(page)
        recent.append(page)
    return page_faults

# OPT
def optimal(pages, frames):
    memory, page_faults = [], 0
    for i in range(len(pages)):
        page = pages[i]
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future = pages[i + 1:]
                index_to_replace, farthest = -1, -1
                for mem_page in memory:
                    if mem_page in future:
                        idx = future.index(mem_page)
                        if idx > farthest:
                            farthest = idx
                            index_to_replace = memory.index(mem_page)
                    else:
                        index_to_replace = memory.index(mem_page)
                        break
                memory[index_to_replace] = page
            page_faults += 1
    return page_faults

# Animation Function (ms)
def animate_output(text, delay=500):
    output_label.config(text="")
    lines = text.split('\n')
    display = []

    def show_line(index=0):
        if index < len(lines):
            display.append(lines[index])
            output_label.config(text="\n".join(display))
            output_label.after(delay, show_line, index + 1)

    show_line()

# \o/ Simulation \o/
def simulate():
    try:
        frames = int(entry_frames.get())
        if frames <= 0:
            raise ValueError

        input_str = entry_ref_string.get().strip()
        if input_str:
            reference_string = [int(x.strip()) for x in input_str.split(',') if x.strip().isdigit()]
            if not reference_string:
                raise ValueError
        else:
            reference_string = generate_reference_string()

        fifo_result = fifo(reference_string, frames)
        lru_result = lru(reference_string, frames)
        opt_result = optimal(reference_string, frames)

        result_text = (
            f" Reference String:\n{reference_string}\n\n"
            f" FIFO Page Faults: {fifo_result}\n"
            f" LRU Page Faults:  {lru_result}\n"
            f" OPT Page Faults:  {opt_result}"
        )

        animate_output(result_text)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number and reference string.")

# \o/ GUI \o/
root = tk.Tk()
root.title("Page Replacement Simulator")
root.geometry("700x550")
root.configure(bg="#e0f4ff")  # Blue-themed background

# Fonts
label_font = font.Font(family="Segoe UI", size=12)
title_font = font.Font(family="Segoe UI", size=16, weight="bold")

# Page Title
tk.Label(root, text="Page Replacement Simulator", font=title_font, bg="#e0f4ff", fg="#003366").pack(pady=20)

# Frames input
tk.Label(root, text="Enter the number of page frames:", font=label_font, bg="#e0f4ff").pack()
entry_frames = tk.Entry(root, font=label_font, width=10, justify="center")
entry_frames.pack(pady=5)

# Reference string input
tk.Label(root, text="Enter reference string (comma-separated):", font=label_font, bg="#e0f4ff").pack()
entry_ref_string = tk.Entry(root, font=label_font, width=50, justify="center")
entry_ref_string.pack(pady=5)

# Generate random button
tk.Button(root, text="Generate Random Reference String", font=label_font,
          bg="#4caf50", fg="white", activebackground="#388e3c",
          command=lambda: entry_ref_string.delete(0, tk.END) or entry_ref_string.insert(
              0, ",".join(map(str, generate_reference_string()))
          )).pack(pady=5)

# Start simulation button
tk.Button(root, text="Start Simulation", font=label_font,
          bg="#007acc", fg="white", activebackground="#005c99",
          padx=10, pady=5, command=simulate).pack(pady=10)

# Output 
output_label = tk.Label(root, text="", font=label_font, justify="left",
                        bg="#e0f4ff", fg="#002244", anchor="nw")
output_label.pack(pady=10)

root.mainloop()
