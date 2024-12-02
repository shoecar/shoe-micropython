#!/bin/sh

DEFAULT_PORT=/dev/cu.usbmodem101

MPROOT=~/Dropbox/code/micropython
MICROPYTHON=$MPROOT/offical/micropython-1.24.0

SHARED_FILES=$MPROOT/my-projects/shared/

mp_flash() {
  if [ "$1" = "" ]; then
    echo "INVALID: must specify file to flash"
    return
  fi

  target_file=$([ "$2" = "" ] && echo $SHARED_FILES/"$1" || echo "$2")
  python3 $MICROPYTHON/tools/pyboard.py -d "$DEFAULT_PORT" -f cp "$target_file" :"$1"
}

mp_rm() {
  if [ "$1" = "" ]; then
    echo "INVALID: must specify file to remove"
    return
  fi

  python3 $MICROPYTHON/tools/pyboard.py -d "$DEFAULT_PORT" -f rm :"$1"
}

mp_all_flash() {
  target_project=$([ "$1" = "" ] && echo "$SHARED_FILES" || echo "$1")

  mp_flash boot.py "$target_project"/boot.py
  mp_flash main.py "$target_project"/main.py
  mp_flash mcuconfig.py "$target_project"/main.py
  mp_flash secrets.py
  mp_flash umqttsimple.py
  mp_flash mcuperipherals.py
}
