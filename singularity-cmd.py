import sys
import system.main

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Usage: python main.py <path to file> <path to output.format> <type of module to use ffmpeg/pillow/text")
    sys.exit(1)

try:
    arg3 = sys.argv[3]
except:
    arg3 = None

system.main.convert(sys.argv[1], sys.argv[2], arg3)