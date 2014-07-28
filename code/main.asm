	;; main.asm
		sei		; disable interrupts
		lda #53
		sta $1		; switch off BASIC ROM at $a000
		jsr vicinit
loopvid
		jsr wait
		jsr frame1
		jsr wait
		jsr frame2
		jsr wait
		jsr frame3
		jsr wait
		jsr frame4
		jsr wait
		jsr frame5
		jsr wait
		jsr frame6
		jsr wait
		jsr frame7
		jsr wait
		jsr frame8
		jsr wait
		jsr frame9
		jsr wait
		jsr frame10
		jsr wait
		jsr frame11
		jsr wait
		jsr frame12
		jsr wait
		jsr frame13
		jsr wait
		jsr frame14
		jsr wait
		jsr frame15
		jmp loopvid

wait		jsr wait_frame2
		jsr wait_frame2
		jsr wait_frame2
		rts

	;; Wait for beam to reach row $ff
wait_frame	lda #$ff
.wait_frame	cmp $d012
		bne .wait_frame
		rts

	;; Wait for beam to reach and leave row $ff
wait_frame2	lda #$ff
.wait_frame2a	cmp $d012
		bne .wait_frame2a
.wait_frame2b	cmp $d012
		beq .wait_frame2b
		rts

wait_spc	lda $dc01
		cmp #$ef	; space pressed
		bne wait_spc
.rel_spc        lda $dc01
		cmp #$ff	; now wait for space being released again
	        bne .rel_spc
		rts
