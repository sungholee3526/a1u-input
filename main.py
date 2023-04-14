import serial
from pynput import keyboard

REQUEST_BYTES = bytes([0xA6, 0x01, 0x00])

SYS_LIVE = 0b00010000
SYS_VOLUME = 0b00000011
JOY_U = 0b00001000
JOY_D = 0b00000010
JOY_L = 0b00000100
JOY_R = 0b00000001
BTN_A = 0b00001000
BTN_B = 0b00000001
BTN_C = 0b00010000
BTN_X = 0b00000100
BTN_START = 0b00100000

# For some reason, start button bit is in joystick byte.
JOY = [BTN_START, JOY_U, JOY_D, JOY_L, JOY_R]
BTN = [BTN_A, BTN_B, BTN_C, BTN_X]

JOY_MAP = {
    JOY_R: keyboard.Key.right,
    JOY_L: keyboard.Key.left,
    JOY_U: keyboard.Key.up,
    JOY_D: keyboard.Key.down,
    BTN_START: keyboard.KeyCode.from_char('1'),
}
BTN_MAP = {
    BTN_A: keyboard.Key.ctrl_l,
    BTN_B: keyboard.Key.alt_l,
    BTN_C: keyboard.Key.space,
    BTN_X: keyboard.Key.shift_l,
}

kb = [keyboard.Controller() for _ in range(5)]

class Player():

    def __init__(self, keyboard: keyboard.Controller, joy_map: dict, btn_map: dict):
        self._keyboard = keyboard
        self._prev_joystick = 0
        self._prev_button = 0
        self._joy_map = joy_map
        self._btn_map = btn_map
    
    def handle_input(self, input: bytes):
        joystick_input = input[0]
        button_input = input[1]

        joy_diff = self._prev_joystick ^ joystick_input
        for joy_code in JOY:
            if joy_code & joy_diff:
                self._keyboard.touch(self._joy_map[joy_code], bool(joy_code & joystick_input))
        btn_diff = self._prev_button ^ button_input
        for btn_code in BTN:
            if btn_code & btn_diff:
                self._keyboard.touch(self._btn_map[btn_code], bool(btn_code & button_input))

        self._prev_joystick = joystick_input
        self._prev_button = button_input

class System():

    def __init__(self, keyboard: keyboard.Controller):
        self._keyboard = keyboard
        self._prev_input = 0

    def handle_input(self, input: int):
        diff = self._prev_input ^ input

        if SYS_LIVE & diff:
            self._keyboard.touch(keyboard.Key.tab, bool(SYS_LIVE & input))
        if SYS_VOLUME & diff:
            vol = SYS_VOLUME & input
            if vol == 0b00:
                self._keyboard.tap(keyboard.Key.media_volume_down)
            elif vol == 0b10:
                self._keyboard.tap(keyboard.Key.media_volume_up)
        
        self._prev_input = input
        

system = System(kb[4])
players = [Player(kb[p], JOY_MAP, BTN_MAP) for p in range(4)]

with serial.Serial('/dev/cu.usbserial-A50285BI', 115200) as s:
    while True:
        s.write(REQUEST_BYTES)
        res = s.read(18)
        system_input = res[2]
        input = [res[4:6], res[8:10], res[12:14], res[16:18]]
        system.handle_input(system_input)
        for player, input in zip(players, input):
            player.handle_input(input)
