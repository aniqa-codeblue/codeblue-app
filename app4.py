import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import requests
import json
from PIL import Image, ImageTk  # For handling images

# AI API Endpoint (Replace with actual API URL)
API_URL = "http://127.0.0.1:5000"

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        display_image(file_path)

def display_image(file_path):
    global img_tk  # Keep image reference global
    image_path.set(file_path)

    # Open and resize image to 150x150
    img = Image.open(file_path)
    img = img.resize((150, 150), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    # Update label with image
    image_label.config(image=img_tk, borderwidth=2, relief="solid")  # Add border
    image_label.image = img_tk  # Keep reference
    image_label.grid(row=1, column=0, pady=10)  # Below upload button

    # Show "Remove" button below the image
    remove_button.grid(row=3, column=0, pady=10)

    # Adjust window dynamically
    root.update_idletasks()

def remove_image():
    image_label.config(image="", borderwidth=0)  # Remove image and border
    image_label.image = None  # Remove reference
    image_path.set("")  # Clear image path
    remove_button.grid_forget()  # Hide "Remove" button

def generate_prompt(options):
    prompt = "You are an expert UI/UX developer. Create an HTML and CSS-based design following best practices. Ensure clean, semantic, and responsive code."

    if options["responsive"]:
        prompt += " The design should be fully responsive using modern CSS techniques like media queries."
    if options["form_validation"]:
        prompt += " Implement proper form validation using JavaScript and HTML5 validation attributes."
    if options["use_flex_grid"]:
        prompt += " Use Flexbox and Grid where necessary to enhance layout structure."
    if options["animations"]:
        prompt += " Include smooth animations and transitions for a better user experience."
    if options["seo_optimization"]:
        prompt += " Ensure the code is optimized for SEO with proper meta tags and semantic HTML."

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
root.geometry("800x750")  # Adjusted height
root.configure(bg="white")

# Center Frame
centerframe = tk.Frame(root, bg="white")
centerframe.grid(row=0, column=0, pady=10, padx=110)

# Checkbox Frame
checkframe = tk.Frame(root, bg="white")
checkframe.grid(row=1, column=0, pady=10, padx=110)

# Generate Button Frame
generatebtnframe = tk.Frame(root, bg="white")
generatebtnframe.grid(row=2, column=0, pady=10, padx=150)

# Create and place the title label
title_label = tk.Label(centerframe, text="Upload Image to Generate Code For", font=("Arial", 14, "bold"), bg="white", fg="black")
title_label.grid(row=0, column=0, pady=15, padx=110)

# Image path storage
image_path = tk.StringVar()

# Upload button
upload_button = tk.Button(centerframe, text="Upload Image", command=upload_image, bg="black", fg="white", font=("Arial", 11))
upload_button.grid(row=1, column=0, pady=10, padx=150)

# Image label (Displays uploaded image)
image_label = tk.Label(centerframe, bg="white")
image_label.grid(row=2, column=0, pady=10, padx=110)  # Below upload button

# Remove button (Initially hidden)
remove_button = tk.Button(centerframe, text="Remove", command=remove_image, bg="black", fg="white", font=("Arial", 11))
remove_button.grid_forget()  # Initially hidden

# Checkbox options
responsive_var = tk.BooleanVar()
validation_var = tk.BooleanVar()
flex_grid_var = tk.BooleanVar()
animation_var = tk.BooleanVar()
seo_var = tk.BooleanVar()

tk.Checkbutton(checkframe, text="Make it Responsive", bg="white", fg="black", font=("Arial", 11), variable=responsive_var).pack()
tk.Checkbutton(checkframe, text="Add Form Validation", bg="white", fg="black", font=("Arial", 11), variable=validation_var).pack()
tk.Checkbutton(checkframe, text="Use Flex/Grid", bg="white", fg="black", font=("Arial", 11), variable=flex_grid_var).pack()
tk.Checkbutton(checkframe, text="Include Animations", bg="white", fg="black", font=("Arial", 11), variable=animation_var).pack()
tk.Checkbutton(checkframe, text="Optimize for SEO", bg="white", fg="black", font=("Arial", 11), variable=seo_var).pack()

# Submit button
tk.Button(generatebtnframe, text="Generate Code", command=submit_data, bg="rosybrown1", fg="black", font=("Arial", 11)).pack(pady=20)

root.mainloop()