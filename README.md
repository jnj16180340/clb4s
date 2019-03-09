# clb4s
[![Thumbnail](https://i.imgur.com/crap.jpg)](https://goatse.cx))

## Hardware
- Arduino Uno, remove the atmega328p chip
- FTDI TTYUSB interface
- Remember the atmega16u2 is talking *to* the chip whose pins are exposed.
 - So RX->RX, TX->TX
- `make`
- quick reset to enter programming mode
- `dfu-programmer atmega16u2 erase`
- `dfu-programmer atmega16u2 flash Joystick.hex`
- `dfu-programmer reset`
- Serial is recommended to stay at 9600 per LUFA?

### Refs
[NintendoSwitchをPCから操作する - おいら屋ファクトリー](https://blog.feelmy.net/control-nintendo-switch-from-computer/)(in Japanese)

