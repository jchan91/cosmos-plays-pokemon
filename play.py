import time
import random
import ctypes


SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def Press(hexKeyCode):
    PressKey(hexKeyCode)
    time.sleep(0.3)
    ReleaseKey(hexKeyCode)


hexCodesByName = {
    # 'up' : 0xC8,
    # 'left' : 0xCB,
    # 'right' : 0xCD,
    # 'down' : 0xD0,
    'w' : 0x11,
    'a' : 0x1E,
    's' : 0x1F,
    'd' : 0x20,
    'x' : 0x2D,
    'z' : 0x2C,
    'enter' : 0x1C,
    'back' : 0x0E
}


if __name__ == '__main__':
    numKeys = len(hexCodesByName)

    # Turn off numlock for arrow keys
    # num_lock_in_hex = 0x45
    # Press(num_lock_in_hex)

    while True:
        # time.sleep(1)

        random_index = random.randint(0, numKeys - 1)

        key = hexCodesByName.keys()[random_index]
        keyInHex = hexCodesByName[key]
        print('Selected key: {0}. Hex: {1}'.format(key, keyInHex))
        Press(keyInHex)

