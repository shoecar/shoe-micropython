#!/bin/sh

DEFAULT_PORT=/dev/cu.usbmodem101
BAUD=115200
MPROOT=~/Dropbox/code/micropython

# load flash methods
. $MPROOT/scripts/mpflash.sh

mp_usb_stream() {
  port=$([ "$1" = "" ] && echo "$DEFAULT_PORT" || echo "$1")
  screen -port "$port" $BAUD
}

mp_usb_files() {
  port=$([ "$1" = "" ] && echo "$DEFAULT_PORT" || echo "$1")
  rshell -p "$port" -b $BAUD
}
