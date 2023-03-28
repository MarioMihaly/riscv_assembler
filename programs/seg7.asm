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