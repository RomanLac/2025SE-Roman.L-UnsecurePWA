import re
import html
import bcrypt

# Code snippet for logging a message
# app.logger.critical("message")

# validation
def check_password(password):
    if not isinstance(password, str):
        return False
    if not (1 <= len(password) <= 9):
        return False
    if not re.match("^[a-zA-Z0-9]*$", password):
        return False

    # alpha and num
    digits = sum(c.isdigit() for c in password)
    letters = sum(c.isalpha() for c in password)
    
    if digits < 3:
        return False
    if letters < 4:
        return False

    return True

# sanitize library
def make_web_safe(string: str) -> str:
    return html.escape(string)

# use this for exam
def replace_characters(input_string: str) -> str:
    to_replace = ["<", ">", ";"]
    replacements = ["%3C", "%3E", "%3B"]
    char_list = list(input_string)
    for i in range(len(char_list)):
        if char_list[i] in to_replace:
            index = to_replace.index(char_list[i])
            char_list[i] = replacements[index]