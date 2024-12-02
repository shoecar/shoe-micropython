#!/bin/sh

PORT=/dev/cu.usbmodem101
# bin source: https://micropython.org/download/ESP32_GENERIC_C3/
BIN_PATH=/Users/tschukar/Dropbox/code/esp32/ESP32_GENERIC_C3-20241025-v1.24.0.bin
CHIP=esp32c3

esptool.py --chip $CHIP --port $PORT erase_flash
esptool.py --chip $CHIP --port $PORT --baud 460800 write_flash -z 0x0 $BIN_PATH

# setup WebREPL:
screen -port $PORT 115200
> import webrepl_setup
# connect at http://micropython.org/webrepl/?#192.168.42.108:8266/

# connect to file system
rshell -p $PORT -b 115200 --editor code
edit /pyboard/boot.py

MPROOT=~/Dropbox/code/micropython
PORT=/dev/cu.usbmodem101

python3 $MPROOT/micropython-1.24.0/tools/pyboard.py -d $PORT -f cp $MPROOT/my-projects/shared/boot.py :boot.py
python3 $MPROOT/micropython-1.24.0/tools/pyboard.py -d $PORT -f cp $MPROOT/my-projects/shared/main.py :main.py

mpflash() {
  port=$([ "$2" = "" ] && echo "$PORT" || echo "$2")
  python3 $MPROOT/micropython-1.24.0/tools/pyboard.py -d "$port" -f cp $MPROOT/my-projects/shared/"$1" :"$1"
  echo ""
}

mprm() {
  port=$([ "$2" = "" ] && echo "$PORT" || echo "$2")
  python3 $MPROOT/micropython-1.24.0/tools/pyboard.py -d "$port" -f rm :"$1"
  echo ""
}

mpaflash() {
  mpflash boot.py
  mpflash main.py
  mpflash umqttsimple.py
  mpflash mcuperipherals.py
}
