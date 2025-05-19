import tkinter as tk
from tkinter import messagebox, font
import random

def generate_reference_string(length=20, page_range=10):
    return [random.randint(0, page_range - 1) for _ in range(length)]

def fifo(pages, frames):
    memory, page_faults = [], 0
    for page in pages:
        if page not in memory:
            if len(memory) >= frames:
                memory.pop(0)
            memory.append(page)
            page_faults += 1
    return page_faults

def lru(pages, frames):
    memory, page_faults, recent = [], 0, []
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

def simulate():
    try:
        frames = int(entry_frames.get())
        if frames <= 0:
            raise ValueError
        pages = generate_reference_string()
        result = f"📘 Reference String:\n{pages}\n\n"
        result += f"🟦 FIFO Faults:  {fifo(pages, frames)}\n"
        result += f"🟩 LRU Faults:   {lru(pages, frames)}\n"
        result += f"🟥 OPT Faults:   {optimal(pages, frames)}"
        output_label.config(text=result)
    except ValueError:
        messagebox.showerror("❌ Invalid Input", "Please enter a positive integer for frames.")

# GUI Setup
root = tk.Tk()
root.title("📄 Page Replacement Simulator")
root.geometry("600x400")
root.configure(bg="#f4f4f8")

custom_font = font.Font(family="Segoe UI", size=12)

tk.Label(root, text="Page Replacement Algorithm Simulator", font=("Segoe UI", 16, "bold"),
         fg="#333", bg="#f4f4f8").pack(pady=15)

tk.Label(root, text="Enter number of page frames:", font=custom_font, bg="#f4f4f8").pack()
entry_frames = tk.Entry(root, font=custom_font, width=10, justify="center")
entry_frames.pack(pady=5)

tk.Button(root, text="Run Simulation", font=custom_font, bg="#4caf50", fg="white",
          activebackground="#45a049", padx=10, pady=5, command=simulate).pack(pady=10)

output_label = tk.Label(root, text="", font=custom_font, justify="left", bg="#ffffff", anchor="nw",
                        fg="#222", width=60, height=10, bd=1, relief="solid", padx=10, pady=10)
output_label.pack(pady=10)

root.mainloop()
