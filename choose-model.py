import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from pathlib import Path
import webbrowser
import random
import string
import threading
import google.generativeai as genai

class CodeBlue(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window configuration
        self.title("Code Blue")
        self.geometry("1000x600")
        self.minsize(1000, 600)

        # Initialize variables
        self.image_path = tk.StringVar()
        self.img_tk = None

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create main frames with dark theme colors
        self.left_panel = ctk.CTkFrame(
            self, 
            width=400, 
            corner_radius=10,
            fg_color=("#333333", "#1E1E1E")
        )
        self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.left_panel.grid_propagate(False)

        self.right_panel = ctk.CTkFrame(
            self, 
            corner_radius=10,
            fg_color=("#333333", "#1E1E1E")
        )
        self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Initialize panels
        self.create_left_panel()
        self.create_right_panel()

        # Initialize Gemini AI
        genai.configure(api_key='AIzaSyAl5tKWcYUXk7UIN82cDbj7KNJMqTDrgKM')

    def create_left_panel(self):
        # Configure grid
        self.left_panel.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkLabel(
            self.left_panel,
            text="Image Upload & Customization",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            pady=10
        )
        header.grid(row=0, column=0, padx=10, sticky="ew")

        model_dropdown = ctk.CTkComboBox(
            self.left_panel,
            values=["open-ai", "ollama", "anthoropic", "gemini"],  # Add your model options here
            font=ctk.CTkFont(size=14),
            width=150  # Adjust width as needed
        )
        model_dropdown.grid(row=0, column=1, padx=10, sticky="w")
        
        # Prompt section
        prompt_label = ctk.CTkLabel(
            self.left_panel,
            text="Prompt for the Design",
            font=ctk.CTkFont(size=14),
            text_color=("#E0E0E0", "#E0E0E0")
        )
        prompt_label.grid(row=1, column=0, padx=10, pady=(20, 5), sticky="w")

        self.prompt_input = ctk.CTkTextbox(
            self.left_panel,
            height=60,
            font=ctk.CTkFont(size=13),
            fg_color=("#2B2B2B", "#2B2B2B"),
            text_color=("#FFFFFF", "#FFFFFF"),
            border_color=("#555555", "#555555")
        )
        self.prompt_input.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ew")


        # Upload button
        self.upload_button = ctk.CTkButton(
            self.left_panel,
            text="Upload Image",
            command=self.upload_image,
            height=35,
            fg_color="#0066FF",
            hover_color="#0052CC"
        )
        self.upload_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Remove button (initially hidden)
        self.remove_button = ctk.CTkButton(
            self.left_panel,
            text="Remove Image",
            command=self.remove_image,
            height=35,
            fg_color="#2B2B2B",
            hover_color="#3B3B3B"
        )

        # Progress bar and label
        self.progress_label = ctk.CTkLabel(
            self.left_panel,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=("#E0E0E0", "#E0E0E0")
        )
        self.progress_label.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(
            self.left_panel,
            mode="indeterminate",
            height=5
        )

        # Individual checkboxes
        self.checkbox1 = ctk.CTkCheckBox(
            self.left_panel,
            text="Make it Responsive",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox1.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.checkbox2 = ctk.CTkCheckBox(
            self.left_panel,
            text="Add Form Validation",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox2.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.checkbox3 = ctk.CTkCheckBox(
            self.left_panel,
            text="Use Flex Layout",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox3.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.checkbox4 = ctk.CTkCheckBox(
            self.left_panel,
            text="Use Grid Layout",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox4.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        self.checkbox5 = ctk.CTkCheckBox(
            self.left_panel,
            text="Include Animations/Icons",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox5.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        self.checkbox6 = ctk.CTkCheckBox(
            self.left_panel,
            text="Color Transitions",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox6.grid(row=12, column=0, padx=10, pady=5, sticky="w")

        # Generate button
        self.generate_button = ctk.CTkButton(
            self.left_panel,
            text="Generate Code",
            command=self.generate_code,
            font=ctk.CTkFont(size=15, weight="bold"),
            height=40,
            fg_color="#0066FF",
            hover_color="#0052CC"
        )
        self.generate_button.grid(row=13, column=0, padx=10, pady=20, sticky="ew")

        # Image display label
        self.image_label = ctk.CTkLabel(
            self.left_panel,
            text="No image selected",
            font=ctk.CTkFont(size=13),
            text_color=("#E0E0E0", "#E0E0E0")
        )
        self.image_label.grid(row=14, column=0, padx=10, pady=5, sticky="ew")
    def create_right_panel(self):
        # Configure grid
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkLabel(
            self.right_panel,
            text="Code Preview",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            pady=10
        )
        header.grid(row=0, column=0, padx=10, sticky="ew")

        # Code preview area
        self.code_preview = ctk.CTkTextbox(
            self.right_panel,
            font=ctk.CTkFont(family="Courier", size=13),
            wrap="none",
            fg_color=("#2B2B2B", "#2B2B2B"),
            text_color=("#FFFFFF", "#FFFFFF"),
            border_color=("#555555", "#555555")
        )
        self.code_preview.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # Button frame
        button_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color="transparent"
        )
        button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        # Copy and Save buttons
        self.copy_button = ctk.CTkButton(
            button_frame,
            text="Copy Code",
            command=self.copy_code,
            width=120,
            height=32,
            fg_color=("#2B2B2B", "#2B2B2B"),
            hover_color=("#3B3B3B", "#3B3B3B"),
            border_width=1,
            border_color=("#555555", "#555555")
        )
        self.copy_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save & Open",
            command=self.save_and_open_html,
            width=120,
            height=32,
            fg_color=("#2B2B2B", "#2B2B2B"),
            hover_color=("#3B3B3B", "#3B3B3B"),
            border_width=1,
            border_color=("#555555", "#555555")
        )
        self.save_button.pack(side="left", padx=5)

    def generate_prompt(self):
        options = {
            "responsive": self.checkbox1.get(),
            "form_validation": self.checkbox2.get(),
            "use_flex_structure": self.checkbox3.get(),
            "use_grid_structure": self.checkbox4.get(),
            "animations": self.checkbox5.get(),
            "color_Transitions": self.checkbox6.get(),
            "custom_input": self.prompt_input.get("1.0", tk.END).strip()
        }

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
            prompt += " " + options["custom_input"]

        return prompt

    def generate_code(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please upload an image first!")
            return

        self.progress_label.configure(text="Generating code... Please wait")
        self.progress_bar.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.progress_bar.start()

        threading.Thread(target=self.generate_code_thread, daemon=True).start()

    def generate_code_thread(self):
        """Thread for generating code using selected AI model"""
        try:
            image = Image.open(self.image_path.get())
            prompt = self.generate_prompt()
            selected_model = self.model_dropdown.get().lower()
            result = ""

            if selected_model == "ollama":
                # First get visualization prompt from Gemini
                gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                vision_prompt = "Analyze this image and describe its layout, components, and visual structure in detail. Include information about positioning, styling, and interactive elements."
                vision_response = gemini_model.generate_content([vision_prompt, image])
                
                # Use the vision response to generate code with Ollama
                self.enchanced_prompt = f"Based on this visual description: {vision_response.text}\n\n{prompt}"
                # TODO: Implement Ollama API call
                result = "// Ollama integration pending\n// Using this model requires Ollama API implementation"

            elif selected_model == "anthropic":
                # TODO: Implement Anthropic Claude API call
                result = "// Anthropic integration pending\n// Using this model requires Claude API implementation"

            elif selected_model == "gemini":
                model = genai.GenerativeModel('gemini-2.0-flash')
            
                if self.image_path.get():
                    response = model.generate_content([self.prompt, image])
                else:
                    response = model.generate_content(self.prompt)
                
                result = response.text

            else:  # Default to Gemini
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content([prompt, image])
                result = response.text

            self.after(0, self.update_code_preview, result)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to generate code: {str(e)}"))
        finally:
            self.after(0, self.stop_progress)



    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.image_path.set(file_path)
            self.display_image(file_path)

    def display_image(self, file_path):
        try:
            image = Image.open(file_path)
            image = image.resize((150, 130))
            self.img_tk = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.img_tk, text="")
            self.remove_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def remove_image(self):
        self.image_label.configure(image="", text="No image selected")
        self.img_tk = None
        self.image_path.set("")
        self.remove_button.grid_forget()

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.grid_forget()
        self.progress_label.configure(text="")

    def update_code_preview(self, code):
        self.code_preview.delete("1.0", "end")
        self.code_preview.insert("1.0", code)

    def copy_code(self):
        code = self.code_preview.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(code)
        messagebox.showinfo("Success", "Code copied to clipboard!")

    def save_and_open_html(self):
        code = self.code_preview.get("1.0", "end-1c")
        if not code.strip():
            messagebox.showwarning("Warning", "No code to save!")
            return

        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        filename = f"generated_html_{random_string}.html"
        
        downloads_folder = str(Path.home() / "Downloads")
        file_path = os.path.join(downloads_folder, filename)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            webbrowser.open('file://' + os.path.realpath(file_path))
            messagebox.showinfo("Success", f"HTML file created and opened in browser.\nSaved in: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

if __name__ == "__main__":
    app = CodeBlue()
    app.mainloop()