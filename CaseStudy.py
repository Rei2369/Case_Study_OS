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
def simulate_all():
    try:
        frames = int(entry_frames.get())
        if frames <= 0:
            raise ValueError

        reference_string = get_reference_string()

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

 # FIFO Only
def run_fifo_only():
    try:
        frames = int(entry_frames.get())
        if frames <= 0:
            raise ValueError

        reference_string = get_reference_string()
        result = fifo(reference_string, frames)
        result_text = f" Reference String:\n{reference_string}\n\nFIFO Page Faults: {result}"
        animate_output(result_text)

    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid frames or reference string.")

# LRU Only
def run_lru_only():
    try:
        frames = int(entry_frames.get())
        if frames <= 0:
            raise ValueError

        reference_string = get_reference_string()
        result = lru(reference_string, frames)
        result_text = f" Reference String:\n{reference_string}\n\nLRU Page Faults: {result}"
        animate_output(result_text)

    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid frames or reference string.")

# OPT Only
def run_opt_only():
    try:
        frames = int(entry_frames.get())
        if frames <= 0:
            raise ValueError

        reference_string = get_reference_string()
        result = optimal(reference_string, frames)
        result_text = f" Reference String:\n{reference_string}\n\nOPT Page Faults: {result}"
        animate_output(result_text)

    except ValueError:
        messagebox.showerror("Invalid Input", "Invalid frames or reference string.")

# Generate Reference String
def get_reference_string():
    input_str = entry_ref_string.get().strip()
    if input_str:
        reference_string = [int(x.strip()) for x in input_str.split(',') if x.strip().isdigit()]
        if not reference_string:
            raise ValueError
    else:
        reference_string = generate_reference_string()
    return reference_string

# \o/ GUI \o/
root = tk.Tk()
root.title("Page Replacement Simulator")
root.geometry("700x600")
root.configure(bg="#2f94c3")

# Fonts
label_font = font.Font(family="Segoe UI", size=12)
title_font = font.Font(family="Segoe UI", size=16, weight="bold")

# Page Title
tk.Label(root, text="Page Replacement Simulator", font=title_font, bg="#2f94c3", fg="#003366").pack(pady=20)

# Frames input
tk.Label(root, text="Enter the number of page frames:", font=label_font, bg="#2f94c3").pack()
entry_frames = tk.Entry(root, font=label_font, width=10, justify="center")
entry_frames.pack(pady=5)

# Reference string input
tk.Label(root, text="Enter reference string (comma-separated):", font=label_font, bg="#2f94c3").pack()
entry_ref_string = tk.Entry(root, font=label_font, width=50, justify="center")
entry_ref_string.pack(pady=5)

# Generate random button
tk.Button(root, text="Generate Random Reference String", font=label_font,
          bg="#1E8E74", fg="white", activebackground="#388e3c",
          command=lambda: entry_ref_string.delete(0, tk.END) or entry_ref_string.insert(
              0, ",".join(map(str, generate_reference_string()))
          )).pack(pady=5)

# \o/ Algorithm Buttons (Horizontal) \o/
algo_button_frame = tk.Frame(root, bg="#2f94c3")
algo_button_frame.pack(pady=5)

tk.Button(algo_button_frame, text="FIFO", font=label_font,
          bg="#7c3885", fg="white", activebackground="#1565c0",
          padx=10, pady=5, command=run_fifo_only).pack(side="left", padx=5)

tk.Button(algo_button_frame, text="LRU", font=label_font,
          bg="#8c2450", fg="white", activebackground="#2e7d32",
          padx=10, pady=5, command=run_lru_only).pack(side="left", padx=5)

tk.Button(algo_button_frame, text="OPT", font=label_font,
          bg="#964f2c", fg="white", activebackground="#bf360c",
          padx=10, pady=5, command=run_opt_only).pack(side="left", padx=5)

# Start simulation button (FIFO, LRU, OPT)
tk.Button(root, text="ALL ALGORITHMS", font=label_font,
          bg="#bb223e", fg="white", activebackground="#005c99",
          padx=10, pady=5, command=simulate_all).pack(pady=10)

# Output 
output_label = tk.Label(root, text="", font=label_font, justify="left",
                        bg="#2f94c3", fg="#002244", anchor="nw")
output_label.pack(pady=10)

root.mainloop()