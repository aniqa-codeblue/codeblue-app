import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
from PIL import Image, ImageTk
import google.generativeai as genai
import os

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
    img = img.resize((150, 130), Image.LANCZOS)
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
    prompt = "Generate HTML and CSS code with as much accuracy as possible."

    if options["responsive"]:
        prompt += " The design should be fully responsive using modern CSS."
    if options["form_validation"]:
        prompt += " Add form validation functionality using JavaScript and HTML5 validation attributes."
    if options["use_flex_grid"]:
        prompt += " Use Flexbox or Grid where necessary to enhance layout structure."
    if options["animations"]:
        prompt += " Include smooth animations and transitions for a better user experience."
    if options["color_Transitions"]:
        prompt += " Add same color transitions for buttons and other elements as shown in image when hovered."

    return prompt

def submit_data():
    if not image_path.get():
        messagebox.showerror("Error", "Please upload an image first!")
        return

    options = {
        "responsive": responsive_var.get(),
        "form_validation": validation_var.get(),
        "use_flex_grid": flex_grid_var.get(),
        "animations": animation_var.get(),
        "color_Transitions": trans_var.get()
    }

    prompt = generate_prompt(options)
    
    try:
        image = Image.open(image_path.get())
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([prompt, image])
        
        result = response.text
        display_response(result)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

def display_response(response):
    response_window = tk.Toplevel(root)
    response_window.title("Generated Code")
    response_window.geometry("800x700")

    text_area = scrolledtext.ScrolledText(response_window, wrap=tk.WORD, width=90, height=30)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, response)
    text_area.config(state=tk.DISABLED)

# Initialize Tkinter app
root = tk.Tk()
root.title("AI-Powered HTML & CSS Generator (Gemini)")
root.geometry("750x600")
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
upload_button = tk.Button(centerframe, text="Upload Image", command=upload_image, bg="black", fg="white", font=("Arial", 11))
upload_button.grid(row=1, column=0, pady=10, padx=150)

# Image label (Displays uploaded image)
image_label = tk.Label(centerframe, bg="white")
image_label.grid(row=2, column=0, pady=10, padx=100)

# Remove button (Initially hidden)
remove_button = tk.Button(centerframe, text="Remove", command=remove_image, bg="black", fg="white", font=("Arial", 11))
remove_button.grid_forget()

# Checkbox options
responsive_var = tk.BooleanVar()
validation_var = tk.BooleanVar()
flex_grid_var = tk.BooleanVar()
animation_var = tk.BooleanVar()
trans_var = tk.BooleanVar()

tk.Checkbutton(checkframe, text="Make it Responsive", bg="white", fg="black", font=("Arial", 11), variable=responsive_var).pack()
tk.Checkbutton(checkframe, text="Add Form Validation", bg="white", fg="black", font=("Arial", 11), variable=validation_var).pack()
tk.Checkbutton(checkframe, text="Use Flex/Grid", bg="white", fg="black", font=("Arial", 11), variable=flex_grid_var).pack()
tk.Checkbutton(checkframe, text="Include Animations", bg="white", fg="black", font=("Arial", 11), variable=animation_var).pack()
tk.Checkbutton(checkframe, text="Color Transitions for Elements", bg="white", fg="black", font=("Arial", 11), variable=trans_var).pack()

# Submit button
tk.Button(generatebtnframe, text="Generate Code", command=submit_data, bg="rosybrown1", fg="black", font=("Arial", 11)).pack(pady=20)

root.mainloop()