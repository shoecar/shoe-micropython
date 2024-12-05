#!/bin/sh

DEFAULT_PORT=/dev/cu.usbmodem101

MPROOT=~/Dropbox/code/micropython
MICROPYTHON=$MPROOT/official/micropython-1.24.0

SHARED_FILES=$MPROOT/my-projects/shared/

mp_flash() {
  if [ "$1" = "" ]; then
    echo "INVALID: must specify file to flash"
    return
  fi

  target_file=$([ "$2" = "" ] && echo $SHARED_FILES/"$1" || echo "$2")
  python $MICROPYTHON/tools/pyboard.py -d "$DEFAULT_PORT" -f cp "$target_file" :"$1"
}

mp_write() {
  if [ "$1" = "" ]; then
    echo "INVALID: must specify file to flash"
    return
  fi

  target_file=$([ "$2" = "" ] && echo $SHARED_FILES/"$1" || echo "$2")
  extension="${target_file##*.}"

  if [ "$extension" = "py" ]  && [ -x "$(command -v pyminify)" ]; then
    temp_file=tmp-minified_$(basename "$target_file")
    echo "Creating temp $temp_file storing minified: $(basename "$target_file")"
    pyminify "$target_file" > "$temp_file"

    python $MICROPYTHON/tools/pyboard.py -d "$DEFAULT_PORT" -f cp "$temp_file" :"$1"

    echo "Removing $temp_file"
    rm "$temp_file"
  else
    python $MICROPYTHON/tools/pyboard.py -d "$DEFAULT_PORT" -f cp "$target_file" :"$1"
  fi
}

mp_rm() {
  if [ "$1" = "" ]; then
    echo "INVALID: must specify file to remove"
    return
  fi

  python $MICROPYTHON/tools/pyboard.py -d "$DEFAULT_PORT" -f rm :"$1"
}

mp_all_flash() {
  target_project=$([ "$1" = "" ] && echo "$SHARED_FILES" || echo "$1")

  mp_write boot.py "$target_project"/boot.py
  mp_write main.py "$target_project"/main.py
  mp_write mcuconfig.py "$target_project"/main.py
  mp_write secrets.py
  mp_write umqttsimple.py
  mp_write mcuperipherals.py
}
