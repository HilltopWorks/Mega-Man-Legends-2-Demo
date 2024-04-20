.psx
.erroronwarning on

.definelabel overlay_ID, 	0x800e0000 ;Byte
.definelabel overlay_start, 0x800e0000 
;Area 1
scene23_ID 		equ 0x1B
scene23_start 	equ 0x15810
;Area 2
scene24_ID 		equ 0x1C
scene24_start 	equ 0x12850
;Area 3
scene25_ID 		equ 0x1D
scene25_start 	equ 0x1CAE0

; ------------- Define area for VWF table and new functions
.definelabel freespace_text_1_start, 0x80010660		;vwf table and code
freespace_text_1_size equ 0x2a8

.definelabel freespace_text_2_start, 0x8001091C
freespace_text_2_size equ 0x4BC

.definelabel freespace_library_start, 0x80065B5C	;ST23, 24
freespace_library_size equ 0xFE0

;.open "unpack_edit/DAT/ST23T/ST23T-0x00000000-1.bin", 0x800e0000
;.org overlay_start + scene23_start
.open "src_edit/SLPS_021.09",0x8000f800

.org freespace_library_start
.area freespace_library_size
S23_sub:
.import "ST23T_sub.bin"
.align 4
S23_scripting:
.import "ST23T_scripting.bin"
.align 4

;.close

;.open "unpack_edit/DAT/ST24T/ST24T-0x00000000-1.bin", 0x800e0000
;.org overlay_start + scene24_start
S24_sub:
.import "ST24T_sub.bin"
.align 4
S24_scripting:
.import "ST24T_scripting.bin"
.align 4
.endarea
.close

.open "unpack_edit/DAT/ST25T/ST25T-0x00000000-1.bin", 0x800e0000
.org overlay_start + scene25_start
S25_sub:
.import "ST25T_sub.bin"
.align 4
S25_scripting:
.import "ST25T_scripting.bin"
.align 4
.close

; ----------------                 --------------------
.open "src_edit/SLPS_021.09",0x8000f800

; ------------- Default furigana to off
.org 0x80012b28
	sw zero, 0x34(v0) 


; ------------- Subtitle scenes

.definelabel voice_hijack, 0x8003decc
.definelabel text_render, 0x8003e640

.org voice_hijack
	jal func_voice_sub
	nop

;----------------------------------------------------------------------------------

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




;Skip clearing space after EXE
.org 0x8004f32c
nop


; --------------- New code area


.org freespace_text_1_start
.area freespace_text_1_size

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

;-------------------.endarea

.definelabel render_text, 	0x8003dee4	;render_text(int position, void* pTextBlock, int line_id, int kerning)
											;position & 0x3FF  => X
											;(position >> 10) & 0x1FF => Y
											;kerning should be 0
.definelabel set_text, 		0x8003d9ec	;set_text(int state_variable, void* pTextBlock, int line_id)

.definelabel voice_active, 	0x80070a58	;Byte
.definelabel scene_state,	0x80070a59	;4 bytes
.definelabel progress_timer,0x80070a74	;Int

;.org freespace_2_start
;.area freespace_2_size

func_voice_sub:
	;housekeeping
	addiu sp, sp, -4
	sw ra, 0x0(sp)
	
	;do the function we hijacked
	jal text_render			
	nop

	;--START--;
	;___if (!voice active) return
	la v0, voice_active
	lbu v0, 0x0(v0)
	nop
	beq v0, zero, voice_return
	nop
	
	;___if current_overlay not in voice_overlays, return
	la t0, overlay_ID
	lbu t0, 0x0(t0)
	li t1, scene23_ID
	beq t0, t1, execute_area_1
	nop
	li t1, scene24_ID
	beq t0, t1, execute_area_2
	nop
	li t1, scene25_ID
	beq t0, t1, execute_area_3
	nop
	j voice_return ;Not in the 3 areas
	nop

execute_area_1:
	;Get current scene state, compare to all scripting
	la t6, S23_sub
	la t7, S23_scripting
	j perform_subtitle
	nop
execute_area_2:
	la t6, S24_sub
	la t7, S24_scripting
	j perform_subtitle
	nop
execute_area_3:
	la t6, S25_sub
	la t7, S25_scripting
	j perform_subtitle
	nop

perform_subtitle:
	;t6 holds text block start
	;t7 holds scripting block start

	;if current_state in scripted_subs:
	;	set_text(0, pTextBlock, correct_index)
	;else:
	;	return
	la a2, scene_state
	lbu t0, 0x0(a2);t0 gets scene state
	lbu t1, 0x1(a2) 
	lbu t2, 0x2(a2)
	lbu t3, 0x3(a2)
	sll t1, t1, 0x8
	sll t2, t2, 0x10
	sll t3, t3, 0x18
	addu t0, t1
	addu t0, t2
	addu t0, t3

	addiu a3, t7,   0 	;a3 is script block ptr
	addiu t5, zero, 0 	;t5 is index cursor

script_check_loop_head:
	lw a2, 0x0(a3)	;a2 gets next check block
	la v0, 0xFFFFFFFF
	beq a2, v0, voice_return	;Return if FFFFFFFF terminator reached
	nop
	beq a2, t0, check_timer	;goto check_timer if match
	nop
	addiu t5, t5, 1		;Increment index counter
	j script_check_loop_head
	addiu a3, a3, 0x8	;Increment scripting block ptr

check_timer:
	;if current_time == target_time:
	;	goto print
	;else:
	;	continue
	lw t4, 0x4(a3)	;t4 gets target time
	la t3, progress_timer
	lw t3, 0x0(t3)	;t3 gets current_time
	nop
	beq t3, t4, print_subtitle
	nop
	addiu a3, a3, 0x8
	j script_check_loop_head
	addiu t5, t5, 1		;Increment index counter

	;t6 holds pTextBlock
	;t5 holds index
print_subtitle:
	;set_text(0, void* pTextBlock, int index)
	addiu a1, t6, 0x0
	addiu a2, t5, 0x0
	jal set_text
	addiu a0, zero, -1

	;return
voice_return:
	lw ra, 0x0(sp)
	nop
	jr ra
	addiu sp, sp, 4
.endarea

; ---------- Secret level code
.definelabel set_level_hijack, 0x800b0958 
.definelabel mem_audio_volume, 0x80070b40
.definelabel mem_level_ID, 0x8008AAE8
.definelabel mem_furigana_flag, 0x8008ab0c

secret_level_ID equ 0x7
level_4 equ 0x23		;Breaks if loading this level

.org freespace_text_2_start
.area freespace_text_2_size
; ---
secret_level_check:
	;v0 has level ID
	;s2 has mem_level_ID - 0x10
	
	;if furigana_flag == False:
	;	return
	la v1, mem_furigana_flag
	lb v1, 0x0(v1)
	nop
	beq v1, zero, secret_level_return
	nop
	
	;if next_level == level_4:
	;	return
	li v1, level_4
	beq v1, v0, secret_level_return
	nop

	;set_audio(VOLUME_OFF)
	la v1, mem_audio_volume
	sh zero, 0x0(v1)

	;set_level(secret_level_ID)
	li v0, secret_level_ID

secret_level_return:
	sb v0, 0x10(s2) ;Restored instruction
	jr ra
	lui v0, 0x800b	;Restored instruction

.endarea
.close

;------------------------ DEMO

.open "unpack_edit/DAT/DEMO/DEMO-0x00000000-1.bin", 0x800b0000

.org set_level_hijack
	jal secret_level_check
	nop


;Move and expand select title elements
.org 0x800B1700
	ori a2, a2, 0x18	;1st box X
.org 0x800B1710
	ori t0, t0, 0x118
.org 0x800b1720
	ori t3, t3, 0x218
.org 0x800b1730
	ori t1, t1, 0x5C	;3rd box width


.close
