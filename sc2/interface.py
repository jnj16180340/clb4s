# Microcontroller does it like
# char t[8];
# char c[16];
# sscanf(line, "%s %s", t, c);

from os import getenv
from time import sleep
# ser = serial.Serial(args.port, 9600)
from time import sleep 

DEFAULT_PORT='/dev/ttyUSB0'
PORT = getenv('SER_CONTROLLER', DEFAULT_PORT)

class BadButtonError(Exception):
    print('Invalid controller command!')

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

    valid_hat_positions = {"TOP"
                           "TOP_RIGHT"
                           "RIGHT"
                           "BOTTOM_RIGHT"
                           "BOTTOM"
                           "BOTTOM_LEFT"
                           "LEFT"
                           "TOP_LEFT"
                           "CENTER"}

    def block_on_connect(port='/dev/ttyUSB0'): 
        p = Path(port)
        elapsed = 0
        while not p.exists():
            print(f'Waiting {elapsed}s for controller on {port}...')
            sleep(0.25)
        print('...Got it!') 
        return str(p)

    def __enter__():
        if self.boc:
            block_on_connect()
        print(f'Opening {self.port}')
        self.ser = serial.Serial(self.port, self.baudrate)
        ser.clear_input_buffer()
        ser.clear_output_buffer()
        return ser

    def __exit__(self, *args):
        print(f'Closing {self.port}')
        self.ser.close()

    @classmethod
    def fcmd(msg):
        return f'{msg}\r\n'.encode('utf-8')

    def send(self, cmd, dur=0.1, rel=True):
        self.ser.write(format_command(cmd))
        sleep(dur)
        if rel:
            self.ser.write(b'RELEASE\r\n')

    def release(self, **kwargs):
        send(fcmd('RELEASE'), **kwargs)

    def button(self, b, **kwargs):
        if b not in valid_buttons:
            raise BadButtonError(b)
        send(fcmd(f'Button {b}'))

    def stick(s, p, **kwargs):
        if s not in valid_sticks:
            raise BadButtonException
        if p not in valid_stick_positions:
            raise BadButtonError(s, p)
        send(fcmd(f'{s} {p}'), **kwargs)

    def hat(p, **kwargs):
        if p not in valid_hat_positions:
            raise BadButtonError(p)
        send(fcmd(f'HAT {p}'), **kwargs)

