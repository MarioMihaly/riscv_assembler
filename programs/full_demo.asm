/////////////////////////////////////////////////////////////////////
// Initial design for full demonstration with pixel design for the
// VGA. The design uses the FULL_DEMO_RAM.mem file.
/////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////
// Variable initialization

        // Initialization of VGA X & Y
        LB A 00         // Load initial X, Y = 0
        SB A 20         // Initialise X = 0 for VGA
        SB A 21         // Initialise Y = 0 for VGA
        SB A 40         // IR initial packet is also 0

        // Unset previous mouse status
        LB A 31         // Load last Mouse X
        LB B 32         // Load last Mouse Y
        SB A B0         // Send last Mouse X to VGA
        SB B B1         // Send last Mouse Y to VGA
        LB A 22         // Load last pixel value at the location
        SB A B2         // Restore pixel as needed

        // Initialise Mouse Status, X and Y
        LB A 09         // Load initial MouseStatus
        SB A 30         // Initialise MouseStatus variable
        LB A 0A         // Load initial MouseX
        SB A 31         // Initialise MouseX variable
        SB A C1         // Set upper 8 LEDs
        LB B 0B         // Load initial MouseY
        SB B 32         // Initialise MouseY variable
        SB B C0         // Set lower 8 LEDs

        // Show mouse pixel in the middle
        SB A B0         // Send initial MouseX to VGA
        SB B B1         // Send initial MouseY to VGA
        LB A B2         // Load current pixel value at location
        SB A 22         // Save value in RAM for turning it back on later.
        NOT A           // Invert pixel value
        SB A B2         // Send inverted pixel value to VGA

        IDLE            // End of variable initialisation, go to IDLE and 
                        // wait for interrupts.

/////////////////////////////////////////////////////////////////////
// IR packet generation

IR:     LB A 00         // Load clear packet value
        SB A 40         // Reset packet in RAM
        JUMP CHECK_F    // Check going forward

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
        LB B 0F         // Load forward mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP CHECK_L

// Check BACKWARD
CHECK_B:LB A 32         // Load current MouseY
        LB B 08         // Load 2nd Y bar (80)
        BLT CHECK_L     // if Y < 80 check LEFT
        
        // Only enter here if in BACKWARD region
        LB A 40         // Load packet
        LB B 0E         // Load backward mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP CHECK_L

// Check LEFT
CHECK_L:LB A 31         // Load current MouseX
        LB B 05         // Load 1st X bar (52)
        BGT CHECK_R     // If X > 52 check right

        // Only enter here if turning left
        LB A 40         // Load packet
        LB B 10         // Load left mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP SEND_IR    // End of packet generation as turning is exlusive

// Check RIGHT
CHECK_R:LB A 31         // Load current MouseX
        LB B 06         // Load 2nd X bar (107)
        BLT SEND_IR     // If X < 107 done generating packet

        // Only enter here if turning right
        LB A 40         // Load packet
        LB B 0D         // Load right mask
        XOR A           // Apply mask
        SB A 40         // Save updated packet

        JUMP SEND_IR    // End of packet generation

/////////////////////////////////////////////////////////////////////
// 7-segment strobing and packet generation

        // Reset 7-segment packet
SEG7:   LB A 00         // Load packet reset value
        SB A 50         // Clear 7-segment packet in RAM
        
        // Check for strobing count reached
        LB A 51         // Load current count
        LB B 02         // Load strobing limit (4)
        BLT SKIP        // Skip resetting count
        LB A 00         // Load 0 to reset count
        SB A 51         // Save new count

        // At this point register A holds the count

        // Add Segment Select to packet
SKIP:   LB B 11         // Load Segment Select mask base address
        ADD B           // Add offset (count) to base address
        DEREF B         // Dereference address to get mask
        LB A 50         // Load 7-segment packet
        OR A            // Apply mask to set which segment to display
        SB A 50         // Save packet back to RAM

        // Get command mask
        LB A 51         // Load current count
        LB B 0C         // Load IR command mask base address
        ADD B           // Add offset (count) to base address
        DEREF B         // Dereference address to get mask
        LB A 40         // Load current IR packet
        AND A           // Extract command bit status for segment
        LB B 00         // Load 0 to compare to
        BEQ OFF         // If command is not set leave it turned OFF

        // Only enterred if the command for the current segment is asserted.
        
        // Add letter to the packet
        LB A 51         // Load current count
        LB B 16         // Load letter base address
        ADD B           // Add offset (count) to base address
        DEREF B         // Dereference address to get letter
        LB A 50         // Load 7-segment packet
        OR A            // Add letter to packet

        // At this point register A holds the final packet
SEND_7: SB A D0         // Send packet to 7-segment display
        LB A 51         // Load current count
        INC A A         // Increment count
        SB A 51         // Save incremented count
        
        RETURN          // End of 7-segment display, resume operation.

        // Add OFF letter to 7-segment packet
OFF:    LB A 50         // Load packet
        LB B 1B         // Load OFF letter
        OR A            // Add letter to packet
        
        // At this point register A holds the final packet
        JUMP SEND_7

/////////////////////////////////////////////////////////////////////
// Define Mouse interrupt handling

        // Turn off last Mouse location pixel
MOUSE:  LB A 31         // Load last Mouse X
        LB B 32         // Load last Mouse Y
        SB A B0         // Send last Mouse X to VGA
        SB B B1         // Send last Mouse Y to VGA
        LB A 22         // Load last pixel value at the location
        SB A B2         // Restore pixel as needed

        // Update MouseStatus in RAM
        LB A A0         // Read Mouse Status
        SB A 30         // Save Mouse Status to RAM (0x30)

        // Update MouseX in RAM and LEDs
        LB A A1         // Read Mouse X
        SB A 31         // Save Mouse X to RAM (0x31)
        SB A C1         // Send Mouse X to upper 8 LEDs

        // Updaet MouseX in RAM and LEDs
        LB B A2         // Read Mouse Y
        SB B 32         // Save Mouse Y to RAM (0x32)
        SB B C0         // Send Mouse Y to lower 8 LEDs

        // Send coordinates of Mouse to VGA
        SB A B0         // Send X coord to VGA
        SB B B1         // Send Y coord to VGA

        // Save original pixel value 
        LB A B2         // Get current pixel value
        SB A 22         // Store it in VGA variable region

        // Show Mouse location by inverting pixel
        NOT A           // Invert pixel value
        SB A B2         // Send inverted pixel value to VGA

        // Generate and send IR command
        FUNC IR

        IDLE            // Go back to IDLE state and wait for interrupts

/////////////////////////////////////////////////////////////////////
// Define Timer interrupt handling

TIMER:  FUNC SEG7       // Call 7-segmetn packet generation
        LB A E0         // Load lower 8 slide switches
        SB A B3         // Send slide switches to VGA to enable or disable GIF.
        LB A E1         // Load upper 8 slide switches
        SB A B4         // Send slide switches to VGA to set the background colour

        IDLE
