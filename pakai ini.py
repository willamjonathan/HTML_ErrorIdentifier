def html_checker(file_path):
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
        'html': 'html_tag',
        'table': 'table_tag',
        '!DOCTYPE html': 'doctype_tag',
    }

    def is_valid_identifier(identifier):
        # You can customize this function to match your identifier rules
        return identifier.isidentifier()

    def validate_tag(tag, line_number, column):
        if tag and tag.startswith('/'):
            opening_tag = tag[1:]
            if opening_tag not in tag_mapping:
                return f"Error: Unmatched closing tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"
        elif tag not in tag_mapping:
            return f"Error: Invalid tag '{tag}', operation type: {tag_mapping.get(tag, 'unknown')}, line: {line_number}, column: {column}"
        return None

    def validate_identifier(identifier, line_number, column):
        if not is_valid_identifier(identifier):
            return f"Error: Invalid identifier '{identifier}', line: {line_number}, column: {column}"
        return None

    def process_line(line, line_number):
        errors = []
        in_comment = False
        current_tag = None

        for i, char in enumerate(line):
            if in_comment:
                if line.startswith('-->', i):
                    in_comment = False
            else:
                if char == '<':
                    current_tag = ''
                elif char == '>':
                    if current_tag and not current_tag.endswith('/'):
                        error = validate_tag(current_tag, line_number, i + 1 - len(current_tag))
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
error_list = html_checker('example.html')
for error in error_list:
    print(error)
