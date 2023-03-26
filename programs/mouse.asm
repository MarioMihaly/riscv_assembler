/////////////////////////////////////////////////////////////////////
// Bare minimum mouse design to draw mouse location to VGA
// without erasing previous location.
/////////////////////////////////////////////////////////////////////

        // Mouse interrupt handling
MOUSE:  LB A A0 // Read Mouse Status
        SB A 30 // Save Mouse Status to RAM (0x30)

        LB A A1 // Read Mouse X
        SB A 31 // Save Mouse X to RAM (0x31)
        SB A C1 // Send Mouse X to upper 8 LEDs

        LB B A2 // Read Mouse Y
        SB B 32 // Save Mouse Y to RAM (0x32)
        SB B C0 // Send Mouse Y to lower 8 LEDs

        SB A B0 // Send X coord to VGA
        SB B B1 // Send Y coord to VGA
        LB A 01 // Load pixel ON value
        SB A B2 // Send pixel ON value to VGA

        IDLE    // Go back to IDLE state and wait for interrupts

TIMER:  LB A E0 // Read lower 8 slide switches
        SB A D0 // Send value to 7-segment display

        IDLE    // Go back to IDLE state and wait for interrupts