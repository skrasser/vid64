import sys
from ffvideo import VideoStream
from vidextract import bwextract, enc, c64asm

infile = sys.argv[1]
outfile = sys.argv[2]
sample = int(sys.argv[3])	# take every sample-th frame
max_frames = int(sys.argv[4])	# cut off after this many frames

vs = VideoStream(infile,
                 frame_size=(320, 200),
                 frame_mode='L') # convert to grayscale


# Compute deltas between pairs of frames
count = 0
pbmp = None
data = []
count_frames = 0
for frame in vs:
    if count % sample == 0 and count_frames < max_frames:
        print "Processing frame..."
        if pbmp == None:
            print "Initial frame, no output"
        count = 0
        count_frames += 1
        img = bwextract.tobw(frame.ndarray())
        bmp = enc.conv_c64_hires(img)
        if pbmp != None:
            rle = enc.runlength_delta_enc(pbmp, bmp)
            srle = enc.runlength_sort(rle)
            asm = c64asm.asm_rle_frame(srle)
            data.append(asm)
        else:
            # Remember the first frame
            firstbmp = bmp
        pbmp = bmp
    else:
        print "Skipping frame..."
    count += 1

# Compute delta between last frame and first frame so we can loop the video
rle = enc.runlength_delta_enc(bmp, firstbmp)
srle = enc.runlength_sort(rle)
asm = c64asm.asm_rle_frame(srle)
data.append(asm)

num_frame = 0
with open(outfile, 'w') as f:
    for frdata in data:
        num_frame += 1
        f.write('frame%d\n' % num_frame)
        f.write(frdata)
        f.write('rts\n')
