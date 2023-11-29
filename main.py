def validate_html_with_tokens(html_code):
    valid_tags = {'<head>': 'head_tag', '<title>': 'title_tag', '<body>': 'body_tag',
                  '<h1>': 'h1_tag', '<tr>': 'tr_tag', '<th>': 'th_tag', '<td>': 'td_tag',
                  '<p>': 'p_tag', '<h2>': 'h2_tag', '<h3>': 'h3_tag', '<h4>': 'h4_tag',
                  '<table>': 'table_tag', '<a>': 'a_tag', '<!DOCTYPE html>': 'doctype_tag'}

    stack = {}  # Dictionary to keep track of opening tags and their counts
    errors = []  # List to store errors

    in_comment = False  # Flag to track whether inside a comment
    inside_tag = False  # Flag to track whether currently parsing a tag
    current_tag = ""  # Variable to store the current tag being parsed

    line_number = 1  # Variable to store the current line number

    for i, char in enumerate(html_code, start=1):
        # Check for comments
        if char == '<' and html_code[i:i + 4] == '<!--':
            in_comment = True
        elif char == '-' and in_comment and html_code[i:i + 3] == '-->':
            in_comment = False

        # Skip characters within comments
        if in_comment:
            continue

        # Check for opening and closing tags using character checks
        if char == '<':
            inside_tag = True
            current_tag = ""
        elif char == '>':
            inside_tag = False
            tag_type = current_tag.lower()
            if tag_type.startswith('</'):
                closing_tag = tag_type[2:-1]
                if closing_tag not in stack or not stack[closing_tag]:
                    errors.append(f"Error: Unclosed tag '{closing_tag}' on line {line_number}, char {i}")
                else:
                    stack[closing_tag].pop()
            else:
                # Extract tag name from the tag with attributes
                tag_name = tag_type.split()[0]
                if tag_name in valid_tags:
                    stack.setdefault(tag_name, []).append((f'opening_{valid_tags[tag_name]}', line_number, i))
                else:
                    errors.append(f"Error: Invalid tag '{tag_name}' on line {line_number}, char {i}. Operator name: {valid_tags.get(tag_name, 'Unknown')}")
                current_tag = ""  # Reset current_tag after processing the tag
        elif char == '!':
            # Check for comments
            if html_code[i:i + 2] == '--':
                in_comment = True
        elif char == '-' and in_comment:
            # Check for the end of comments
            if html_code[i:i + 2] == '--':
                in_comment = False
                continue
        elif char == '\n':
            line_number += 1
            continue  # Skip newline characters
        elif char.isspace():
            continue  # Skip whitespace
        elif not inside_tag and not in_comment:
            continue  # Skip non-tag content

        # Collect characters to form the current tag
        if inside_tag and not in_comment:
            current_tag += char

    # Check for unclosed tags
    for tag, tag_stack in stack.items():
        for item in tag_stack:
            errors.append(f"Error: Found unclosed tag '{item[0]}' for opening tag '{tag}' on line {item[1]}, char {item[2]}")

    # Sort errors based on line number and character position
    errors.sort(key=lambda x: (int(x.split()[-4]), int(x.split()[-2])) if x.split()[-4].isdigit() and x.split()[-2].isdigit() else (float('inf'), float('inf')))

    # If the errors list is not empty, print the errors
    if errors:
        for error in errors:
            print(error)

    # If the errors list is empty, the HTML is valid
    return not errors

# Read HTML code from a file
file_path = 'example.html'  # Replace with the actual path to your HTML file

try:
    with open(file_path, 'r') as file:
        html_code = file.read()

    # Example usage
    if validate_html_with_tokens(html_code):
        print("HTML is valid.")
    else:
        print("HTML is not valid.")

except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
except Exception as e:
    print(f"Error: {str(e)}")
