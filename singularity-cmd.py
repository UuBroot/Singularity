import sys
import system.main

if len(sys.argv) != 3:
    print("Usage: python main.py <arg1> <arg2>")
    sys.exit(1)
    
system.main.convert(sys.argv[1], sys.argv[2])
