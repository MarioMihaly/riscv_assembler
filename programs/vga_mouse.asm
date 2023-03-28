/////////////////////////////////////////////////////////////////////
// Bare minimum design of VGA with Mouse.
/////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////
// 1. Initialise variables
            FUNC INIT_VARS // Initialise variables in RAM
            JUMP VGA_LOOP   // Draw VGA frame

/////////////////////////////////////////////////////////////////////
// Initialization of VGA X & Y
INIT_VARS:  LB A 00     // Load initial X, Y = 0
            SB A 20     // Initialise X = 0 for VGA
            SB A 21     // Initialise Y = 0 for VGA

            // Unset previous mouse status
            LB A 31 // Load last Mouse X
            LB B 32 // Load last Mouse Y
            SB A B0 // Send lst Mouse X to VGA
            SB B B1 // Send last Mouse Y to VGA
            LB A 22 // Load last pixel value at the location
            SB A B2 // Restore pixel as needed

            // Initialise Mouse Status, X and Y
            LB A 09     // Load initial MouseStatus
            SB A 30     // Initialise MouseStatus variable
            LB A 0A     // Load initial MouseX
            SB A 31     // Initialise MouseX variable
            SB A C1     // Set upper 8 LEDs
            LB A 0B     // Load initial MouseY
            SB A 32     // Initialise MouseY variable
            SB A C0     // Set lower 8 LEDs

            RETURN

/////////////////////////////////////////////////////////////////////
// VGA Frame drawing
VGA_LOOP:   FUNC CHECK_X        // Check X coord and set it if needed.
RETURN_X:   FUNC CHECK_Y        // Check Y coord and set it if needed.
RETURN_Y:   FUNC CHECK_X_LIMIT  // Check X limit reached and increment X.
            JUMP VGA_LOOP       // Do next X check.
VGA_DONE:   IDLE          // When VGA setup is done, wait for interrupts

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
                JUMP VGA_LOOP

SET_PIXEL_X:    LB A 01     // Load pixel ON value.
                SB A B2     // Send pixel value to VGA.
                JUMP RETURN_X

SET_PIXEL_Y:    LB A 01     // Load pixel ON value.
                SB A B2     // Send pixel value to VGA.
                JUMP RETURN_Y

/////////////////////////////////////////////////////////////////////
// 2. Define Mouse interrupt handling -> copy over content of mouse.asm
MOUSE:  LB A 31 // Load last Mouse X
        LB B 32 // Load last Mouse Y
        SB A B0 // Send lst Mouse X to VGA
        SB B B1 // Send last Mouse Y to VGA

        LB A 22 // Load last pixel value at the location
        SB A B2 // Restore pixel as needed

        LB A A0 // Read Mouse Status
        SB A 30 // Save Mouse Status to RAM (0x30)

        LB A A1 // Read Mouse X
        SB A 31 // Save Mouse X to RAM (0x31)
        SB A C1 // Send Mouse X to upper 8 LEDs

        LB B A2 // Read Mouse Y
        SB B 32 // Save Mouse Y to RAM (0x32)
        SB B C0 // Send Mouse Y to lower 8 LEDs

        SB A B0 // Send X coord to VGA
        SB B B1 // Send Y coord to VGA

        // Save original pixel value 
        LB A B2 // Get current pixel value
        SB A 22 // Store it in VGA variable region

        // Turn ON location
        LB A 01 // Load pixel ON value
        SB A B2 // Send pixel ON value to VGA

        IDLE    // Go back to IDLE state and wait for interrupts

/////////////////////////////////////////////////////////////////////
// 3. Define Timer interrupt handling
TIMER:  LB A E0 // Read lower 8 slide switches
        SB A D0 // Send value to 7-segment display

        IDLE

//        // Reload VGA frame
//        // Reset variables for X and Y
//        LB A 00     // Load initial X, Y = 0
//        SB A 20     // Initialise X = 0 for VGA
//        SB A 21     // Initialise Y = 0 for VGA
//
//        JUMP VGA_LOOP // Reset VGA frame

        // At the end of the VGA_LOOP we already go back to IDLE