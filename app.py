import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
from PIL import Image, ImageTk
import google.generativeai as genai
import os
import tempfile
import webbrowser
import random
import string
from pathlib import Path
import threading

# Set your Google API key here
genai.configure(api_key='AIzaSyAl5tKWcYUXk7UIN82cDbj7KNJMqTDrgKM')

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        display_image(file_path)

def display_image(file_path):
    global img_tk
    image_path.set(file_path)

    img = Image.open(file_path)
    img = img.resize((150, 130))
    img_tk = ImageTk.PhotoImage(img)

    image_label.config(image=img_tk, borderwidth=2, relief="solid")
    image_label.image = img_tk
    image_label.grid(row=1, column=0, pady=10)

    remove_button.grid(row=3, column=0, pady=10)

    root.update_idletasks()

def remove_image():
    image_label.config(image="", borderwidth=0)
    image_label.image = None
    image_path.set("")
    remove_button.grid_forget()

def generate_prompt(options):
    prompt = "Generate HTML and CSS code with as much accuracy as possible. Do not make separate files for the HTML, css and Javascript code."

    if options["responsive"]:
        prompt += " The design should be fully responsive using modern CSS. The number of all elements and buttons should be same as in the image."
    if options["form_validation"]:
        prompt += " Add form validation functionality using JavaScript and HTML5 validation attributes."
    if options["use_flex_structure"]:
        prompt += " Use Flexbox if necessary  to match the image layout accurately."
    if options["use_grid_structure"]:
        prompt += " Use grid layout if necessary to match the image layout accurately."
    if options["animations"]:
        prompt += " Include smooth transitions/animations/icons (if any) just like in the image. The number of icons should be same as in the image."
    if options["color_Transitions"]:
        prompt += " Add same color transitions for buttons and other elements as shown in image when hovered. Keep text size for elements same as in the image as much as possible."
    if options["custom_input"]:
        prompt

    return prompt

def submit_data():
    if not image_path.get():
        messagebox.showerror("Error", "Please upload an image first!")
        return

    options = {
        "responsive": responsive_var.get(),
        "form_validation": validation_var.get(),
        "use_flex_structure": flex_var.get(),
        "use_grid_structure": grid_var.get(),
        "animations": animation_var.get(),
        "color_Transitions": trans_var.get(),
        "custom_input": custom_input.get()
    }

    prompt = generate_prompt(options)

    progress_label.config(text="Generating code... Please Wait")
    progress_bar.grid(row=4, column=0, pady=10)
    progress_bar.start(10)

    threading.Thread(target=generate_code, args=(prompt,), daemon=True).start()
    
def generate_code(prompt):
    try:
        image = Image.open(image_path.get())
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([prompt, image])
        
        result = response.text
        save_and_open_html(result)
        centerframe.after(0, stop_progress)
    except Exception as e:
        centerframe.after(0, stop_progress)
        messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

def stop_progress():
    progress_bar.stop()  # Stop progress animation
    progress_bar.grid_forget()  # Hide progress bar
    progress_label.config(text="")  # Remove status message

def save_and_open_html(html_content):
    # Generate a random filename
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    filename = f"generated_html_{random_string}.html"
    
    # Get the path to the Downloads folder
    downloads_folder = str(Path.home() / "Downloads")
    file_path = os.path.join(downloads_folder, filename)
    
    # Save the HTML content to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(file_path))

    # Display the file path in a message box
    messagebox.showinfo("File Created", f"HTML file created and opened in browser. Saved in user's Download's folder.\nFile path: {file_path}")

# Initialize Tkinter app
root = tk.Tk()
root.title("AI-Powered HTML & CSS Generator (Gemini)")
root.geometry("750x700")
root.configure(bg="white")

# Center Frame
centerframe = tk.Frame(root, bg="white")
centerframe.grid(row=0, column=0, pady=15, padx=100)

# Checkbox Frame
checkframe = tk.Frame(root, bg="white")
checkframe.grid(row=1, column=0, pady=10, padx=100)

# Generate Button Frame
generatebtnframe = tk.Frame(root, bg="white")
generatebtnframe.grid(row=2, column=0, pady=10, padx=150)

# Create and place the title label
title_label = tk.Label(centerframe, text="Upload Image to Generate Code For", font=("Arial", 14, "bold"), bg="white", fg="black")
title_label.grid(row=0, column=0, pady=15, padx=100)

# Image path storage
image_path = tk.StringVar()

# Upload button
upload_button = tk.Button(centerframe, text="Upload Image", command=upload_image, bg="black", fg="white", font=("Arial", 12))
upload_button.grid(row=1, column=0, pady=10, padx=150)

# Image label (Displays uploaded image)
image_label = tk.Label(centerframe, bg="white")
image_label.grid(row=2, column=0, pady=10, padx=100)

# Remove button (Initially hidden)
remove_button = tk.Button(centerframe, text="Remove", command=remove_image, bg="White", fg="Black", font=("Arial", 11))
remove_button.grid_forget()

progress_label = tk.Label(centerframe, text="", font=("Arial", 10))
progress_label.grid(row=3, column=0, pady=5)

progress_bar = ttk.Progressbar(centerframe, orient="horizontal", length=250, mode="indeterminate")

# Checkbox options
responsive_var = tk.BooleanVar()
validation_var = tk.BooleanVar()
flex_var = tk.BooleanVar()
grid_var = tk.BooleanVar()
animation_var = tk.BooleanVar()
trans_var = tk.BooleanVar()
custom_input = tk.BooleanVar()

tk.Checkbutton(checkframe, text="Make it Responsive", bg="white", fg="black", font=("Arial", 12), variable=responsive_var).pack()
tk.Checkbutton(checkframe, text="Add Form Validation", bg="white", fg="black", font=("Arial", 12), variable=validation_var).pack()
tk.Checkbutton(checkframe, text="Use Flex Layout", bg="white", fg="black", font=("Arial", 12), variable=flex_var).pack()
tk.Checkbutton(checkframe, text="Use Grid Layout", bg="white", fg="black", font=("Arial", 12), variable=grid_var).pack()
tk.Checkbutton(checkframe, text="Include Animations/Icons", bg="white", fg="black", font=("Arial", 12), variable=animation_var).pack()
tk.Checkbutton(checkframe, text="Color Transitions for Elements", bg="white", fg="black", font=("Arial", 12), variable=trans_var).pack()
tk.Checkbutton(checkframe, text="Enter Custom Prompt for AI", bg="white", fg="black", font=("Arial", 12), variable=custom_input).pack()

# Submit button
tk.Button(generatebtnframe, text="Generate Code", command=submit_data, bg="rosybrown1", fg="black", font=("Arial", 13)).pack(pady=18)

root.mainloop()