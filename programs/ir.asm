

// IR packet generation
IR:     LB A 00         // Load clear packet value
        SB A 40         // Reset packet in RAM
        JUMP CHECK_F   // Check going forward

        // At this point packet is generated
SEND_IR:LB A 40         // Load finished packet
        SB A 90         // Send packet to IR
        IDLE

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
