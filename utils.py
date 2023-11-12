import copy

class UnicodeColors:
    '''https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit'''
    RESET =     '\033[0m'
    GRAY =      '\033[48;5;235m'
    YELLOW =    '\033[48;5;226m'
    GREEN =     '\033[48;5;106m'

class HTMLColors:
    '''https://en.wikipedia.org/wiki/Web_colors#HTML_color_names'''
    RESET =     'white'
    GRAY =      'gray'
    YELLOW =    'yellow'
    GREEN =     'green'

def format_str(letter, state):
    d = {
        "correct":  UnicodeColors.GREEN,
        "present":  UnicodeColors.YELLOW,
        "absent":   UnicodeColors.GRAY,
        "empty":    UnicodeColors.RESET
    }
    color = d.get(state, UnicodeColors.RESET)
    if state == "empty":
        letter = "\u25A1"
    return color + letter.upper() + UnicodeColors.RESET

def format_html(letter, state):
    d = {
        "correct":  HTMLColors.GREEN,
        "present":  HTMLColors.YELLOW,
        "absent":   HTMLColors.GRAY,
        "empty":    HTMLColors.RESET
    }
    color = d.get(state, "white")
    if state == "empty":
        letter = "&#x25A1;"
    else:
        letter = letter.upper()
    snippet = f'<span style="background-color: {color}; width: 15px; display: inline-block;">{letter}</span>'
    return snippet


def grid_to_str(grid_list, formatted=False):
    return "\n".join(
        [
            " ".join( 
                [ 
                    format_str(letter, state) if formatted else letter
                    for (state, letter) in row
                ]
            ) 
            for row in grid_list
        ]
    )

def grid_to_html(grid_list):
    return "<br>".join(
        [
            "".join( 
                [ 
                    format_html(letter, state) 
                    for (state, letter) in row
                ]
            ) 
            for row in grid_list
        ]
    )
