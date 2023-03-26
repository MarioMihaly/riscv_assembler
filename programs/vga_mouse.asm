/////////////////////////////////////////////////////////////////////
// Bare minimum design of VGA with Mouse.
/////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////
// 1. Lets draw the VGA frame -> copy over content of vga.asm
VGA_LOOP:   FUNC INIT_VARS   // Initialise variables in RAM
            // At this point X and Y are initialized to 0
            // Start looping through X
NEXT_CHECK: FUNC CHECK_X          // Check X coord and set it if needed.
RETURN_X:   FUNC CHECK_Y          // Check Y coord and set it if needed.
RETURN_Y:   FUNC CHECK_X_LIMIT  // Check X limit reached and increment X.
            JUMP NEXT_CHECK     // Do next X check.
VGA_DONE:   IDLE                // When VGA setup is done, wait for interrupts

            // Initialization of VGA X & Y
INIT_VARS:  LB A 00     // Load initial X, Y = 0
            SB A 20     // Initialise X = 0 for VGA
            SB A 21     // Initialise Y = 0 for VGA

            // Initialise Mouse Status, X and Y
            LB A 09     // Load initial MouseStatus
            SB A 30     // Initialise MouseStatus variable
            LB A 0A     // Load initial MouseX
            SB A 31     // Initialise MouseX variable
            LB A 0B     // Load initial MouseY
            SB A 32     // Initialise MouseY variable

            RETURN

CHECK_X:    LB A 20     // Load current X coord
            LB B 05     // Load first X-bar coord
            BEQ SET_PIXEL_X
            LB B 06     // Load second X-bar coord
            BEQ SET_PIXEL_X
            RETURN

CHECK_Y:    LB A 21     // Load current Y coord
            LB B 07     // Load first Y-bar coord
            BEQ SET_PIXEL_Y
            LB B 08     // Load second Y-bar coord
            BEQ SET_PIXEL_Y
            RETURN
    
CHECK_X_LIMIT:  LB A 20             // Load current X coord
                LB B 03             // Load X limit
                BGT CHECK_Y_LIMIT   // Branch if X out of limit
                INC A A             // Increment X
                SB A 20             // Update X coordinate
                SB A B0             // Send new X coordinate to VGA
                RETURN

CHECK_Y_LIMIT:  LB A 00         // Load 0 into register
                SB A 20         // Reset X to 0
                SB A B0         // Send new X coordinate to VGA
                LB A 21         // Load current Y coord
                LB B 04         // Load Y limit
                BGT VGA_DONE    // Frame is done at this point
                INC A A         // Increment Y
                SB A 21         // Update Y coordinate
                SB A B1         // Send new Y coordinate to VGA
                JUMP NEXT_CHECK

SET_PIXEL_X:    LB A 01     // Load pixel ON value.
                SB A B2     // Send pixel value to VGA.
                JUMP RETURN_X

SET_PIXEL_Y:    LB A 01     // Load pixel ON value.
                SB A B2     // Send pixel value to VGA.
                JUMP RETURN_Y

/////////////////////////////////////////////////////////////////////
// 2. Define Mouse interrupt handling -> copy over content of mouse.asm
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

/////////////////////////////////////////////////////////////////////
// 3. Define Timer interrupt handling
TIMER:  LB A E0 // Read lower 8 slide switches
        SB A D0 // Send value to 7-segment display

        IDLE    // Go back to IDLE state and wait for interrupts