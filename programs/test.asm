// This is a comment that will be removed on the first pass

MAIN:   ADD A
        SUB B
        JUMP MOUSE
        BEQ MAIN

MOUSE:  LB A A0 // Read Mouse Status
        SB A 00 // Write mouse status for Seg7
        LB A A1 // Read Mouse X
        SB A 01 // Save Mouse X to RAM
        SB A C1 // Set upper 8 LEDs
        LB A A2 // Read Mouse Y
        SB A 02 // Save Mouse Y to RAM
        SB A C0 // Set lower 8 LEDs
        RETURN  // End of Mouse interrupt function