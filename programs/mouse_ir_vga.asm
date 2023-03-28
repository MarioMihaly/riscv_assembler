/////////////////////////////////////////////////////////////////////
// Bare minimum design of VGA with Mouse and IR.
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
VGA_DONE:   IDLE                // When VGA setup is done, wait for interrupts

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
// IR packet generation
IR:     LB A 00         // Load clear packet value
        SB A 40         // Reset packet in RAM
        JUMP CHECK_F   // Check going forward

        // At this point packet is generated
SEND_IR:LB A 40         // Load finished packet
        SB A 90         // Send packet to IR

        RETURN

// Check for FORWARD
CHECK_F:LB A 32         // Load current MouseY
        LB B 07         // Load 1st Y bar (39)
        BGT CHECK_B     // if Y > 39 check backward
        
        // Only enter here if in FORWARD region
        LB A 40         // Load packet
        LB B 01         // Load forward mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP CHECK_L

// Check BACKWARD
CHECK_B:LB A 32         // Load current MouseY
        LB B 08         // Load 2nd Y bar (80)
        BLT CHECK_L     // if Y < 80 check LEFT
        
        // Only enter here if in BACKWARD region
        LB A 40         // Load packet
        LB B 0C         // Load backward mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP CHECK_L

// Check LEFT
CHECK_L:LB A 31         // Load current MouseX
        LB B 05         // Load 1st X bar (52)
        BGT CHECK_R     // If X > 52 check right

        // Only enter here if turning left
        LB A 40         // Load packet
        LB B 0D         // Load left mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP SEND_IR    // End of packet generation as turning is exlusive

// Check RIGHT
CHECK_R:LB A 31         // Load current MouseX
        LB B 06         // Load 2nd X bar (107)
        BLT SEND_IR     // If X < 107 done generating packet

        // Only enter here if turning right
        LB A 40         // Load packet
        LB B 0E         // Load right mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP SEND_IR    // End of packet generation


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

        // Generate IR packet
        //FUNC IR

        IDLE    // Go back to IDLE state and wait for interrupts

/////////////////////////////////////////////////////////////////////
// 3. Define Timer interrupt handling
TIMER:  FUNC IR

        //LB A 40 // Read IR packet
        LB A 01
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