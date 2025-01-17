""" All functions based on user input """


import time
import msvcrt


def confirm(delay=1):
    """
    Pauses terminal for 1 second or until key press
    :return: None
    """

    print(f"Press any key or wait {delay} sec to continue")
    startTime = time.time()
    inp = None
    while True:
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > delay:
            break


def get_input():
    """ 
    Gets user input including some special inputs
    :return: key if recognized else None
    """
    first_byte = msvcrt.getch()

    if first_byte in {b'\x00', b'\xe0'}:

        second_byte = msvcrt.getch()
        
        arrow_keys = {
            b'H': 'up',
            b'P': 'down',
            b'K': 'left',
            b'M': 'right'
        }
        
        key_name = arrow_keys.get(second_byte, None)
        
        if key_name:
            return key_name
        else:
            return None
    
    elif first_byte == b'\r':
        return "enter"
    
    elif first_byte == b' ':
        return "space"
    
    elif first_byte == b'\x1b':
        return "esc"

    else:

        try:
            char = first_byte.decode('utf-8')
            return char        

        except UnicodeDecodeError:
            return None
