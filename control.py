from pynput.mouse import Controller
from pynput.keyboard import Controller

#you cannot control mouse and keyboard together

#(left to right, top to bottom) movement of mouse in pixels from top left to the screen ==> is the meaning of (10,20))
#you can imagine the top left to be (0,0)
def controlMouse():
    mouse = Controller()
    mouse.position = (500,200)

def controlKeyboard():
    keyboard = Controller()
    keyboard.type("I am awesome")

controlKeyboard()
