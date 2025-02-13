import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk  # Import PIL for image processing

def upload_file():
    file_path = filedialog.askopenfilename(title="Select a file", 
                                           filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), 
                                                      ("All files", "*.*")])
    if file_path:
        display_image(file_path)

def display_image(file_path):
    # Open the image and resize it
    img = Image.open(file_path)
    img.thumbnail((300, 300))  # Resize to fit within 300x300

    # Convert to Tkinter-compatible format
    img_tk = ImageTk.PhotoImage(img)

    # Update the label with the image
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection
    image_label.pack(pady=20)

def on_drop(event):
    file_path = event.data.strip('{}')  # Remove surrounding {} if present
    display_image(file_path)

def submit():
    prompt = input_field.get()
    print(f"Submitted prompt: {prompt}")

def set_prompt(prompt):
    input_field.delete(0, tk.END)
    input_field.insert(0, prompt)

def on_drop(event):
    file_path = event.data.strip('{}')  # Remove surrounding {} if present
    display_image(file_path)

# Create the main window
root = TkinterDnD.Tk()
root.title("Image Upload App")
root.geometry("800x600")
root.configure(bg="white")

# Create a frame to center all contents
center_frame = tk.Frame(root, bg="white")
center_frame.place(relx=0.5, rely=0.4, anchor="center")

# Create and place the title label
title_label = tk.Label(center_frame, text="Upload Your Image", font=("Arial", 20, "bold"), bg="white", fg="black")
title_label.pack(pady=20)

# Create a label to display images
image_label = tk.Label(center_frame, bg="white")
image_label.pack(pady=20)

# Create and place the upload button
upload_button = tk.Button(center_frame, text="Browse from PC", command=upload_file, bg="black", fg="white", font=("Arial", 11))
upload_button.pack(pady=14)

# Enable drag and drop for images
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Create and place the submit button
submit_button = tk.Button(center_frame, text="Submit", command=submit, bg="pink", fg="black", font=("Arial", 11))
submit_button.pack(pady=14)

# Create and place clickable text prompts
prompt1 = tk.Label(center_frame, text="Enter a prompt", fg="black", cursor="hand2", bg="white", padx=10, pady=5)
prompt1.pack(pady=5)
prompt1.bind("<Button-1>", lambda e: set_prompt("enter a prompt"))

prompt2 = tk.Label(center_frame, text="Enter another prompt", fg="black", cursor="hand2", bg="white", padx=10, pady=5)
prompt2.pack(pady=5)
prompt2.bind("<Button-1>", lambda e: set_prompt("enter another prompt"))

# Start the main event loop
root.mainloop()