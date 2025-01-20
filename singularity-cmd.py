import sys
import os
from system.main import Main

system = Main()

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Usage: python main.py <path to file> <path to output.format> <type of module to use ffmpeg/pillow/text")
    sys.exit(1)

try:
    arg3 = sys.argv[3]
except:
    arg3 = None

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

system.convert(input_file, output_file, arg3)