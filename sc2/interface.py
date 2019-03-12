# Microcontroller does it like
# char t[8];
# char c[16];
# sscanf(line, "%s %s", t, c);

from os import getenv
from time import sleep
from serial import Serial
from time import sleep 

DEFAULT_PORT='/dev/ttyUSB0'
PORT = getenv('SER_CONTROLLER', DEFAULT_PORT)

class BadButtonError(Exception):
    pass

class SwitchController():
    def __init__(self, port=PORT, boc=False):
        self.port = port
        self.baudrate = 9600
        self.boc = False
        self.ser = None

    valid_buttons = {"A",
                     "B",
                     "X",
                     "Y",
                     "L",
                     "R",
                     "ZL",
                     "ZR",
                     "SELECT",
                     "START",
                     "LCLICK",
                     "RCLICK",
                     "HOME",
                     "CAPTURE",
                     "RELEASE"}

    valid_sticks = {"LX",
                    "LY",
                    "RX",
                    "RY"}

    valid_stick_positions = {"MIN",     # 0
                             "CENTER",  # 128
                             "MAX"}     # 255

    valid_hat_positions = {"TOP",
                           "TOP_RIGHT",
                           "RIGHT",
                           "BOTTOM_RIGHT",
                           "BOTTOM",
                           "BOTTOM_LEFT",
                           "LEFT",
                           "TOP_LEFT",
                           "CENTER"}

    def block_on_connect(self): 
        p = Path(self.port)
        elapsed = float(0)
        while not p.exists():
            print(f'Waiting {elapsed}s for controller on {self.port}...')
            sleep(0.25)
        print('...Got it!') 
        return str(p)

    def __enter__(self):
        if self.boc:
            block_on_connect()
        #print(f'Opening {self.port}')
        self.ser = Serial(self.port, self.baudrate)
        return self

    def __exit__(self, *args):
        #print(f'Closing {self.port}')
        self.ser.close()

    @staticmethod
    def fcmd(msg):
        return f'{msg}\r\n'.encode('utf-8')

    def send(self, cmd, dur=0.1, rel=True):
        self.ser.write(self.fcmd(cmd))
        sleep(dur)
        if rel:
            self.ser.write(b'RELEASE\r\n')

    def release(self, **kwargs):
        self.send('RELEASE', **kwargs)

    def button(self, b, **kwargs):
        if b not in self.valid_buttons:
            raise BadButtonError(b)
        self.send(f'Button {b}', **kwargs)

    def stick(self, s, p, **kwargs):
        if s not in self.valid_sticks:
            raise BadButtonException
        if p not in self.valid_stick_positions:
            raise BadButtonError(s, p)
        self.send(f'{s} {p}', **kwargs)

    def hat(self, p, **kwargs):
        if p not in self.valid_hat_positions:
            raise BadButtonError(p)
        self.send(f'HAT {p}', **kwargs)

