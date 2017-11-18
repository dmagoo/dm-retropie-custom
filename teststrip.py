import sys
import signal
from Matrix import Matrix

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    matrix.clearStrip().strip.show()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

matrix = Matrix(32,8)
matrix.test()
