import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import webbrowser
import os
import google.generativeai as genai
import requests
import json
import base64
import cohere

# Initialize AI services (you'll need to set these up)
genai.configure(api_key='AIzaSyAl5tKWcYUXk7UIN82cDbj7KNJMqTDrgKM')
COHERE_API_KEY = '5Bm3dFUEVTHbfyosOGlOzTQ6zrsbekUv2n8kMxqd'
# Add other API keys as needed

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

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

    image_label.configure(image=img_tk)
    image_label.image = img_tk
    image_label.grid(row=4, column=0, pady=5)

    remove_button.grid(row=5, column=0, pady=5)

    root.update_idletasks()

def remove_image():
    image_label.configure(image="")
    image_label.image = None
    image_path.set("")
    remove_button.grid_forget()

def generate_prompt(options, design_details):
    prompt = f" {design_details}"

    if options["responsive"]:
        prompt += " Generate HTML and CSS code with as much accuracy as possible. Do not make separate files for the HTML, CSS and Javascript code. The design should be fully responsive using modern CSS. The number of all elements and buttons should be same as in the image."
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

    return prompt

def submit_data():
    design_details = design_input.get("1.0", "end-1c").strip()
    has_image = bool(image_path.get())
    
    options = {
        "responsive": responsive_var.get(),
        "form_validation": validation_var.get(),
        "use_flex_structure": flex_var.get(),
        "use_grid_structure": grid_var.get(),
        "animations": animation_var.get(),
        "color_Transitions": trans_var.get(),
    }
    
    any_checkbox_selected = any(options.values())

    if not design_details and not has_image and not any_checkbox_selected:
        messagebox.showerror("Error", "Please enter design details, upload an image, or select at least one option!")
        return

    prompt = generate_prompt(options, design_details)

    progress_label.configure(text="Generating code... Please Wait")
    progress_bar.grid(row=7, column=0, pady=5)
    progress_bar.start()

    generate_button.configure(state="disabled", text="Generating code...")

    threading.Thread(target=generate_code, args=(prompt,), daemon=True).start()

def generate_code(prompt):
    try:
        selected_model = model_var.get()
        
        if selected_model == "Gemini":
            result = generate_with_gemini(prompt)
        elif selected_model == "Cohere":
            result = generate_with_cohere(prompt)
        # Add other model handlers here
        
        root.after(0, lambda: display_response(result))
        root.after(0, stop_progress)
    except Exception as e:
        root.after(0, stop_progress)
        root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate code: {str(e)}"))

def generate_with_gemini(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    if image_path.get():
        image = Image.open(image_path.get())
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    
    return response.text

def generate_with_cohere(prompt):
    if image_path.get():
        # First, use Gemini to describe the image
        image_description = get_image_description_from_gemini()
        prompt = f"{image_description}\n\n{prompt}"
    
    # Now, use Cohere to generate the code
    
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "command-r7b-12-2024",
        "prompt": prompt,
        "max_tokens": 10000000,
        "temperature": 0.7,
        "k": 0,
        "stop_sequences": [],
        "return_likelihoods": "NONE"
    }
    response = cohere.chat(cohere.ClientV2(COHERE_API_KEY), headers=headers, json=data)
    response_json = response.json()
    return response_json['generations'][0]['text']

def get_image_description_from_gemini():
    model = genai.GenerativeModel('gemini-2.0-flash')
    image = Image.open(image_path.get())
    prompt = "Give a detailed description of all elements, layouts, forms, buttons, text inputs, icons used, colors used for buttons, forms, input fields and width of all forms inside the image in text that can be used to generate html css and javascript code just like that in the image"
    response = model.generate_content([prompt, image])
    return response.text

def stop_progress():
    progress_bar.stop()
    progress_bar.grid_forget()
    progress_label.configure(text="")
    generate_button.configure(state="normal", text="Generate Code")

def save_file():
    content = response_text.get("1.0", ctk.END)
    html_start = content.find("<!DOCTYPE html>")
    html_end = content.rfind("</html>") + 7
    if html_start != -1 and html_end != -1:
        html_content = content[html_start:html_end]
    else:
        messagebox.showwarning("Warning", "Could not find valid HTML content in the response.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        messagebox.showinfo("File Saved", f"HTML file saved successfully.\nFile path: {file_path}")
        preview_html.file_path = file_path

def copy_code():
    content = response_text.get("1.0", ctk.END)
    root.clipboard_clear()
    root.clipboard_append(content)
    messagebox.showinfo("Copied", "Code copied to clipboard!")

def preview_html():
    if hasattr(preview_html, 'file_path'):
        webbrowser.open('file://' + os.path.realpath(preview_html.file_path))
    else:
        messagebox.showinfo("Info", "No HTML file saved yet. Please save the file first.")

def display_response(response):
    response_text.configure(state="normal")
    response_text.delete("1.0", ctk.END)
    response_text.insert(ctk.END, response)
    response_text.configure(state="disabled")

# Initialize CustomTkinter app
root = ctk.CTk()
root.title("AI-Powered HTML & CSS Generator")
root.geometry("1200x800")

# Main Frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill=ctk.BOTH, expand=True)

# Left Frame (40% width)
left_frame = ctk.CTkFrame(main_frame, width=480)
left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

# Right Frame (60% width)
right_frame = ctk.CTkFrame(main_frame, width=720)
right_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

# Center Frame (inside Left Frame)
centerframe = ctk.CTkFrame(left_frame)
centerframe.pack(pady=10, padx=20, fill=ctk.BOTH, expand=True)

# Create and place the title label
title_label = ctk.CTkLabel(centerframe, text="Enter Your Design Details", font=("Arial", 14, "bold"))
title_label.grid(row=0, column=0, pady=5, sticky="w")

# Model selection dropdown
model_var = ctk.StringVar(value="Gemini")
model_dropdown = ctk.CTkOptionMenu(centerframe, variable=model_var, values=["Gemini", "Cohere", "OpenAI", "Anthropic", "Meta"])
model_dropdown.grid(row=0, column=1, pady=5, padx=10, sticky="e")

# Design input field
design_input = ctk.CTkTextbox(centerframe, width=400, height=100)
design_input.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
design_input.insert("1.0", "Enter details or upload image")
design_input.bind("<FocusIn>", lambda args: design_input.delete("1.0", "end"))

# Image path storage
image_path = ctk.StringVar()

# Upload button
upload_button = ctk.CTkButton(centerframe, text="Upload Image", command=upload_image)
upload_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")

# Image label (Displays uploaded image)
image_label = ctk.CTkLabel(centerframe, text="")
image_label.grid(row=4, column=0, columnspan=2, pady=5)

# Remove button (Initially hidden)
remove_button = ctk.CTkButton(centerframe, text="Remove", command=remove_image)
remove_button.grid_forget()

progress_label = ctk.CTkLabel(centerframe, text="")
progress_label.grid(row=6, column=0, columnspan=2, pady=5)

progress_bar = ctk.CTkProgressBar(centerframe, orientation="horizontal", mode="indeterminate")

# Checkbox options
responsive_var = ctk.BooleanVar()
validation_var = ctk.BooleanVar()
flex_var = ctk.BooleanVar()
grid_var = ctk.BooleanVar()
animation_var = ctk.BooleanVar()
trans_var = ctk.BooleanVar()

ctk.CTkCheckBox(centerframe, text="Make it Responsive", variable=responsive_var).grid(row=8, column=0, columnspan=2, sticky="w", pady=2)
ctk.CTkCheckBox(centerframe, text="Add Form Validation", variable=validation_var).grid(row=9, column=0, columnspan=2, sticky="w", pady=2)
ctk.CTkCheckBox(centerframe, text="Use Flex Layout", variable=flex_var).grid(row=10, column=0, columnspan=2, sticky="w", pady=2)
ctk.CTkCheckBox(centerframe, text="Use Grid Layout", variable=grid_var).grid(row=11, column=0, columnspan=2, sticky="w", pady=2)
ctk.CTkCheckBox(centerframe, text="Include Animations/Icons", variable=animation_var).grid(row=12, column=0, columnspan=2, sticky="w", pady=2)
ctk.CTkCheckBox(centerframe, text="Color Transitions for Elements", variable=trans_var).grid(row=13, column=0, columnspan=2, sticky="w", pady=2)

# Generate button
generate_button = ctk.CTkButton(centerframe, text="Generate Code", command=submit_data)
generate_button.grid(row=14, column=0, columnspan=2, pady=10, sticky="ew")

# Right Frame Layout
right_frame_inner = ctk.CTkFrame(right_frame)
right_frame_inner.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

# Button Frame (for Save File and Copy buttons)
button_frame = ctk.CTkFrame(right_frame_inner)
button_frame.pack(fill=ctk.X, pady=(0, 5))

# Save File Button
save_button = ctk.CTkButton(button_frame, text="Save File", command=save_file)
save_button.pack(side=ctk.RIGHT, padx=(5, 8))

# Copy Button
copy_button = ctk.CTkButton(button_frame, text="Copy", command=copy_code)
copy_button.pack(side=ctk.RIGHT)

# Code Preview Title
right_title = ctk.CTkLabel(right_frame_inner, text="Code Preview", font=("Arial", 14, "bold"))
right_title.pack(pady=(0, 5))

# Response Text (in Right Frame)
response_text = ctk.CTkTextbox(right_frame_inner, wrap="word", width=600, height=500)
response_text.pack(fill=ctk.BOTH, expand=True)
response_text.configure(state="disabled")

# Preview Button
preview_button = ctk.CTkButton(right_frame, text="Preview", command=preview_html)
preview_button.pack(side=ctk.BOTTOM, anchor=ctk.SE, padx=10, pady=10)

root.mainloop()