import sys
from ffvideo import VideoStream
from vidextract import bwextract, enc, c64asm

infile = sys.argv[1]
outfile = sys.argv[2]
sample = int(sys.argv[3])

vs = VideoStream(infile,
                 frame_size=(320, 200),
                 frame_mode='L') # convert to grayscale

count = 0
pbmp = None
data = []
for frame in vs:
    if count % sample == 0:
        print "Processing frame..."
        count = 0
        img = bwextract.tobw(frame.ndarray())
        bmp = enc.conv_c64_hires(img)
        if pbmp != None:
            rle = enc.runlength_delta_enc(pbmp, bmp)
            srle = enc.runlength_sort(rle)
            asm = c64asm.asm_rle_frame(srle)
            data.append(asm)
        pbmp = bmp
    else:
        print "Skippin frame..."
    count += 1

with open(outfile, 'w') as f:
    f.write(data[0])
