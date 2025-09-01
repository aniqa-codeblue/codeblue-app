import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os, sys
from pathlib import Path
import webbrowser
import random
import string
import threading
import google.generativeai as genai
import cohere
import mysql.connector
import traceback
import pyotp
import qrcode
import io
import base64
from datetime import datetime
import requests
import json
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from openai import OpenAI

MODE_ENV = 'production'
CURRENT_VERSION = '1.0.0'

# Email configuration - UPDATED with direct SMTP settings
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'engineering.codeblue@gmail.com',  # Replace with actual sender email
    'sender_password': 'kwls wffw qroa avpz',  # Replace with app password (for Gmail)
    'target_email': 'aniqa.codeblue@gmail.com'  # Admin email to receive QR codes
}

mysql_config = {
    'host' : '68.178.174.206',
    'user' : 'vectorizerimage_code-generator',
    'password' : 'codegenerator_12',
    'database' : 'vectorizerimage_user-management-dashboard',
    'port' : 3306
}

class EmailSender:
    """Email sender using direct SMTP"""
    
    @staticmethod
    def send_qr_email(user_email, user_id, secret_key, qr_image_data):
        """Send QR code via direct SMTP email"""
        try:
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = EMAIL_CONFIG['target_email']
            msg['Subject'] = f'2FA Setup Required - {user_email}'
            
            # Create HTML body with embedded image
            html_body = f"""
            <html>
            <body>
                <h2>Code Blue Generator - 2FA Setup</h2>
                <p><strong>Admin:</strong> {user_email}</p>
                <p><strong>User ID:</strong> {user_id}</p>
                <p><strong>Login Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Secret Key:</strong> <code>{secret_key}</code></p>
                <p>QR Code is attached below. Scan with Google Authenticator.</p>
                <img src="cid:qr_code" width="250" height="250">
                <p>This is an automated message. Please do not reply.</p>
            </body>
            </html>
            """
            
            # Attach HTML body
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach QR code image
            image = MIMEImage(qr_image_data, _subtype="png")
            image.add_header('Content-ID', '<qr_code>')
            image.add_header('Content-Disposition', 'inline', filename='qr_code.png')
            msg.attach(image)
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                server.send_message(msg)
                
            return True, "Email sent successfully via SMTP"
            
        except Exception as e:
            error_msg = f"Email sending error: {str(e)}"
            print(error_msg)
            return False, error_msg
    

class CodeBlue(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window configuration
        self.title("Code Blue")
        self.geometry("1000x600")
        self.minsize(1500, 900)

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
        self.left_panel.grid_columnconfigure(0, weight=3)

        # Header
        header = ctk.CTkLabel(
            self.left_panel,
            text="Upload Image or Describe",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            pady=10
        )
        header.grid(row=0, column=0, padx=10, sticky="ew")

        # Model dropdown
        self.model_dropdown = ctk.CTkComboBox(
            self.left_panel,
            values=["Gemini", "Cohere"],
            font=ctk.CTkFont(size=14, weight='bold'),
            width=150
        )
        self.model_dropdown.grid(row=0, column=1, padx=10, sticky="w")
        self.model_dropdown.set("gemini")
        
        # Prompt section
        prompt_label = ctk.CTkLabel(
            self.left_panel,
            text="Prompt For Design",
            font=ctk.CTkFont(size=14, weight='bold'),
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
        self.prompt_input.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")

        # Upload button
        self.upload_button = ctk.CTkButton(
            self.left_panel,
            text="Upload Image",
            command=self.upload_image,
            height=35,
            fg_color="#0066FF",
            hover_color="#0052CC"
        )
        self.upload_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

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
        self.progress_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

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
        self.checkbox1.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.checkbox2 = ctk.CTkCheckBox(
            self.left_panel,
            text="Add Form Validation",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox2.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.checkbox3 = ctk.CTkCheckBox(
            self.left_panel,
            text="Use Flex Layout",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox3.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.checkbox4 = ctk.CTkCheckBox(
            self.left_panel,
            text="Use Grid Layout",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox4.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.checkbox5 = ctk.CTkCheckBox(
            self.left_panel,
            text="Include Animations/Icons",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox5.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.checkbox6 = ctk.CTkCheckBox(
            self.left_panel,
            text="Color Transitions",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox6.grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.checkbox7 = ctk.CTkCheckBox(
            self.left_panel,
            text="Relevant to Shopify",
            font=ctk.CTkFont(size=13),
            fg_color="#0066FF",
            text_color=("#E0E0E0", "#E0E0E0"),
            hover_color="#0052CC",
            border_color=("#555555", "#555555")
        )
        self.checkbox7.grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky="w")

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
        self.generate_button.grid(row=13, column=0, columnspan=2, padx=10, pady=20, sticky="ew")

        # Image display label
        self.image_label = ctk.CTkLabel(
            self.left_panel,
            text="No image selected",
            font=ctk.CTkFont(size=13),
            text_color=("#E0E0E0", "#E0E0E0")
        )
        self.image_label.grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

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
            "shopify": self.checkbox7.get(),
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
        if options["shopify"]:
            prompt += " Ensure the structure is compatible with Shopify Liquid templates, and consider standard Shopify section structure if relevant."

        return prompt

    def generate_code(self):
        if not self.image_path.get():
            messagebox.showerror("Error", "Please upload an image first!")
            return

        self.progress_label.configure(text="Generating code... Please wait")
        self.progress_bar.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.progress_bar.start()

        threading.Thread(target=self.generate_code_thread, daemon=True).start()

    def generate_code_thread(self):
        """Thread for generating code using selected AI model"""
        try:
            image = Image.open(self.image_path.get())
            prompt = self.generate_prompt()
            selected_model = self.model_dropdown.get().lower()
            result = ""

            if selected_model == "Gemini":
                model = genai.GenerativeModel('gemini-2.0-flash')
                response = model.generate_content([prompt, image])
                result = response.text
            # ... other model implementations

            elif selected_model == "Cohere":
                co = cohere.ClientV2('5Bm3dFUEVTHbfyosOGlOzTQ6zrsbekUv2n8kMxqd')
                gemini_model = genai.GenerativeModel('gemini-2.0-flash')
                vision_prompt = "Analyze this image and describe its layout, components, and visual structure in detail. Include information about positioning, styling, and interactive elements."
                vision_response = gemini_model.generate_content([vision_prompt, image])
                
                # Use the vision response to generate code with Cohere
                enhanced_prompt = f"Based on this visual description: {vision_response.text}\n\n{prompt}"
                response = co.chat(
                    model="command-r-plus", 
                    messages=[{"role": "user", "content": enhanced_prompt}]
                )
                result = response.message.content[0].text

            elif selected_model == "DeepSeek":
                
                client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key="<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>",
                ),
                completion = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=[
                    {
                    "role": "user",
                    "content": prompt
                    }
                ]
                )
                result = completion.choices[0].message.content

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
            self.remove_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
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

class OTPVerificationWindow(ctk.CTk):
    def __init__(self, user_email, user_id):
        super().__init__()
        
        self.user_email = user_email
        self.user_id = user_id
        self.secret_key = pyotp.random_base32()
        self.login_time = datetime.now()
        
        # Configure window - much smaller since only OTP input
        self.title("Two-Factor Authentication")
        self.geometry("450x720")
        self.resizable(False, False)
        
        # Create main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Two-Factor Authentication",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#0D0C0C", "#0D0C0C")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 20))
        
        # User info display
        self.user_info_frame = ctk.CTkFrame(self.main_frame)
        self.user_info_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.user_info_frame.grid_columnconfigure(0, weight=1)
        
        self.user_info_label = ctk.CTkLabel(
            self.user_info_frame,
            text=f"Welcome, {self.user_email}\n\nLogin Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        self.user_info_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Info message
        self.info_label = ctk.CTkLabel(
            self.main_frame,
            text="A QR code has been sent to the administrator for setup.\nPlease wait for the administrator to configure your\nauthenticator, then enter the 6-digit code below.",
            font=ctk.CTkFont(size=13),
            justify="center",
            text_color=("#0D0C0C", "#0D0C0C")
        )
        self.info_label.grid(row=2, column=0, padx=20, pady=20)
        
        # OTP input section
        self.otp_input_frame = ctk.CTkFrame(self.main_frame)
        self.otp_input_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.otp_input_frame.grid_columnconfigure(0, weight=1)
        
        self.otp_label = ctk.CTkLabel(
            self.otp_input_frame,
            text="Enter 6-digit OTP:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.otp_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.otp_entry = ctk.CTkEntry(
            self.otp_input_frame,
            width=250,
            height=60,
            font=ctk.CTkFont(size=24),
            placeholder_text="000000",
            justify="center"
        )
        self.otp_entry.grid(row=1, column=0, padx=20, pady=10)
        
        # Verify button
        self.verify_button = ctk.CTkButton(
            self.otp_input_frame,
            text="Verify OTP",
            command=self.verify_otp,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#0066FF",
            hover_color="#0052CC"
        )
        self.verify_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=4, column=0, padx=20, pady=10)
        
        # Back to login button
        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="Back to Login",
            command=self.back_to_login,
            height=35,
            fg_color="gray",
            hover_color="#555555"
        )
        self.back_button.grid(row=5, column=0, padx=20, pady=(10, 30))
        
        # Generate QR code (but don't display it to user)
        self.generate_qr_for_admin()
        
        # Send notification automatically
        self.status_label.configure(text="Sending setup notification to administrator...", text_color="blue")
        threading.Thread(target=self.send_qr_notification, daemon=True).start()
        
        # Focus on OTP entry
        self.otp_entry.focus_set()
        
        # Bind Enter key
        self.bind('<Return>', lambda event: self.verify_otp())
    
    def generate_qr_for_admin(self):
        """Generate QR code for admin (not displayed to user)"""
        try:
            # Create TOTP URI
            totp_uri = pyotp.totp.TOTP(self.secret_key).provisioning_uri(
                name=self.user_email,
                issuer_name="Code Blue Generator"
            )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=8, border=4)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image = qr_image.resize((250, 250))
            
            # Store QR image data for sending to admin
            img_buffer = io.BytesIO()
            qr_image.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            self.qr_image_data = img_buffer.getvalue()
            
        except Exception as e:
            error_msg = f"Error generating QR code: {e}"
            print(error_msg)
            self.qr_image_data = None
    
    def send_qr_notification(self):
        """Send QR code notification to admin only"""
        try:
            # Save to database first
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            
            update_query = """
                UPDATE users 
                SET totp_secret = %s, updated_at = %s 
                WHERE id = %s
            """
            cursor.execute(update_query, (
                self.secret_key, 
                self.login_time, 
                self.user_id
            ))
            connection.commit()
            cursor.close()
            connection.close()
            
            # Try multiple notification methods for admin
            success = False
            message = ""
            
            # Method 1: Try direct email
            if not success and self.qr_image_data:
                try:
                    email_success, email_msg = EmailSender.send_qr_email(
                        self.user_email, self.user_id, self.secret_key, self.qr_image_data
                    )
                    if email_success:
                        success = True
                        message = "Setup notification sent to administrator via email"

                        #store data in db after successful emailing
                        self.log_to_database()
                    else:
                        print(f"Email sending failed: {email_msg}")
                except Exception as e:
                    print(f"Email exception: {str(e)}")
            
            # Method 2: Save to local file as backup for admin
            if not success and self.qr_image_data:
                try:
                    # Save QR code to local file for admin
                    downloads_folder = str(Path.home() / "Downloads")
                    qr_filename = f"ADMIN_qr_code_{self.user_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    qr_filepath = os.path.join(downloads_folder, qr_filename)
                    
                    with open(qr_filepath, 'wb') as f:
                        f.write(self.qr_image_data)
                    
                    # Save details to text file for admin
                    details_filename = f"ADMIN_2fa_setup_{self.user_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    details_filepath = os.path.join(downloads_folder, details_filename)
                    
                    with open(details_filepath, 'w') as f:
                        f.write(f"Code Blue Generator - 2FA Setup (ADMIN ONLY)\n")
                        f.write(f"===============================================\n\n")
                        f.write(f"User Email: {self.user_email}\n")
                        f.write(f"User ID: {self.user_id}\n")
                        f.write(f"Login Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Secret Key: {self.secret_key}\n\n")
                        f.write(f"QR Code saved as: {qr_filename}\n\n")
                        f.write(f"ADMIN INSTRUCTIONS:\n")
                        f.write(f"1. Scan the QR code with Google Authenticator\n")
                        f.write(f"2. Set up the account for user: {self.user_email}\n")
                        f.write(f"3. Provide the 6-digit code to the user\n")
                    
                    success = True
                    message = "Setup files saved for administrator"
                    
                except Exception as e:
                    message = f"Failed to save setup files: {str(e)}"
                    print(f"File saving exception: {str(e)}")
            
            # Update UI
            if success:
                self.after(0, lambda: self.status_label.configure(
                    text=message + "\nWaiting for administrator setup...", 
                    text_color="green"
                ))
            else:
                self.after(0, lambda: self.status_label.configure(
                    text="Setup notification failed. Please contact administrator.", 
                    text_color="red"
                ))
                
        except Exception as e:
            error_msg = f"Error in send_qr_notification: {e}"
            print(error_msg)
            self.after(0, lambda: self.status_label.configure(
                text="Error sending notification. Please contact administrator.", 
                text_color="red"
            ))

    def log_to_database(self):
        """insert the 2FA info into the logged_in_users table"""

        try:
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()

            insert_query = """INSERT INTO logged_in_users (admin, user_id, login_time, secret_key, qr_code)
                            VALUES (%s, %s, %s, %s, %s)"""
            
            cursor.execute(insert_query, (
                EMAIL_CONFIG['target_email'],
                self.user_id,
                self.login_time,
                self.secret_key,
                self.qr_image_data
            ))

            connection.commit()
            cursor.close()
            connection.close()

            print(f"Successfully inserted 2FA record for user {self.user_id} to database.")

        except mysql.connector.Error as e:
            error_msg = f"Database Logging Error: {e}"
            print(error_msg)

        except Exception as e:
            error_msg = f"General Logging Error: {e}"
            print(error_msg)
    
    def verify_otp(self):
        """Verify the entered OTP"""
        otp_code = self.otp_entry.get().strip()
        
        if not otp_code:
            self.status_label.configure(text="Please enter the 6-digit OTP", text_color="red")
            return
        
        if len(otp_code) != 6 or not otp_code.isdigit():
            self.status_label.configure(text="OTP must be 6 digits", text_color="red")
            self.otp_entry.delete(0, 'end')
            return
        
        # Disable button during verification
        self.verify_button.configure(state="disabled", text="Verifying...")
        
        # Verify OTP
        totp = pyotp.TOTP(self.secret_key)
        if totp.verify(otp_code, valid_window=2):
            self.status_label.configure(text="OTP verified successfully! Opening application...", text_color="green")
            self.after(1000, self.open_main_app)
        else:
            self.status_label.configure(text="Invalid OTP. Please try again.", text_color="red")
            self.otp_entry.delete(0, 'end')
            self.verify_button.configure(state="normal", text="Verify OTP")
    
    def back_to_login(self):
        """Go back to login window"""
        self.destroy()
        app = LoginWindow()
        app.mainloop()
    
    def open_main_app(self):
        """Close this window and open main app"""
        self.destroy()
        app = CodeBlue()
        app.mainloop()

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Code Generator - Login")
        self.geometry("500x600")

        # Create a frame for the content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # App title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="CODE GENERATOR",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(40, 10))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="CODE GENERATOR TOOL",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 30))

        # Login form
        self.login_frame = ctk.CTkFrame(self.main_frame)
        self.login_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.login_frame.grid_columnconfigure(0, weight=1)

        # Email field
        self.email_label = ctk.CTkLabel(
            self.login_frame,
            text="Email:",
            anchor="w",
            font=ctk.CTkFont(size=14, weight='bold')
        )
        self.email_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.email_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter your email",
            width=300,
            height=40,
            border_width=1
        )
        self.email_entry.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")

        # Password field
        self.password_label = ctk.CTkLabel(
            self.login_frame,
            text="Password:",
            anchor="w",
            font=ctk.CTkFont(size=14, weight='bold')
        )
        self.password_label.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="w")

        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Enter your password",
            width=300,
            height=40,
            border_width=1,
            show="•"
        )
        self.password_entry.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Login button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            command=self.login,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.login_button.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Status label for login feedback
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=3, column=0, padx=20, pady=(0, 10))

        # Version display
        self.version_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Version {CURRENT_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.version_label.grid(row=4, column=0, padx=20, pady=(10, 0))

        # Focus on email entry
        self.email_entry.focus_set()

        # Bind Enter key to login function
        self.bind('<Return>', lambda event: self.login())

    def login(self):
        """Handle login process with proper error handling"""
        # Clear previous status
        self.status_label.configure(text="")
        
        # Get email and password from entry fields
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        # Validate input
        if not email:
            self.status_label.configure(text="Please enter your email address")
            self.email_entry.focus_set()
            return
            
        if not password:
            self.status_label.configure(text="Please enter your password")
            self.password_entry.focus_set()
            return

        # Disable login button and show logging in message to prevent multiple attempts
        self.login_button.configure(state="disabled")
        self.status_label.configure(text="Logging in...", text_color="blue")
        self.update()  # Force update to show the logging message
        
        # Use after to give UI time to update before potentially freezing during authentication
        self.after(100, lambda: self.perform_authentication(email, password))
    
    def perform_authentication(self, email, password):
        """Perform actual authentication in a separate method"""
        try:
            status, message, user_data = authenticate_user(email, password)
            
            # Authentication result handling
            if status:
                # Close login window
                self.destroy()
                
                # Show OTP verification window
                app = OTPVerificationWindow(user_data['email'], user_data['id'])
                app.mainloop()
            else:
                self.status_label.configure(text=message, text_color="red")
                self.login_button.configure(state="normal")
                
            # If credentials are invalid, clear password field for security
            if "Invalid" in message:
                self.password_entry.delete(0, 'end')
                self.password_entry.focus_set()
        except Exception as e:
            error_msg = f"Login error: {str(e)}"
            self.status_label.configure(text=error_msg, text_color="red")
            self.login_button.configure(state="normal")
            print(f"Authentication error: {e}")  # Log the full error

def authenticate_user(email, password):
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor(dictionary=True)

        user_query = """
            SELECT id, email, password
            FROM users 
            WHERE email = %s AND password = %s
        """
        cursor.execute(user_query, (email, password))
        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if not user:
            messagebox.showerror("Invalid Credentials", "Kindly enter correct email or password.")
            return False, "Invalid email or password", None
        
        return True, "Authentication Successful", user
    
    except mysql.connector.Error as err:
        error_msg = f"Database Error: {err}"
        print(error_msg)
        
        if MODE_ENV == 'testing':
            messagebox.showerror("Testing Mode disabled", "Kindly change the environment mode to production.")
            return False, "Authentication service unavailable. Please try again later.", None
        else:
            return False, error_msg, None

def checkIfVersionValid():
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor(dictionary=True)

        version_query = "SELECT * FROM version ORDER BY id DESC LIMIT 1"
        cursor.execute(version_query)
        version = cursor.fetchone()

        cursor.close()
        connection.close()
        
        if version and version.get('version_number') != CURRENT_VERSION:
            return False
        else:
            return True
    except mysql.connector.Error as err:
        print(f"Version check error: {err}")
        return True  # Allow app to continue if version check fails

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
        return cursor.fetchone() is not None
    except mysql.connector.Error:
        return False

def setup_database_tables():
    """Setup required database tables for 2FA"""
    try:
        connection = mysql.connector.connect(**mysql_config)
        cursor = connection.cursor()
        
        # Only add the columns we need
        columns_to_add = [
            {
                'name': 'totp_secret',
                'definition': 'VARCHAR(32) DEFAULT NULL'
            },
            {
                'name': 'updated_at',
                'definition': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'
            }
        ]
        
        for column in columns_to_add:
            if not check_column_exists(cursor, 'users', column['name']):
                try:
                    alter_query = f"ALTER TABLE users ADD COLUMN {column['name']} {column['definition']}"
                    cursor.execute(alter_query)
                    print(f"Added column: {column['name']}")
                except mysql.connector.Error as e:
                    print(f"Error adding column {column['name']}: {e}")
            else:
                print(f"Column {column['name']} already exists")
        
        # Create logged_in_users table if it doesn't exist
        create_logged_users_table = """
            CREATE TABLE IF NOT EXISTS logged_in_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Admin VARCHAR(255) NOT NULL,
                `User ID` INT NOT NULL,
                `Log in Time` TIMESTAMP NOT NULL,
                `Secret Key` VARCHAR(32) NOT NULL,
                `QR Code` LONGBLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        cursor.execute(create_logged_users_table)
        print("logged_in_users table created or already exists")
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database setup completed successfully")
        
    except mysql.connector.Error as err:
        print(f"Database setup error: {err}")

def main():
    """Main function to handle application startup"""
    try:
        # Setup database tables for 2FA
        #setup_database_tables()
        
        # Check if we're in testing mode - skip login
        if MODE_ENV == 'testing':
            app = CodeBlue()
            app.mainloop()
        else:
            # Production mode - check version and show login
            try:
                checkVersionValidity = checkIfVersionValid()
                if checkVersionValidity:
                    app = LoginWindow()
                    app.mainloop()
                else:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Version Error", 
                                       'Your app version is outdated or invalid. Please update to the latest version.')
                    sys.exit(1)
            except mysql.connector.Error as db_err:
                # Handle database connectivity issues
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Database Connection Error", 
                                   f"Could not connect to database: {str(db_err)}\n\nThe application will continue in offline mode.")
                # Continue with login window even if DB is unavailable
                app = LoginWindow()
                app.mainloop()
    except Exception as e:
        # Log the error and show user-friendly message
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
        
        # Display error message to user
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Application Error", 
                           f"An unexpected error occurred: {str(e)}\n\nDetails have been written to error_log.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()