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
        'header': 'header',
        'style': 'style',
        'ul': 'ul',
        'nav': 'navigation',
        'section': 'section',
        'meta charset="UTF8"':'UTF-8',
        'html': 'html_tag',
        'table': 'table_tag',
        '!DOCTYPE html': 'doctype_tag',
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
        if tag.startswith("!DOCTYPE html"):
            the_tag.append("html")
            return None
        if tag.startswith("html lang"):
            the_tag.append("html")
            return None
        if tag.startswith("meta charset"):
            return None

        if not tag.startswith("/"):
            opening_tag = tag[0:]
            the_tag.append(opening_tag)
            print(the_tag)

            if opening_tag not in tag_mapping:
                return f"Error: Unmatched closing tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"

        elif tag.startswith('/'):
            closing_tag = tag[1:]  # Remove the '/' from the closing tag
            the_closing.append(closing_tag)
            print(the_closing)

            if not the_tag:
                return f"Error: Unmatched closing tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"

            opening_tag = the_tag.pop()  # Get the last opening tag
            if opening_tag != closing_tag:
                return f"Error: Mismatched closing tag '{opening_tag}' for opening tag '{opening_tag}', operation type: {tag_mapping.get(opening_tag, 'unknown')}, line: {line_number}, column: {column}"

        elif tag not in tag_mapping:
            if not validate_html_language(tag):
                return f"Error: Invalid tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"

        # # Check the last closing tag
        # if the_closing and not the_tag:
        #     last_closing_tag = the_closing[-1]
        #     return f"Warning: Last closing tag '{last_closing_tag}' does not have a corresponding opening tag, line: {line_number}, column: {column}"

        return None



    def validate_identifier(identifier, line_number, column):
        if not is_valid_identifier(identifier):
            return f"Error: Invalid identifier '{identifier}', line: {line_number}, column: {column}"
        return None

    def process_line(line, line_number):
        errors = []
        tag = []
        in_comment = False
        current_tag = None

        for i, char in enumerate(line):
            if in_comment:
                if line.startswith('-->', i):
                    in_comment = False

            else:
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
                elif char == '-':
                    if line.startswith('<!--', i):
                        in_comment = True
                elif current_tag is not None:
                    current_tag += char

        if in_comment:
            errors.append(f"Error: Unclosed multi-line comment in line {line_number}")

        if current_tag:
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
    

    return errors
# Example usage:
error_list = html_checker('ayam.html')
for error in error_list:
    print(error)
