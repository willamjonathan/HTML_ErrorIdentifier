def  html_checker(file_path):
    tag_mapping = {
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
        'href':'reference'
    }

    the_tag =[]
    the_closing = []
    
    def validate_html_language(line):
        if 'html' in line.lower() and 'lang' in line.lower():
            start_index = line.lower().find('lang') + 5  # Adjusted the start index
            end_index = len(line) # Set end_index to the length of the line
            language_value = line[start_index:end_index].strip()
            
            if len(language_value) != 4:
                return False

        return True
        
    def validate_tag(tag, line_number, column):
        if tag.startswith("div class"):
            the_tag.append('div')
            return None
        if tag.startswith("!DOCTYPE html"):
            return None
        if tag.startswith("html lang"):
            the_tag.append("html")
            return None
        if tag.startswith("meta charset"):
            return None
        if tag.startswith("a href"):
            the_tag.append("a")
            return None
        if tag.startswith("meta name"):
            return None

        if not tag.startswith("/"):
            opening_tag = tag[0:]
            the_tag.append(opening_tag)
            print("Opening tag:",the_tag)

            if opening_tag not in tag_mapping:
                return f"Error: Unmatched closing tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"

        elif tag.startswith('/'):
            closing_tag = tag[1:]  # Remove the '/' from the closing tag
            opening_tag = tag[0:]
            the_closing.append(closing_tag)
            # print(the_closing)

            if not the_tag:
                return f"Error: Unmatched closing tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"

        # Check if the closing tag matches the last opening tag
            last_opening_tag = the_tag[-1]
            if closing_tag == last_opening_tag:
                opening_tag = the_tag.pop()  # Get the last opening tag
            else:
                return f"Error: Unmatched closing tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"


            print(opening_tag)
            print("Closing tag", the_closing)
            print(closing_tag)
            
            if opening_tag != closing_tag:
                return f"Error: Mismatched closing tag '{opening_tag}' for opening tag '{opening_tag}', operation type: {tag_mapping.get(opening_tag, 'unknown')}, line: {line_number}, column: {column}"

        elif tag not in tag_mapping:
            if not validate_html_language(tag):
                return f"Error: Invalid tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"

        

        # if len(the_tag) > len(the_closing):
        #     return f"Error: Unclosed tag '{the_tag[-1]}', line: {line_number}"

        # # Check the last closing tag
        # if the_closing and not the_tag:
        #     last_closing_tag = the_closing[-1]
        #     return f"Warning: Last closing tag '{last_closing_tag}' does not have a corresponding opening tag, line: {line_number}, column: {column}"

        return None


    def process_line(line, line_number):
        errors = []
        tag = []
        in_comment = False
        current_tag = None

        for i, char in enumerate(line):
            # print("               ", i, char, in_comment)
            if in_comment:
                print(line, "TEST")
                if char == '>':
                    # print("Going out the comment")
                    in_comment = False
                    current_tag = None
                if line.startswith('<!--'):
                    print(len(line))
                    if i == (len(line) - 1):
                        # print("Going out the comment")
                        in_comment = False
                        current_tag = None

            else:
                if line.startswith('<!--'):
                    # print("Inside a comment")
                    in_comment = True
                    current_tag = None
                if line.endswith('-->'):
                    # print("Inside a comment")
                    in_comment = True
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
                        error = validate_tag(current_tag, line_number, i + 1 - len(current_tag))
                        # print(error)
                        if error:
                            errors.append(error)
                    current_tag = None
                        
                elif current_tag is not None:
                    current_tag += char

        if in_comment:
            errors.append(f"Error: Unclosed multi-line comment in line {line_number}")

        if current_tag:
            print(current_tag, "COBAAAAAAAA")
            if current_tag.startswith('/'):
                current_tag = current_tag[1:]
                
                errors.append(f"Error: Missing closing '>' , operation type: {tag_mapping.get(current_tag, 'unknown')}, line: {line_number}")
            else:
                errors.append(f"Error: Missing closing '>' , operation type: {tag_mapping.get(current_tag, 'unknown')}, line: {line_number}")

        return errors

    errors = []
    with open(file_path, 'r') as file:
        line_number = 0
        for line in file:
            line_number += 1
            line = line.strip()
            if line:
                errors.extend(process_line(line, line_number))
    
    unclosed_tags = set(the_tag) - set(the_closing)
    if unclosed_tags:
        errors.extend([f"Error: Unclosed tag '{tag}', line: {line_number}, operation type: {tag_mapping.get(tag, 'unknown')}" for tag in unclosed_tags])

    return errors

# Example usage:
error_list = html_checker('html-files/example.html')
for error in error_list:
    print(error)
