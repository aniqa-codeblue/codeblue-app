import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import requests
import json
import os

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image_path.set(file_path)

def generate_prompt(options):
    prompt = "You are an expert UI/UX developer. Create an HTML and CSS-based design following best practices."

    if options["responsive"]:
        prompt += " The design should be fully responsive using modern CSS techniques."
    if options["form_validation"]:
        prompt += " Implement proper form validation."
    if options["use_flex_grid"]:
        prompt += " Use Flexbox and Grid to enhance the layout."
    if options["animations"]:
        prompt += " Include smooth animations."
    if options["seo_optimization"]:
        prompt += " Optimize for SEO using proper meta tags and semantic HTML."

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
        "seo_optimization": seo_var.get()
    }

    prompt = generate_prompt(options)

    # Prepare file and data payload
    files = {'image': open(image_path.get(), 'rb')}
    data = {'options': json.dumps(options), 'prompt': prompt}

    try:
        response = requests.post("http://127.0.0.1:5000/generate", files=files, data=data)
        result = response.json()

        if "html" in result and "css" in result:
            show_generated_code(result["html"], result["css"])
        else:
            messagebox.showerror("Error", "Invalid response from AI API")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

def submit_data():
    if not image_path.get():
        messagebox.showerror("Error", "Please upload an image first!")
        return

    options = {
        "responsive": responsive_var.get(),
        "form_validation": validation_var.get(),
        "use_flex_grid": flex_grid_var.get(),
        "animations": animation_var.get(),
        "seo_optimization": seo_var.get()
    }

    prompt = generate_prompt(options)

    # Prepare file and data payload
    files = {'image': open(image_path.get(), 'rb')}  # Open image file
    data = {'options': json.dumps(options), 'prompt': prompt}

    try:
        response = requests.post("http://127.0.0.1:5000/generate", files=files, data=data)  # Local Flask API
        result = response.json()

        if "html" in result and "css" in result:
            with open("output.html", "w") as html_file:
                html_file.write(result["html"])
            with open("styles.css", "w") as css_file:
                css_file.write(result["css"])
            messagebox.showinfo("Success", "HTML & CSS files generated successfully!")
        else:
            messagebox.showerror("Error", "Invalid response from AI API")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

# Initialize Tkinter app
root = tk.Tk()
root.title("AI-Powered HTML & CSS Generator")
root.geometry("600x400")

# Image path storage
image_path = tk.StringVar()

# Upload button
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# Options
responsive_var = tk.BooleanVar()
validation_var = tk.BooleanVar()
flex_grid_var = tk.BooleanVar()
animation_var = tk.BooleanVar()
seo_var = tk.BooleanVar()

tk.Checkbutton(root, text="Responsive Design", variable=responsive_var).pack()
tk.Checkbutton(root, text="Form Validation", variable=validation_var).pack()
tk.Checkbutton(root, text="Use Flex/Grid", variable=flex_grid_var).pack()
tk.Checkbutton(root, text="Include Animations", variable=animation_var).pack()
tk.Checkbutton(root, text="SEO Optimization", variable=seo_var).pack()

# Generate button
generate_button = tk.Button(root, text="Generate Code", command=submit_data, bg="green", fg="white")
generate_button.pack(pady=10)

root.mainloop()