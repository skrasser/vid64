import sys
from ffvideo import VideoStream
from vidextract import bwextract, enc, c64asm

infile = sys.argv[1]
outfile = sys.argv[2]

vs = VideoStream(infile,
                 frame_size=(320, 200),
                 frame_mode='L') # convert to grayscale

frame = vs.get_frame_at_sec(0)
img = bwextract.tobw(frame.ndarray())
bmp = enc.conv_c64_hires(img)
asm = c64asm.asm_byte_frame(bmp)

with open(outfile, 'w') as f:
    f.write(asm)
