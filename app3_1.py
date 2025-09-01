import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD

def upload_file():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
    if file_path:
        print(f"File selected: {file_path}")
        input_field.delete(0, tk.END)
        input_field.insert(0, file_path)

def submit():
    prompt = input_field.get()
    print(f"Submitted prompt or file: {prompt}")

def set_prompt(prompt):
    input_field.delete(0, tk.END)
    input_field.insert(0, prompt)

def on_drop(event):
    file_path = event.data
    if file_path:
        input_field.delete(0, tk.END)
        input_field.insert(0, file_path)
        print(f"File dropped: {file_path}")

# Create the main window
root = TkinterDnD.Tk()
root.title("Prompt Input App")
root.geometry("1000x900")
root.configure(bg="white")

# Create a frame to center all contents
center_frame = tk.Frame(root, bg="white")
center_frame.place(relx=0.5, rely=0.3, anchor="center")

# Create and place the title label
title_label = tk.Label(center_frame, text="Enter your prompts", font=("Arial", 20, "bold"), bg="white", fg="black")
title_label.pack(pady=20)

# Create and place the input field with drag and drop support
input_field = tk.Entry(center_frame, width=50, bg="white", fg="black", insertbackground="black", font=("Arial", 13))
input_field.pack(pady=20, ipady=10)  # ipady increases height)
input_field.configure(highlightbackground="black", highlightcolor="black", highlightthickness=1)
input_field.drop_target_register(DND_FILES)
input_field.dnd_bind('<<Drop>>', on_drop)

# Create and place the upload button
upload_button = tk.Button(center_frame, text="Browse from PC", command=upload_file, bg="black", fg="white", font=("Arial", 11))
upload_button.pack(pady=14)

# Create and place the submit button
submit_button = tk.Button(center_frame, text="Submit", command=submit, bg="pink", fg="black", font=("Arial", 11))
submit_button.pack(pady=14)

# Create and place the clickable text lines with rounded borders
prompt1 = tk.Label(center_frame, text="Enter a prompt", fg="black", cursor="hand2", bg="white", padx=10, pady=5)
prompt1.pack(pady=5)
prompt1.bind("<Button-1>", lambda e: set_prompt("enter a prompt"))

prompt2 = tk.Label(center_frame, text="Enter another prompt", fg="black", cursor="hand2", bg="white", padx=10, pady=5)
prompt2.pack(pady=5)
prompt2.bind("<Button-1>", lambda e: set_prompt("enter another prompt"))

# Start the main event loop
root.mainloop()