import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog

def upload_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
    if file_path:
        input_field.insert(tk.END, f"\n[Attached: {file_path}]")  # Show file in input field
        print(f"File selected: {file_path}")

def submit():
    prompt = input_field.get("1.0", tk.END).strip()
    print(f"Submitted prompt: {prompt}")

def handle_paste(event):
    clipboard_data = root.clipboard_get()
    if clipboard_data.startswith("file://"):  # Check if clipboard contains file path
        file_path = clipboard_data.replace("file://", "")
        input_field.insert(tk.END, f"\n[Attached: {file_path}]")
    else:
        input_field.insert(tk.END, clipboard_data)

def set_prompt(prompt):
    input_field.delete(0, tk.END)
    input_field.insert(0, prompt)

# Create the main window
root = ttk.Window(themename="darkly")  # Using a modern theme
root.title("Prompt Input App")
root.geometry("1000x900")
root.configure(bg="black")

# Create a frame to center all contents
center_frame = tk.Frame(root, bg="black")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Create and place the title label
title_label = ttk.Label(root, text="Enter your prompts", font=("Arial", 20, "bold"), bootstyle="light")
title_label.pack(pady=20)

# Create a rounded multi-line input field
input_field = tk.Text(root, width=50, height=2, font=("Arial", 13), wrap="word", bg="black", fg="white", insertbackground="white")
input_field.pack(pady=10)

# Bind paste event
input_field.bind("<Control-v>", handle_paste)

# Create and place the upload button
upload_button = ttk.Button(root, text="Upload File", command=upload_file, bootstyle="outline-primary", padding=10)
upload_button.pack(pady=10)

# Create and place the submit button
submit_button = ttk.Button(root, text="Submit", command=submit, bootstyle="success", padding=10)
submit_button.pack(pady=10)

# Create and place the clickable text lines
prompt1 = tk.Label(center_frame, text="enter a prompt", fg="white", cursor="hand2", bg="black")
prompt1.pack(pady=5)
prompt1.bind("<Button-1>", lambda e: set_prompt("enter a prompt"))

prompt2 = tk.Label(center_frame, text="enter another prompt", fg="white", cursor="hand2", bg="black")
prompt2.pack(pady=5)
prompt2.bind("<Button-1>", lambda e: set_prompt("enter another prompt"))

# Start the main event loop
root.mainloop()