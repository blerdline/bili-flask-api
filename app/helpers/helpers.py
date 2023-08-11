def convert_escape_chars(string):
    """Converts escape characters such as \n to their actual values"""
    
    # Convert \n to new line, \t to tab, etc.
    string = string.replace('\\n', '\n')
    string = string.replace('\\t', '\t')
    string = string.replace('\\r', '\r')

    return string