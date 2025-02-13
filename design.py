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

class ModernDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.saved_file_path = None

        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window configuration
        self.title("Code Blue")
        self.geometry("1200x600")
        self.minsize(1000, 800)

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

        # Checkbox options
        self.responsive_var = ctk.BooleanVar()
        self.validation_var = ctk.BooleanVar()
        self.flex_var = ctk.BooleanVar()
        self.grid_var = ctk.BooleanVar()
        self.animation_var = ctk.BooleanVar()
        self.trans_var = ctk.BooleanVar()

        # Header
        header = ctk.CTkLabel(
            self.left_panel,
            text="Image Upload & Customization",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            pady=10
        )
        header.grid(row=0, column=0, padx=10, sticky="ew")

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
            height=70,
            font=ctk.CTkFont(size=14),
            fg_color=("#2B2B2B", "#2B2B2B"),
            text_color=("#FFFFFF", "#FFFFFF"),
            border_color=("#555555", "#555555"),
            border_width=1,
            scrollbar_button_hover_color="white"
        )
        self.prompt_input.grid(row=2, column=0, padx=10, pady=(0, 20), sticky="ew")

        
        # Upload button
        self.upload_button = ctk.CTkButton(
            self.left_panel,
            text="Upload Image",
            command=self.upload_image,
            height=35,
            fg_color="#0066FF",
            hover_color="#0052CC",
            font=("Arial", 14, "bold")
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
            border_color=("#555555", "#555555"),
            corner_radius=30,
            variable=self.responsive_var
        )
        self.checkbox1.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.checkbox2 = ctk.CTkCheckBox(
            self.left_panel,
            text="Add Form Validation",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555"),
            corner_radius=30,
            variable=self.validation_var
        )
        self.checkbox2.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.checkbox3 = ctk.CTkCheckBox(
            self.left_panel,
            text="Use Flex Layout",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555"),
            corner_radius=30,
            variable=self.flex_var
        )
        self.checkbox3.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.checkbox4 = ctk.CTkCheckBox(
            self.left_panel,
            text="Use Grid Layout",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555"),
            corner_radius=30,
            variable=self.grid_var
        )
        self.checkbox4.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        self.checkbox5 = ctk.CTkCheckBox(
            self.left_panel,
            text="Include Animations/Icons",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555"),
            corner_radius=30,
            variable=self.animation_var
        )
        self.checkbox5.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        self.checkbox6 = ctk.CTkCheckBox(
            self.left_panel,
            text="Color Transitions",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555"),
            corner_radius=30,
            variable=self.trans_var
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

        self.preview_button = ctk.CTkButton(
            button_frame,
            text="Preview",
            command=self.preview_btn,
            width=120,
            height=32,
            fg_color=("#2B2B2B", "#2B2B2B"),
            hover_color=("#3B3B3B", "#3B3B3B"),
            border_width=1,
            border_color=("#555555", "#555555")
        )
        self.preview_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save File",
            command=self.save_file,
            width=120,
            height=32,
            fg_color=("#2B2B2B", "#2B2B2B"),
            hover_color=("#3B3B3B", "#3B3B3B"),
            border_width=1,
            border_color=("#555555", "#555555")
        )
        self.save_button.pack(side="left", padx=5)

    def generate_prompt(self, options, design_details):
        self.design_details = design_details
        options = {
            "responsive": self.checkbox1.get(),
            "form_validation": self.checkbox2.get(),
            "use_flex_structure": self.checkbox3.get(),
            "use_grid_structure": self.checkbox4.get(),
            "animations": self.checkbox5.get(),
            "color_Transitions": self.checkbox6.get(),
        }

        prompt = f" {design_details}"

        if options["responsive"]:
            prompt += " Generate HTML and CSS code with as much accuracy as possible. Do not make separate files for the HTML, CSS and Javascript code. The design should be fully responsive using modern CSS. The number of all elements and buttons should be same as in the image."
        if options["form_validation"]:
            prompt += " Add form validation functionality using JavaScript and HTML5 validation attributes. The validation messages or error messages should look just like that in the image."
        if options["use_flex_structure"]:
            prompt += " Use Flexbox if necessary to match the image layout accurately."
        if options["use_grid_structure"]:
            prompt += " Use grid layout if necessary to match the image layout accurately."
        if options["animations"]:
            prompt += " Include smooth transitions/animations/icons (if any) just like in the image. The number of icons should be same as in the image."
        if options["color_Transitions"]:
            prompt += " Add same color transitions for buttons and other elements as shown in image when hovered. Keep text size for elements same as in the image as much as possible."

        return prompt

    def generate_code(self):
        self.design_details = self.prompt_input.get("1.0", tk.END).strip()
        self.has_image = bool(self.image_path.get())
        
        options = {
            "responsive": self.responsive_var.get(),
            "form_validation": self.validation_var.get(),
            "use_flex_structure": self.flex_var.get(),
            "use_grid_structure": self.grid_var.get(),
            "animations": self.animation_var.get(),
            "color_Transitions": self.trans_var.get(),
        }
        
        any_checkbox_selected = any(options.values())

        if not self.design_details and not self.has_image and not any_checkbox_selected:
            messagebox.showerror("Error", "Please enter design details, upload an image, or select at least one option!")
            return

        prompt = self.generate_prompt(options, self.design_details)

        self.progress_label.configure(text="Generating code... Please wait")
        self.progress_bar.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.progress_bar.start()

        self.generate_button.configure(state="disabled", text="Generating code...")
        self.upload_button.configure(state="disabled")

        threading.Thread(target=self.generate_code_thread, args=(prompt,), daemon=True).start()

    def generate_code_thread(self, prompt):
        self.prompt = prompt
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            if self.image_path.get():
                image = Image.open(self.image_path.get())
                response = model.generate_content([self.prompt, image])
            else:
                response = model.generate_content(self.prompt)
            
            result = response.text

            self.after(0, self.update_code_preview, result)
            self.after(0, self.stop_progress)
        except Exception as e:
            self.after(0, self.stop_progress)
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
        self.generate_button.configure(state="normal", text="Generate Code")
        self.upload_button.configure(state="normal")

    def update_code_preview(self, code):
        self.code_preview.delete("1.0", "end")
        self.code_preview.insert("1.0", code)

    def copy_code(self):
        code = self.code_preview.get("1.0", tk.END)
        html_start = code.find("<!DOCTYPE html>")
        html_end = code.rfind("</html>") + 7  # Include the closing tag
        if html_start != -1 and html_end != -1:
            code = code[html_start:html_end]
        else:
            messagebox.showwarning("Warning", "Could not find valid HTML content in the response.")
            return
        self.clipboard_clear()
        self.clipboard_append(code)
        messagebox.showinfo("Success", "Code copied to clipboard!")

    def save_file(self):
        code = self.code_preview.get("1.0", tk.END)
        if not code.strip():
            messagebox.showwarning("Warning", "No code to save!")
            return

        html_start = code.find("<!DOCTYPE html>")
        html_end = code.rfind("</html>") + 7  # Include the closing tag
        if html_start != -1 and html_end != -1:
            code = code[html_start:html_end]
        else:
            messagebox.showwarning("Warning", "Could not find valid HTML content in the response.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            messagebox.showinfo("File Saved", f"HTML file saved successfully.\nFile path: {file_path}")
            self.saved_file_path = file_path  # Update the saved_file_path

    def preview_btn(self):
        if self.saved_file_path and os.path.exists(self.saved_file_path):
            webbrowser.open('file://' + os.path.realpath(self.saved_file_path))
        else:
            messagebox.showerror("Save File", "No HTML file generated yet. Please save the code first.")

if __name__ == "__main__":
    app = ModernDesktopApp()
    app.mainloop()