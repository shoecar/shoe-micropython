DEFAULT_PORT = "/dev/cu.usbmodem101"
MPROOT = "/Users/tschukar/Dropbox/code/micropython"
SHARED_FILES = f"{MPROOT}/my-projects/shared/"

import argparse
import python_minifier
from pyboard import Pyboard

parser = argparse.ArgumentParser(description="Write target local file to Micropython board")
parser.add_argument("target_file", help="Target file to write to. Should not include path")
parser.add_argument("-l", "--local_file", help=f"Path to local file to write. When excluded the target file mame is used at {SHARED_FILES}")
parser.add_argument("-p", "--port", default=DEFAULT_PORT, help="USB Serial port target board is connected to")
parser.add_argument("--skip-minify", action="store_true", help="Do NOT Minify Python file contents")
args = parser.parse_args()

target_file_name = args.target_file
if not target_file_name.startswith('/'):
    target_file_name = '/' + target_file_name
local_file_name = args.local_file if args.local_file else f"{SHARED_FILES}{target_file_name}"

with open(local_file_name, "r") as file:
  local_file_content = file.read()
target_content = python_minifier.minify(local_file_content) if target_file_name.endswith(".py") and not args.skip_minify else local_file_content

print(f"Writing file '{local_file_name}' contents{" (minified)"} to '{target_file_name}' on device at port '{args.port}'")
pyb = Pyboard(args.port)
pyb.enter_raw_repl()
pyb.fs_writefile(target_file_name, target_content)

print(f"File '{target_file_name}' successfully written")
pyb.exit_raw_repl()
pyb.close()
