from ffvideo import VideoStream
import numpy
from scipy import ndimage

def print_info(vs):
    print "codec: %s" % vs.codec_name
    print "duration: %.2f" % vs.duration
    print "frame rate: %d" % vs.framerate
    print "bit rate: %d" % vs.bitrate
    print "frame size: %dx%d" % (vs.frame_width, vs.frame_height)
    print "frame mode: %s" % vs.frame_mode

def tobw(img, threshold=95):
    """Convert grayscale image to b/w"""
    bi = img <= threshold
    bi_cl = ndimage.binary_closing(bi)
    bi_op = ndimage.binary_opening(bi_cl)
    return bi_op

def analyze_diff(img1, img2):
    """Count different pixels between two monochrome images"""
    count_b2w = 0 # blk in 1, wht in 2
    count_w2b = 0 # wht in 1, blk in 2
    for (y,x), val1 in numpy.ndenumerate(img1):
        val2 = img2[y,x]
        if val1 == False and val2 == True:
            count_b2w += 1
        elif val1 == True and val2 == False:
            count_w2b += 1
    return count_b2w, count_w2b

def viz_diff(img1, img2):
    """Visualize the differences between monochrome images img1 and img2"""
    (y, x) = img1.shape
    dimg = numpy.ndarray(shape=(y, x, 3), dtype=numpy.uint8)
    for (y,x), val1 in numpy.ndenumerate(img1):
        val2 = img2[y,x]
        if val1 == val2:
            if val1:	# both white
                dimg[y,x] = (255, 255, 255)
            else:	# both black
                dimg[y,x] = (0, 0, 0)
        elif val1:	# white to black
            dimg[y,x] = (255, 0, 0)	# show as red
        else:		# black to white
            dimg[y,x] = (0, 0, 255)	# show as blue
    return dimg

