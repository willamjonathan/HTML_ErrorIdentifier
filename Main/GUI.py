import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

class HTMLChecker:
    def __init__(self):
        self.tag_mapping = {
            'head': 'head_tag',
            'title': 'title_tag',
            'body': 'body_tag',
            'h1': 'h1_tag',
            'tr': 'tr_tag',
            'th': 'th_tag',
            'td': 'td_tag',
            'p': 'p_tag',
            'h2': 'h2_tag',
            'h3': 'h3_tag',
            'h4': 'h4_tag',
            'a': 'a_tag',
            'li': 'list',
            'footer': 'footer',
            'ul':'unordered list',
            'header': 'header',
            'style': 'style',
            'ul': 'ul',
            'nav': 'navigation',
            'section': 'section',
            'meta charset="UTF8"':'UTF-8',
            'html': 'html_tag',
            'table': 'table_tag',
            '!DOCTYPE html': 'doctype_tag',
            'div':'div_tag',
            'href':'reference',
            'img':'img_tag'
        }

        self.the_tag =[]
        self.the_closing = []
        self.in_comment = False
        self.msg = None
    
    def validate_html_language(self, line):
        if 'html' in line.lower() and 'lang' in line.lower():
            start_index = line.lower().find('lang') + 5 
            end_index = len(line) 
            language_value = line[start_index:end_index].strip()
            
            if len(language_value) != 4:
                return False

        return True
        
    def validate_tag(self, tag, line_number, column, max_line_number):
        if tag.startswith("div class"):
            self.the_tag.append('div')
            return None
        if tag.startswith("!DOCTYPE html"):
            return None
        if tag.startswith("html lang"):
            self.the_tag.append("html")
            return None
        if tag.startswith("meta charset"):
            return None
        if tag.startswith("a href"):
            self.the_tag.append("a")
            return None
        if tag.startswith("meta name"):
            return None

        if not tag.startswith("/"):
            opening_tag = tag[0:]
            if not opening_tag.startswith("img"):
                self.the_tag.append(opening_tag)
                print("Opening tag:",self.the_tag)

                if opening_tag not in self.tag_mapping:
                    return f"Error: Invalid tag '{tag}', operation type: {self.tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"


        if tag.startswith('/'):
            closing_tag = tag[1:]
            opening_tag = tag[1:]
            self.the_closing.append(closing_tag)
            # print(the_closing)

            if not self.the_tag:
                return f"Error: Unmatched closing tag '{tag}', operation type: {self.tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"
        
            last_opening_tag = self.the_tag[-1]
            if closing_tag == last_opening_tag:
                opening_tag = self.the_tag.pop() 
                closing_tag = self.the_closing.pop()
                print(f"POPPED {opening_tag} BECAUSE closing_tag == last_opening_tag ")
            else:
                # print("IM HERE")
                found_match = False
                for i in self.the_tag[::-1]:
                    if i == closing_tag:
                        # opening_tag = self.the_tag.remove(i)
                        # print("IM HERE 2")
                        found_match = True
                        break

                if not found_match:
                    if closing_tag not in self.the_tag:
                        # print(f"BEEBOOP!!!!!!!!!!!!! {opening_tag} not found_match ")
                        closing_tag = self.the_closing.pop()
                        return f"Error: No opening tag for closing tag '{opening_tag}', operation type: {self.tag_mapping.get(closing_tag, 'unknown')}, line: {line_number}, column: {column}"
                    else:
                        # print("IM HERE 3")
                        opening_tag = self.the_tag.pop()
                        closing_tag = self.the_closing.pop()
                        print(f"POPPED {opening_tag} BECAUSE not found_match ")
                        return f"Error: Unclosed closing tag '{opening_tag}', operation type: {self.tag_mapping.get(closing_tag, 'unknown')}, line: {line_number}, column: {column}"
                    
            # print("Opening tag", self.the_tag)
            # print(opening_tag)
            # print("Closing tag", self.the_closing)
            # print(closing_tag)
            
            if opening_tag != closing_tag :
                return f"Error: Mismatched closing tag '{closing_tag}' for opening tag '{opening_tag}', operation type: {self.tag_mapping.get(opening_tag, 'unknown')}, line: {line_number}, column: {column}"

        elif tag not in self.tag_mapping:
            if not self.validate_html_language(tag):
                return f"Error: Invalid tag '{tag}', operation type: {self.tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"
        
        if line_number == max_line_number:
            for i in self.the_tag:
                for j in self.the_closing:
                    if i not in self.the_closing:
                        # print(f"YES3 {i} AND {self.the_closing}")
                        self.the_tag.remove(i)
                        return f"Error: No closing tag '{i}' for opening tag '{i}', operation type: {self.tag_mapping.get(i, 'unknown')}, line: {line_number}, column: {column}"
                    else:
                        pass

        return None


    def process_line(self, line, line_number, max_line_number):
        errors = []
        current_tag = None

        for i, char in enumerate(line):
            # print("               ", i, char, self.in_comment)
            if self.in_comment:
                # print(line, "TEST")
                if line.endswith('-->'):
                    # print("Line 128")
                    self.in_comment = False
                    current_tag = None
                    # endComment = line_number
                    break
                else:
                    break

            else:
                if line.startswith('<!--') and line.endswith('-->'):
                    # print("Inside a 1 line comment")
                    self.in_comment = True
                    # startComment = line_number
                    current_tag = None
                elif line.startswith('<!--') and not line.endswith('-->'):
                    # print("Line 142")
                    self.in_comment = True
                    current_tag = None
                    break
                if line.endswith('-->'):
                    # print("Line 147")
                    self.in_comment = True
                    current_tag = None
                if char == '<':
                    current_tag = ''
                    # if current_tag.startswith('/'):
                    #     current_tag = current_tag[1:]
                    #     closing_tag = current_tag
                    #     print(closing_tag)
                elif char == '>':
                    if current_tag and not current_tag.endswith('/'):
                        # print (current_tag)
                        error = self.validate_tag(current_tag, line_number, i + 1 - len(current_tag), max_line_number)
                        # print(error)
                        if error:
                            errors.append(error)
                    current_tag = None
                        
                elif current_tag is not None:
                    current_tag += char

        # if in_comment and (line_number not in range(startComment, endComment)):
        #     errors.append(f"Error: Unclosed multi-line comment in line {line_number}")

        if current_tag:
            # print(current_tag, "COBAAAAAAAA")
            if current_tag.startswith('/'):
                current_tag = current_tag[1:]
                
                errors.append(f"Error: Missing closing '>' , operation type: {self.tag_mapping.get(current_tag, 'unknown')}, line: {line_number}")
            else:
                errors.append(f"Error: Missing closing '>' , operation type: {self.tag_mapping.get(current_tag, 'unknown')}, line: {line_number}")

        return errors

    def html_checker(self, file_path):
        errors = []
        with open(file_path, 'r') as file:
            max_line_number = 0
            for i in file:
                max_line_number += 1

        # print(max_line_number)
        with open(file_path, 'r') as file:
            # max_line_number = 0
            current_line = 0
            for line in file:
                current_line += 1
                line = line.strip()
                if line:
                    errors.extend(self.process_line(line, current_line, max_line_number))
        
    
        unclosed_tags = set(self.the_tag) - set(self.the_closing)
        if unclosed_tags:
            errors.extend([f"Error: Unclosed tag '{tag}', line: {current_line}, operation type: {self.tag_mapping.get(tag, 'unknown')}" for tag in unclosed_tags])

        return errors

class HTMLUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML File Uploader")

        self.create_ui()

    def create_ui(self):
        self.root.columnconfigure(0, weight=1)

        top_buttons_frame = tk.Frame(self.root, background="#e6e6e6")
        top_buttons_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label = tk.Label(top_buttons_frame, text="Select HTML File:", padx=10, pady=5)
        self.label.grid(row=0, column=0, sticky="w")

        self.upload_button = tk.Button(top_buttons_frame, text="Upload File", command=self.upload_file)
        self.upload_button.grid(row=0, column=1, padx=5)

        self.html_text = tk.Text(self.root, height=10, width=80)
        self.html_text.grid(row=1, column=0, padx=10, sticky="nsew")
        self.html_text.config(state="normal")

        self.validate_button = tk.Button(self.root, text="Validate HTML", command=self.validate_html)
        self.validate_button.grid(row=2, column=0, pady=10)

        scrollbar = tk.Scrollbar(self.root, command=self.html_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.html_text.config(yscrollcommand=scrollbar.set)

        self.error_text = tk.Text(self.root, height=15, width=80)
        self.error_text.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.error_text.config(state="normal")

        scrollbar_error = tk.Scrollbar(self.root, command=self.error_text.yview)
        scrollbar_error.grid(row=3, column=1, sticky="ns")
        self.error_text.config(yscrollcommand=scrollbar_error.set)

        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)

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
            errors = HTMLChecker().html_checker(self.file_path)

            if not errors:
                self.error_text.delete(1.0, tk.END)
                tk.messagebox.showinfo("Validation", "HTML is valid.")
            else:
                error_message = "\n".join(errors)
                self.error_text.delete(1.0, tk.END)
                self.error_text.insert(tk.END, error_message)
                tk.messagebox.showerror("Validation", "HTML is not valid. See errors below.")

        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"File '{self.file_path}' not found.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HTMLUploader(root)
    root.mainloop()
