#!/usr/bin/env python3
import argparse
import serial
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()

def send(msg, duration=0):
    print(msg)
    ser.write(f'{msg}\r\n'.encode('utf-8'));
    sleep(duration)
    ser.write(b'RELEASE\r\n');

ser = serial.Serial(args.port, 9600)

send('Button A', 0.1)
sleep(1)
send('Button A', 0.1)
sleep(1)
send('Button A', 0.1)
sleep(3)
from random import choice
try:
    while True:
        b = choice(['A','B','X','Y'])
        sleep(0.1)
        send(f'Button {b}', 0.2)
except KeyboardInterrupt:
    send('RELEASE')
    ser.close()
