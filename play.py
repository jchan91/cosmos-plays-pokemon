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


action_keys = [
    'w',
    'a',
    's',
    'd',
    'x',
    'z',
    'enter'
]


move_keys = [
    'w',
    'a',
    's',
    'd'
]

vertical_keys = [
    'w',
    's'
]

horizontal_keys = [
    'a',
    'd'
]


start_key = 'enter'


save_key = 'p'


def ChooseRandomActionKey():
    num_keys = len(action_keys)
    random_index = random.randint(0, num_keys - 1)
    key = action_keys[random_index]
    return key


current_biased_vertical_direction = 'w'
current_biased_horizontal_direction = 'a'
def MaybeChangeKey(current_direction):
    if current_biased_vertical_direction is not current_direction or current_biased_horizontal_direction is not current_direction:
        # Possibly choose a new direction
        choose_again_probability = 1
        p = random.random()
        if p <= choose_again_probability:
            return ChooseRandomActionKey()
        else:
            return current_direction
    else:
        # Keep current direction
        return current_direction


def SaveGame():
    save_key_in_hex = hex_codes_by_name[save_key]
    Press(save_key_in_hex, holdTimeInSec=0.1)


current_iteration_since_last_save = 0
def MaybeSaveGame():
    iterations_per_save = 1000
    global current_iteration_since_last_save

    current_iteration_since_last_save = current_iteration_since_last_save + 1
    if current_iteration_since_last_save % iterations_per_save is 0:
        SaveGame()
        current_iteration_since_last_save = 0  # Reset the counter


current_iteration_since_last_choosing_of_direction = 0
def MaybeChooseRandomDirection():
    global current_iteration_since_last_choosing_of_direction
    global current_biased_vertical_direction
    global current_biased_horizontal_direction
    iterations_per_choosing_direction = 10000

    current_iteration_since_last_choosing_of_direction = current_iteration_since_last_choosing_of_direction + 1
    if current_iteration_since_last_choosing_of_direction % iterations_per_choosing_direction is 0:
        num_keys = 2
        random_index = random.randint(0, num_keys - 1)
        current_biased_vertical_direction = vertical_keys[random_index]
        random_index = random.randint(0, num_keys - 1)
        current_biased_horizontal_direction = horizontal_keys[random_index]
        current_iteration_since_last_choosing_of_direction = 0
        print('Chose ({0}, {1}) direction'.format(
            current_biased_vertical_direction,
            current_biased_horizontal_direction))


if __name__ == '__main__':
    keys = hex_codes_by_name.keys()

    # Turn off numlock for arrow keys
    # num_lock_in_hex = 0x45
    # Press(num_lock_in_hex)

    while True:
        # Choose a random key
        key = ChooseRandomActionKey()

        # Decide how long to hold down the key
        hold_time_in_sec = 0.001
        if key in move_keys:
            # First decide whether to keep it
            key = MaybeChangeKey(key)

        # Check if possibly modified key is the new key
        if key in move_keys:
            # Hold down a random amount of time
            hold_time_in_sec = random.random() * 0.025  # Up to 0.1 seconds
        
        if key is start_key:
            # Have some probability of keeping the start key
            random_i = random.random()  # Gives me a number from [0,1]
            probability_to_keep_start_key = 0.5
            if random_i > probability_to_keep_start_key:
                # Don't keep this start key
                key = ChooseRandomActionKey()
        
        # Press the key
        key_in_hex = hex_codes_by_name[key]
        print('[{3}, {4}] Selected key: {0} ({1}) for {2:.2f} sec'.format(
            key,
            key_in_hex,
            hold_time_in_sec,
            current_biased_vertical_direction,
            current_biased_horizontal_direction))
        Press(key_in_hex, hold_time_in_sec)

        # Give the child a chance to save himself
        MaybeSaveGame()

        # Choose a new biased direction
        MaybeChooseRandomDirection()
