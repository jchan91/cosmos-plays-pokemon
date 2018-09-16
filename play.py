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


def Press(hexKeyCode, holdTimeInSec):
    PressKey(hexKeyCode)
    time.sleep(holdTimeInSec)
    ReleaseKey(hexKeyCode)


hex_codes_by_name = {
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
    'p': 0x19,
    'enter' : 0x1C,
    'back' : 0x0E
}


move_keys = [
    'w',
    'a',
    's',
    'd'
]


save_key = 'p'


def SaveGame():
    save_key_in_hex = hex_codes_by_name[save_key]
    Press(save_key_in_hex, holdTimeInSec=0.1)


current_iteration_since_last_save = 0
def MaybeSaveGame():
    iterations_per_save = 5
    global current_iteration_since_last_save

    current_iteration_since_last_save = current_iteration_since_last_save + 1
    if current_iteration_since_last_save % iterations_per_save is 0:
        SaveGame()
        current_iteration_since_last_save = 0  # Reset the counter
    print(current_iteration_since_last_save)


if __name__ == '__main__':
    num_keys = len(hex_codes_by_name)
    keys = hex_codes_by_name.keys()

    # Turn off numlock for arrow keys
    # num_lock_in_hex = 0x45
    # Press(num_lock_in_hex)

    while True:
        # Choose a random key
        random_index = random.randint(0, num_keys - 1)
        key = keys[random_index]

        # Decide how long to hold down the key
        hold_time_in_sec = 0.02
        if key in move_keys:
            # Hold down a random amount of time
            hold_time_in_sec = random.random() * 3.0  # Up to 3 seconds
        
        # Press the key
        key_in_hex = hex_codes_by_name[key]
        print('Selected key: {0} ({1}) for {2:.2f} sec'.format(
            key,
            key_in_hex,
            hold_time_in_sec))
        Press(key_in_hex, hold_time_in_sec)

        # Give the child a chance to save himself
        MaybeSaveGame()
