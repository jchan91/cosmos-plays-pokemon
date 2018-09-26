import time
import random
import ctypes
import numpy as np


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


class StateMachine:
    _current_state = 'w'
    _transition_table = None
    _key_to_index = {}
    _state_statistics = {}

    
    def __init__(self):
        num_keys = len(action_keys)
        self._transition_table = np.zeros(shape=(num_keys, num_keys))

        # Setup a key -> index dictionary
        for i in range(0, num_keys):
            key = action_keys[i]
            self._key_to_index[key] = i

        # Setup a debugging table of statistics of chosen states
        for key in action_keys:
            self._state_statistics[key] = 0

        # Set all transitions to be the same, regardless of current state
        for from_state in action_keys:
            self.set_transition(from_state, 'w', 1.0)
            self.set_transition(from_state, 'a', 1.0)
            self.set_transition(from_state, 's', 1.0)
            self.set_transition(from_state, 'd', 1.0)
            self.set_transition(from_state, 'x', 1.0)
            self.set_transition(from_state, 'z', 1.0)
            self.set_transition(from_state, 'enter', 0.1)
        
        # Normalize table so for a given from_state, all next_state_probabilities sum to 1.0
        self.normalize_transition_table()


    def get_current_state(self):
        return self._current_state


    def choose_next_state(self):
        transition_probabilities = self._get_transition_probabilities_for_current_state()
        transition_probability_cdf = self._cdf(transition_probabilities)

        random_draw = random.random()
        num_transitions = len(transition_probabilities)
        for i in range(0, num_transitions):
            transition_cdf_value = transition_probability_cdf[i]
            if random_draw < transition_cdf_value:
                # Found chosen key
                chosen_state = action_keys[i]
                self._current_state = chosen_state

                # Accumulate some statistics
                self._state_statistics[chosen_state] = self._state_statistics[chosen_state] + 1
                return
            else:
                # Keep searching up the CDF
                continue


    def get_statistics_summary(self):
        summary = ''
        for key, stat in self._state_statistics.items():
            summary += '{0}: {1}, '.format(key, stat)
        return summary


    def set_transition(self, from_state, to_state, value):
        from_idx = self._key_to_index[from_state]
        to_idx = self._key_to_index[to_state]
        self._transition_table[from_idx, to_idx] = value
    

    def normalize_transition_table(self):
        num_rows = self._transition_table.shape[0]
        for row in range(0, num_rows):
            transition_values = self._transition_table[row]
            self._transition_table[row] = self._transition_table[row] / np.sum(transition_values)


    @staticmethod
    def _cdf(pdf_array):
        num_elems = len(pdf_array)
        cdf_array = np.zeros(num_elems)
        accumulation = 0.0
        for i in range(0, num_elems):
            p = pdf_array[i]
            accumulation = accumulation + p
            cdf_array[i] = accumulation

        # Normalize cdf_array to [0,1]
        cdf_array = cdf_array / accumulation
        return cdf_array


    def _get_transition_probabilities_for_current_state(self):
        current_idx = self._key_to_index[self._current_state]
        return self._transition_table[current_idx]


    def _get_transition_probability_by_index(self, to_state_index):
        current_idx = self._key_to_index[self._current_state]
        return self._transition_table[current_idx, to_state_index]


state_machine = StateMachine()
def choose_random_action_key():
    state_machine.choose_next_state()
    return state_machine.get_current_state()


def save_game():
    save_key_in_hex = hex_codes_by_name[save_key]
    Press(save_key_in_hex, holdTimeInSec=0.1)


current_iteration_since_last_save = 0
def maybe_save_game():
    iterations_per_save = 1000
    global current_iteration_since_last_save

    current_iteration_since_last_save = current_iteration_since_last_save + 1
    if current_iteration_since_last_save % iterations_per_save is 0:
        save_game()
        current_iteration_since_last_save = 0  # Reset the counter


current_biased_vertical_direction = 'w'
current_biased_horizontal_direction = 'a'
def maybe_change_key(current_direction):
    if current_biased_vertical_direction is not current_direction or current_biased_horizontal_direction is not current_direction:
        # Possibly choose a new direction
        choose_again_probability = 1
        p = random.random()
        if p <= choose_again_probability:
            return choose_random_action_key()
        else:
            return current_direction
    else:
        # Keep current direction
        return current_direction


def set_state_machine_bias_direction(state_machine):
    for from_state in action_keys:
        for to_state in action_keys:
            if to_state is current_biased_vertical_direction or to_state is current_biased_horizontal_direction:
                # Set biased direction probabilities
                state_machine.set_transition(from_state, to_state, 5.0)
            elif to_state in move_keys:
                # Set other move key probabilities
                state_machine.set_transition(from_state, to_state, 2.0)
            else:
                # Set other keys
                state_machine.set_transition(from_state, to_state, 1.0)
            state_machine.set_transition(from_state, 'enter', 0.1)

    # Normalize the transition tables after setting new probabilities
    state_machine.normalize_transition_table()


current_iteration_since_last_choosing_of_direction = 0
def maybe_choose_bias_direction():
    global current_iteration_since_last_choosing_of_direction
    global current_biased_vertical_direction
    global current_biased_horizontal_direction
    iterations_per_choosing_direction = 10000

    if current_iteration_since_last_choosing_of_direction % iterations_per_choosing_direction is 0:
        # Choose a new direction bias
        num_keys = 2
        # Choose a vertical bias
        random_index = random.randint(0, num_keys - 1)
        current_biased_vertical_direction = vertical_keys[random_index]
        # Choose a horizontal bias
        random_index = random.randint(0, num_keys - 1)
        current_biased_horizontal_direction = horizontal_keys[random_index]
        # Reset counter
        current_iteration_since_last_choosing_of_direction = 0
        # Increase state machine probabilities for these biased directions
        set_state_machine_bias_direction(state_machine)
        print('Chose ({0}, {1}) direction'.format(
            current_biased_vertical_direction,
            current_biased_horizontal_direction))

    current_iteration_since_last_choosing_of_direction = current_iteration_since_last_choosing_of_direction + 1    


if __name__ == '__main__':
    while True:
        # Choose a random key
        key = choose_random_action_key()

        # Decide how long to hold down the key
        hold_time_in_sec = 0.025
        # Check if possibly modified key is the new key
        if key in move_keys:
            # Hold down a random amount of time
            hold_time_in_sec = random.random() * 0.1  # Up to 0.1 seconds
        
        # Press the key
        key_in_hex = hex_codes_by_name[key]
        print('[{2}, {3}] Selected key: {0} for {1:.2f} sec. Stats: {4}'.format(
            key[0],
            hold_time_in_sec,
            current_biased_vertical_direction,
            current_biased_horizontal_direction,
            state_machine.get_statistics_summary()))
        Press(key_in_hex, hold_time_in_sec)

        # Give the child a chance to save himself
        maybe_save_game()

        # Choose a new biased direction
        maybe_choose_bias_direction()
