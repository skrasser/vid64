_loopidx = 0

def asm_loadval(val):
    """Assembler code to load val into accumulator"""
    return '\t\tlda #%d\n' % val	# 2 bytes, 2 cycles

def asm_setpix(off):
    """Assembler code to write accumulator into bitmap RAM"""
    return '\t\tsta bmpram+%d\n' % off	# 3 bytes, 4 cycles

def asm_setpix_len_abs(off, len):
    """Assembler code to set len bytess at offset off using absolute addressing
    Generates 3 bytes of machine code per 8 pixels
    """
    res = ''
    for i in xrange(0, len):
        res += asm_setpix(off + i)
    return res

def asm_setpix_len_idx_ff(off):
    """Assembler code to set 255 bytess using index/loop"""
    global _loopidx
    res = '''
		ldy #$00
.loop%d		sta bmpram+%d, y
		iny
		bne .loop%d
    ''' % (_loopidx, off, _loopidx)
    _loopidx += 1
    return res

def asm_setpix_len_idx(off, len):
    """Assembler code to set len bytes using index/loop (up to 254 bytes)"""
    global _loopidx
    res = ''

    # Can't optimize for offset 0, write it using absolute addressing
    if off == 0:
        res = asm_setpix(off)
        off = 1
        len -= 1

    # Decrease offset so that we can break the loop at offset 0 (saves a register),
    # i.e. len=3 writes for y=3,2,1
    res += '''
		ldy #%d			; 2 bytes, 2 cycles
.loop%d		sta bmpram+%d, y	; 3 bytes, 5 cycles
		dey			; 1 byte,  1 cycle
		bne .loop%d		; 2 bytes, 3 cycles (taken, same page)
    ''' % (len, _loopidx, off - 1, _loopidx)
    _loopidx += 1
    return res

def asm_rle_frame(slre):
    """Generate assembler code to update frame based on sorted RLE data"""
#    res = 'init_frame\n'
    res = ''
    for val in slre:
        res += asm_loadval(val)	# load value
        for (off, cnt) in slre[val]:
            if cnt > 2 and cnt <= 254:
                res += asm_setpix_len_idx(off, cnt)
            else:
                # Generates less machine code for 3 or more bytes
                res += asm_setpix_len_abs(off, cnt)
                if cnt > 254:
                    print "Warning: unoptimized sequence"
                    # TODO: if this occurs, break up into multiple loops
#    res += '\t\trts\n'
    return res

def asm_byte_frame(bmp):
    """Generate assembler code for all data bytes in bmp"""
    res = ''
    count = 0
    for b in bmp:
        if count == 0:
            res += '!byte $%02x' % b
        else:
            res += ',$%02x' % b
        count += 1
        if count == 16:
            res += '\n'
            count = 0
    return res
