.psx
.erroronwarning on

; ----------------         CRC AREA START               --------------------
.open "src_edit/SLPS_021.09",0x8000f800

; ------------- Disable the custom area name kerning
.org 0x80043044
	addiu a3, zero, 0x0
.org 0x80043060
	addiu a3, zero, 0x0

; ------------- Hijack a jump at end of glyph render
.definelabel jump_hijack, 0x8003eca4 

.org jump_hijack
	la v0, func_vwf
	jr v0
	nop

; ------------- Define area for VWF table and new functions

.definelabel freespace_start, 0x80010660

.org freespace_start
.area 0x770

vwf_table:
.import "vwf.bin"
.align

func_vwf:
	;vwf, t3 gets width
	
	bne t4, zero, two_byte_char	;If 2 byte char, use default width
	nop
	addiu v0, t0, -1		;t0 = &glyph
	lb v0, 0x0(v0)			;v0 = char
	la v1, vwf_table		;v1 = &vwf_table
	andi v0, v0, 0xFF
	addu v1, v1, v0			;v1 = &vwf_table[char]
	lbu	t3, 0x0(v1)			;t3 = *&vwf_table[char] = vwf_table[char]
	j end_vwf
	addiu t3, t3, 0x1		;Add 1 character of 

two_byte_char:
	li t3, 0xC				;Default glyph width
end_vwf:
	la t1,jump_hijack + 4*4	;Set return address
	lui a0, 0x1f80			;Moved instruction
	ori a0, a0, 0x48		;Moved instruction
	lw v0, 0x0(a0)			;Moved instruction
	jr t1					;RETURN
	lui v1, 0xFF			;Moved instruction

.endarea
.close