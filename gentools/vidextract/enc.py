import numpy
from scipy import ndimage

def conv_c64_hires(img):
    """Convert a 320x200 b/w image to C64 hires graphics mode memory layout"""
    idx = 0
    bmp = numpy.ndarray(shape=(320 * 200 / 8), dtype=numpy.uint8)
    for ay in xrange(0, 25):		# 25 attribute cells high
        for ax in xrange(0, 40):	# 40 attribute cells wide
            for b in xrange(0, 8):	# 8 bytes per attribute cell
                x = ax * 8
                y = ay * 8 + b
                l = list(img[y, x:x+8])	# get 8 pixels

                # Convert 8 pixels into one byte
                l = map(lambda v: 1 if v else 0, l)
                val = reduce(lambda t, v: t * 2 + v, l)

                bmp[idx] = val
                idx += 1
    return bmp

def runlength_enc(bmp):
    """Run-length encode bitmap data"""
    curval = None
    offset = 0
    dlist = []
    for idx in xrange(0, bmp.shape[0]):
        val = bmp[idx]
        if curval == val:	# same value, increment runlength count
            count += 1
        else:
            if curval != None and curval != 0:
                # Append to output list unless pixel is white (0, no bits set),
                # which the buffer will be initialized to
                dlist.append((offset, curval, count))
                
            # Init new count
            count = 1
            curval = val	# remember value
            offset = idx	# remember offset
    dlist.append((offset, curval, count))	# append last sequence
    return dlist

def runlength_sort(dlist):
    """Order RLE list data by byte value to change"""
    srle = {}
    for (off, val, cnt) in dlist:
        if not val in srle:
            srle[val] = []
        srle[val].append((off, cnt))
    return srle

def runlength_delta_enc(bmp1, bmp2):
    curval = None
    offset = 0
    dlist = []
    for idx in xrange(0, bmp1.shape[0]):
        val1 = bmp1[idx]
        val2 = bmp2[idx]
        if val1 == val2:
            if curval != None:			# segment of differences ends
                if curval != None:		# active count, write it out
                    dlist.append((offset, curval, count))
                curval = None		# nothing to count
        else:
            if curval == val2:			# same segment of differences
                count += 1
            else:				# new segment
                if curval != None:		# active count, write it ou
                    dlist.append((offset, curval, count))
                
                # Init new count
                count = 1
                curval = val2
                offset = idx

    if curval != None:
        dlist.append((offset, curval, count))       # append last sequence
    
    return dlist
