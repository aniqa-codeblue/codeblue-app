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
    prompt = "Generate HTML and CSS code with as much accuracy as possible. Do not make separate files for the HTML, CSS and Javascript code."

    if options["responsive"]:
        prompt += " The design should be fully responsive using modern CSS. The number of all elements and buttons should be same as in the image."
    if options["form_validation"]:
        prompt += " Add form validation functionality using JavaScript and HTML5 validation attributes."
    if options["use_flex_structure"]:
        prompt += " Use Flexbox if necessary to match the image layout accurately."
    if options["use_grid_structure"]:
        prompt += " Use grid layout if necessary to match the image layout accurately."
    if options["animations"]:
        prompt += " Include smooth transitions/animations/icons (if any) just like in the image. The number of icons should be same as in the image."
    if options["color_Transitions"]:
        prompt += " Add same color transitions for buttons and other elements as shown in image when hovered. Keep text size for elements same as in the image as much as possible."
    if options["custom_input"]:
        prompt += " " + custom_input_entry.get("1.0", tk.END)

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
        display_response(result)
        centerframe.after(0, stop_progress)
    except Exception as e:
        centerframe.after(0, stop_progress)
        messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

def stop_progress():
    progress_bar.stop()  # Stop progress animation
    progress_bar.grid_forget()  # Hide progress bar
    progress_label.config(text="")  # Remove status message

def save_file():
    # Extract HTML content from the full response
    html_content = response_text.get("1.0", tk.END)
    html_start = html_content.find("<!DOCTYPE html>")
    html_end = html_content.rfind("</html>") + 7  # Include the closing tag
    if html_start != -1 and html_end != -1:
        html_content = html_content[html_start:html_end]
    else:
        messagebox.showwarning("Warning", "Could not find valid HTML content in the response.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        messagebox.showinfo("File Saved", f"HTML file saved successfully.\nFile path: {file_path}")
    
    preview_code.file_path = file_path #giving path to file

def preview_code():
    if hasattr(preview_code, 'file_path'):
        webbrowser.open('file://' + os.path.realpath(preview_code.file_path))
    else:
        messagebox.showerror("Save File", f"No html file generated yet. Please save the code first.")

def copy_code():
    content = response_text.get("1.0", tk.END)
    html_start = content.find("<!DOCTYPE html>")
    html_end = content.rfind("</html>") + 7  # Include the closing tag
    if html_start != -1 and html_end != -1:
        html_content = content[html_start:html_end]
    else:
        messagebox.showwarning("Warning", "Could not find valid HTML content in the response.")
        return
    root.clipboard_clear()
    root.clipboard_append(html_content)
    messagebox.showinfo("Copied","Content copied to clipboard!")

def display_response(response):
    response_text.config(state=tk.NORMAL)
    response_text.delete(1.0, tk.END)
    response_text.insert(tk.END, response)
    response_text.config(state=tk.DISABLED)

def toggle_custom_input():
    if custom_input.get():
        custom_input_entry.grid(row=7, column=0, pady=5, padx=5, sticky="ew")
    else:
        custom_input_entry.grid_forget()

# Initialize Tkinter app
root = tk.Tk()
root.title("AI-Powered HTML & CSS Generator (Gemini)")
root.geometry("1230x850")
root.configure(bg="white")

# Main Frame
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill=tk.BOTH, expand=True)

# Left Frame (40% width)
left_frame = tk.Frame(main_frame, bg="white", width=450)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Right Frame (60% width)
right_frame = tk.Frame(main_frame, bg="white", width=750)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Center Frame (inside Left Frame)
centerframe = tk.Frame(left_frame, bg="white")
centerframe.pack(pady=15, padx=10)

# Checkbox Frame (inside Left Frame)
checkframe = tk.Frame(left_frame, bg="white")
checkframe.pack(pady=10, padx=10)

# Entry Frame (inside Left Frame)
entryframe = tk.Frame(left_frame, bg="white")
entryframe.pack(pady=10, padx=10)

# Generate Button Frame (inside Left Frame)
generatebtnframe = tk.Frame(left_frame, bg="white")
generatebtnframe.pack(pady=10, padx=10)

# Create and place the title label
title_label = tk.Label(centerframe, text="Upload Image to Generate Code For", font=("Arial", 14, "bold"), bg="white", fg="black")
title_label.grid(row=0, column=0, pady=10, padx=100)

# Image path storage
image_path = tk.StringVar()

# Upload button
upload_button = tk.Button(centerframe, text="Upload Image", command=upload_image, bg="black", fg="white", font=("Arial", 12))
upload_button.grid(row=1, column=0, pady=14, padx=150)

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

tk.Checkbutton(checkframe, text="Make it Responsive", bg="white", fg="black", font=("Arial", 12), variable=responsive_var).pack(anchor="w")
tk.Checkbutton(checkframe, text="Add Form Validation", bg="white", fg="black", font=("Arial", 12), variable=validation_var).pack(anchor="w")
tk.Checkbutton(checkframe, text="Use Flex Layout", bg="white", fg="black", font=("Arial", 12), variable=flex_var).pack(anchor="w")
tk.Checkbutton(checkframe, text="Use Grid Layout", bg="white", fg="black", font=("Arial", 12), variable=grid_var).pack(anchor="w")
tk.Checkbutton(checkframe, text="Include Animations/Icons", bg="white", fg="black", font=("Arial", 12), variable=animation_var).pack(anchor="w")
tk.Checkbutton(checkframe, text="Color Transitions for Elements", bg="white", fg="black", font=("Arial", 12), variable=trans_var).pack(anchor="w")
tk.Checkbutton(checkframe, text="Enter Custom Prompt for AI", bg="white", fg="black", font=("Arial", 12), variable=custom_input, command=toggle_custom_input).pack(anchor="w")

# Custom input entry
custom_input_entry = tk.Text(entryframe, width=50, height=3, font=("Arial", 13), padx=10, pady=10)

# Submit button
tk.Button(generatebtnframe, text="Generate Code", command=submit_data, bg="rosybrown1", fg="black", font=("Arial", 13)).pack(pady=20)

# Right Frame Layout
right_frame_inner = tk.Frame(right_frame, bg="white")
right_frame_inner.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Button Frame (for Save File and Copy buttons)
button_frame = tk.Frame(right_frame, bg="white")
button_frame.pack(fill=tk.X, pady=(5, 5))

# Save File Button
save_button = tk.Button(button_frame, text="Save File", command=save_file, bg="black", fg="white", font=("Arial", 12))
save_button.pack(side=tk.RIGHT, padx=(5, 8))

# Copy Button
copy_button = tk.Button(button_frame, text="Copy", command=copy_code, bg="antiquewhite2", fg="black", font=("Arial", 12))
copy_button.pack(side=tk.RIGHT)

# Code Preview Title (inside the text area boundary)
right_title = tk.Label(right_frame_inner, text="Code Preview", font=("Arial", 14, "bold"), bg="white", fg="black")
#right_title.pack(pady=(0, 5))
right_title.pack(anchor="sw", pady=(16, 0))

# Response Text (in Right Frame)
response_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=150, height=38)
response_text.pack(padx=12, pady=5, fill=tk.BOTH, expand=True)
response_text.config(state=tk.DISABLED)

preview_button = tk.Button(right_frame, text="Preview", command=preview_code, bg="green", fg="white", font=("Arial", 12))
preview_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=15)

root.mainloop()
