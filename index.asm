!cpu 6502
!to "build/vid64.prg",cbm    ; output file

	;; BASIC loader

* = $0801				; BASIC start address (#2049)
!byte $0d,$08,$dc,$07,$9e,$20,$34,$39	; BASIC loader to start at $c000...
!byte $31,$35,$32,$00,$00,$00		; puts BASIC line 2012 SYS 49152
* = $c000				; start address for 6502 code

!source "code/macro.asm"
!source "code/mem.asm"
!source "code/main.asm"
!source "code/vicinit.asm"

; * = $4000
; !source "build_asm/frame_init.asm"
* = $2000
!source "build/gen/frame_init.asm"
dummy
!source "foo2.asm"
rts
dummy2