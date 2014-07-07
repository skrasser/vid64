	;; *** set up graphics
vicinit		jsr vicsetup
		jsr clearscreen
		rts

	;; *** set up vic for hires gfx
vicsetup	lda vic+$11 	; load vic control register 1
		ora #$20	; set bit 5
		sta vic+$11	; write back

		lda #$18	; 1: $0400, 8: $2000
		sta vic+$18	; set vic base addresses
		rts
	
	;; *** clear all pixels and colors; set border color
clearscreen	lda #$01
		sta vic+$20	; set white border
		+w_mov zbl,bmpram

	;; clear pixels from $2000 to $3f40 ($1f40 bytes)
	;; this clear to $3f00
		ldx #$00
.setpix		lda #$00
	;	jsr fillmem
		inc zbh		; increment high byte of vector (adding $100 to vector)
		inx		; increment counter
		cpx #$1f	; and check if reached $1f00 bytes
		bne .setpix
	;; till $3f40, with some overlap starting from $3e40
		ldx #$3e
		stx zbh
		ldx #$40
		stx zbl
	;	jsr fillmem
	
	;; set colors for $3e8 cells starting at $0400
		ldy #$00
		lda #$01	; 0 = black fg, 1 = white bg
.setcol		sta scrram,y
		sta scrram+$100,y
		sta scrram+$200,y
		sta scrram+$2e8,y
		iny
		bne .setcol
		rts

	;; *** Fill $ff bytes of memory referenced at zbl with accumulator
fillmem 	ldy #$00
.fillmem1	sta (zbl),y
		iny
		bne .fillmem1
		rts

	;; *** Fill x bytes of memory referenced at zbl with accumulator
fillmemn	ldy #$00
.fillmemn1	sta (zbl),y
		iny
		dex
		bne .fillmemn1
		rts
