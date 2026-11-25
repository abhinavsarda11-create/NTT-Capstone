// Box.asm - Interactive Black Box Renderer
// Student Name: Abhinav Sarda
// Roll No: 2501730089 | K = 89
// Box Specifications:
//   - Starting Row: 89 (SCREEN + 89 * 32 = 16384 + 2848 = 19232)
//   - Height: 20 rows (rows 89 through 108)
//   - Width: 16 * ((89 mod 4) + 1) = 32 pixels (2 words from left edge)

(MAIN_LOOP)
    // Poll keyboard memory map (RAM[24576])
    @KBD
    D=M
    @SET_WHITE
    D;JEQ           // If no key is pressed (KBD == 0), draw white (0)

(SET_BLACK)
    @color
    M=-1            // -1 (0xFFFF) turns all 16 pixels in a word black
    @DRAW_INIT
    0;JMP

(SET_WHITE)
    @color
    M=0             // 0 (0x0000) turns all 16 pixels in a word white

(DRAW_INIT)
    // Start address = SCREEN (16384) + 89 * 32 (2848) = 19232
    @19232
    D=A
    @addr
    M=D

    // Box height = 20 rows
    @20
    D=A
    @rows
    M=D

(DRAW_ROW)
    // Exit drawing loop once all 20 rows are updated
    @rows
    D=M
    @MAIN_LOOP
    D;JEQ

    // Paint Word 0 (columns 0..15)
    @color
    D=M
    @addr
    A=M
    M=D

    // Move 1 word right to Word 1
    @addr
    M=M+1

    // Paint Word 1 (columns 16..31)
    @color
    D=M
    @addr
    A=M
    M=D

    // Advance 31 words to reach Word 0 of the next row (1 + 31 = 32 words/row)
    @31
    D=A
    @addr
    M=M+D

    // Decrement row counter and loop
    @rows
    M=M-1
    @DRAW_ROW
    0;JMP
