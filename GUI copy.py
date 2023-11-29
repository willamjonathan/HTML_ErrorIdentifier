import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

def validate_html_with_tokens(html_code):
    stack = {}  # Dictionary to keep track of opening tags and their counts
    errors = []  # List to store errors

    # Split the HTML code into lines for better error reporting
    lines = html_code.split('\n')

    in_comment = False  # Flag to track whether inside a comment

    for i, line in enumerate(lines, start=1):
        # Check for opening and closing tags using simple string checks
        if '<!--' in line:
            in_comment = True
        if '-->' in line:
            in_comment = False
            continue  # Skip the rest of the line if inside a comment
    
        if not in_comment:
            if '<table' in line:
                if 'border=' not in line or '>' not in line:
                     errors.append(f"Error: Missing attribute border or > '<table>' tag on line {i}")
                stack.setdefault('table', []).append(('opening_table', i))
            if '</table>' in line:
                if 'table' not in stack or not stack['table']:
                    errors.append(f"Error: Unclosed tag '<table>' on line {i}")
                else:
                    stack['table'].pop()

            # Process only if not inside a comment
            # Define a list of tags to check for opening and closing
            tags_to_check = ['head', 'title', 'body', 'h1', 'tr', 'th', 'td', 'p','h2','h3','h4','a']

            for tag in tags_to_check:
                opening_tag = f'<{tag}>'
                closing_tag = f'</{tag}>'

                if opening_tag in line:
                    stack.setdefault(tag, []).append((f'opening_{tag}', i))
                if closing_tag in line:
                    if tag not in stack or not stack[tag]:
                        errors.append(f"Error: Unclosed tag '{opening_tag}' on line {i}")
                    else:
                        stack[tag].pop()

    # Check for unclosed tags
    for tag, tag_stack in stack.items():
        for item in tag_stack:
            errors.append(f"Error: Found unclosed tag '{item[0]}' for opening tag '<{tag}>' on line {item[1]}")

    # Sort errors based on line number
    errors.sort(key=lambda x: int(x.split()[-1]))

    # If the errors list is empty, the HTML is valid
    return errors

class HTMLUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML File Uploader")

        window_width = 800
        window_height = 600

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.file_path = ""

        self.create_ui()

    def create_ui(self):


        top_buttons_frame = tk.Frame(self.root)
        top_buttons_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.label = tk.Label(top_buttons_frame, text="Select HTML File:", background="#e6e6e6", padx=10, pady=5)
        self.label.pack(side=tk.LEFT, fill=tk.X, pady=10) 

        self.upload_button = tk.Button(top_buttons_frame, text="Upload File", command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT, padx=5)  

        self.save_button = tk.Button(top_buttons_frame, text="Save File", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=5) 


        self.html_text = tk.Text(self.root, height=10, width=80)  
        self.html_text.pack(pady=10, padx=10)

        self.validate_button = tk.Button(self.root, text="Validate HTML", command=self.validate_html)
        self.validate_button.pack(pady=10)


        scrollbar = tk.Scrollbar(self.root, command=self.html_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.html_text.config(yscrollcommand=scrollbar.set)

        self.error_text = tk.Text(self.root, height=15, width=80)  
        self.error_text.pack(pady=10, padx=10)

        scrollbar_error = tk.Scrollbar(self.root, command=self.error_text.yview)
        scrollbar_error.pack(side=tk.RIGHT, fill=tk.Y)
        self.error_text.config(yscrollcommand=scrollbar_error.set)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("HTML Files", "*.html")])

        if file_path:
            self.file_path = file_path
            self.label.config(text=f"Selected HTML File: {os.path.basename(file_path)}")

            with open(file_path, 'r') as file:
                html_content = file.read()
                self.html_text.delete(1.0, tk.END)  
                self.html_text.insert(tk.END, html_content)

    def validate_html(self):
        if not self.file_path:
            tk.messagebox.showwarning("Warning", "Please select an HTML file first.")
            return

        try:
            with open(self.file_path, 'r') as file:
                html_code = file.read()

            errors = validate_html_with_tokens(html_code)

            if not errors:
                tk.messagebox.showinfo("Validation", "HTML is valid.")
            else:
                error_message = "\n".join(errors)
                self.error_text.delete(1.0, tk.END)  # Clear previous errors
                self.error_text.insert(tk.END, error_message)
                tk.messagebox.showerror("Validation", "HTML is not valid. See errors below.")

        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"File '{self.file_path}' not found.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {str(e)}")

    def save_file(self):
        if not self.file_path:
            tk.messagebox.showwarning("Warning", "Please select an HTML file first.")
            return

        save_directory = "html-files/"

        new_file_path = os.path.join(save_directory, os.path.basename(self.file_path))
        shutil.copy(self.file_path, new_file_path)

        tk.messagebox.showinfo("Success", "HTML file saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLUploader(root)
    root.mainloop()
