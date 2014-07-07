import sys
from ffvideo import VideoStream
from vidextract import bwextract

file = sys.argv[1]

vs = VideoStream(file)
bwextract.print_info(vs)
