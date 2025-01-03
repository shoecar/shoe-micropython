#!/bin/sh

PORT=/dev/cu.usbmodem101
MPROOT=~/Dropbox/code/micropython

####################
# Initial Board Setup

# ESP32C3 bin source from: https://micropython.org/download/ESP32_GENERIC_C3/
BIN_PATH=$MPROOT/official/board-bins/ESP32_GENERIC_C3-20241025-v1.24.0.bin
CHIP=esp32c3 # set to board type matching .bin

esptool.py --chip $CHIP --port $PORT erase_flash
esptool.py --chip $CHIP --port $PORT --baud 460800 write_flash -z 0x0 $BIN_PATH


##############
# Flash Shared

# register bash methods
. $MPROOT/scripts/all.sh
# run run flash all (make sure to redefine DEFAULT_PORT first, if needed)
mp_all_flash

##################
# Connect to Board

# serial connect to REPL (aka: mp_usb_stream):
screen -port $PORT 115200

# setup webrepl in Python REPL:
# >>> import webrepl_setup
# connect at http://micropython.org/webrepl/?#192.168.42.108:8266/ (update IP)

# serial connect to file system (aka: mp_usb_files):
rshell -p $PORT -b 115200 --editor code

# >>> ls ls /pyboard
# >>> edit /pyboard/boot.py
