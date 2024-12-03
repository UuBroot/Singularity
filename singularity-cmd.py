import sys
import system.main

if len(sys.argv) != 3:
    print("Usage: python main.py <path to file> <path to output.format>")
    sys.exit(1)
    
system.main.convert(sys.argv[1], sys.argv[2])
