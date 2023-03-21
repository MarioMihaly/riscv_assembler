from instructions import *
from constants import *
from utils import bin_format, insert_functions

def get_test_rom():
    return [bin_format(i) for i in range(ROM_SIZE)]

def get_test_ram():
    return [(i, i) for i in range(RAM_SIZE)]

def get_processor_test_rom():
    program = [
        # Memory instruction testing
        read_mem_to_A(0),
        read_mem_to_B(1),
        write_A_to_mem(2),
        write_B_to_mem(3),
        read_mem_to_A(3),
        read_mem_to_B(2), # line 12

        # ALU operation testing
        alu_to_A(ALU_OPS.ADD),
        alu_to_B(ALU_OPS.ADD),
        alu_to_B(ALU_OPS.SUB),
        alu_to_A(ALU_OPS.SUB),
        alu_to_A(ALU_OPS.MUL),
        alu_to_B(ALU_OPS.MUL),
        alu_to_A(ALU_OPS.SL_A),
        alu_to_A(ALU_OPS.SR_A),
        alu_to_B(ALU_OPS.SL_A),
        alu_to_B(ALU_OPS.SR_A),
        alu_to_A(ALU_OPS.INC_A),
        alu_to_A(ALU_OPS.DEC_A),
        alu_to_B(ALU_OPS.INC_B),
        alu_to_B(ALU_OPS.DEC_B),
        alu_to_A(ALU_OPS.EQ),
        alu_to_B(ALU_OPS.EQ),
        alu_to_A(ALU_OPS.EQ),
        alu_to_A(ALU_OPS.GT),
        alu_to_A(ALU_OPS.LT),
        alu_to_B(ALU_OPS.EQ),
        alu_to_B(ALU_OPS.LT),
        alu_to_B(ALU_OPS.GT),
        alu_to_B(ALU_OPS.INC_B),
        alu_to_B(ALU_OPS.OUT_A),
        alu_to_A(ALU_OPS.OUT_A), # line 37

        # Conditional branch testing
        breq(41), # Go to line 42 (address 41)
        read_mem_to_A(0), # Skipped
        bltq(45), # Go to line 46 (address 45)
        read_mem_to_A(0),
        bgtq(49), # Go to line 50 (address 49)
        read_mem_to_A(1), # Skipped
        read_mem_to_B(1), # Line 50

        # Unconditional branch
        goto(54), # Go to line 55 (address 54)
        alu_to_A(ALU_OPS.SL_A), # Line 54

        # Go to Idle State and wait for Interrupts
        goto_idle(), # Line 55

        # Functional call testing
        func_call(253), # Line 56

        # Register dereference testing
        deref_A(),
        deref_B(),
    
        # Extra feature testing: bitwise ALU operands
        alu_to_A(ALU_OPS.AND),
        alu_to_A(ALU_OPS.XOR),
        alu_to_B(ALU_OPS.NOT_A),
        alu_to_B(ALU_OPS.AND),
        alu_to_B(ALU_OPS.OR),
        alu_to_A(ALU_OPS.NOT_A),
        alu_to_B(ALU_OPS.XOR),
        alu_to_A(ALU_OPS.OR)
    ]
    
    # Insert mouse handling function
    functions = [
        ([bin_format(55), bin_format(55)], 254),
        ([func_return()], 253)  
    ]

    # Insert functions and return final program
    return insert_functions(program, functions)

def get_processor_test_ram():
    ram_entries = [
        (0, 42),
        (1, 69),
        (42, 69),
        (69, 42)
    ]
    return ram_entries

def get_mouse_demo_rom():
    program = [
        ############################
        # Start of Mouse interrupt

        # Read Mouse Status
        read_mem_to_A(MOUSE_BASE_ADDR, check=False),
        # Set dataline with Mouse Status for Seg7 to read
        write_A_to_mem(MOUSE_BASE_ADDR, check=False),

        # Read Mouse X and stored it back to RAM
        read_mem_to_A(MOUSE_BASE_ADDR + 1, check=False),
        write_A_to_mem(MOUSE_BASE_ADDR + 1, check=False),
        write_A_to_mem(LEDS_BASE_ADDR + 1, check=False), # Set upper 8 LEDs with X

        # Read Mouse Y and stored it back to RAM
        read_mem_to_A(MOUSE_BASE_ADDR + 2, check=False),
        write_A_to_mem(MOUSE_BASE_ADDR + 2, check=False),
        write_A_to_mem(LEDS_BASE_ADDR, check=False), # Set lower 8 LEDs with Y

        # At the end of the service, go back to IDLE and
        # wait for the next interrupt
        goto_idle(),

        # End of Mouse interrupt
        ############################
        # Start of Timer interrupt

        # Update slide switch
        read_mem_to_A(SWITCH_BASE_ADDR, check=False),
        # write_A_to_mem(SWITCH_BASE_ADDR, check=False),
        write_A_to_mem(SEG7_BASE_ADDR, check=False),

        # At the end of the service, go back to IDLE and
        # wait for the next interrupt
        goto_idle()

        # End of Timer interrupt
        ############################
    ]

    functions = [
        ([bin_format(0)], 255), # Mouse Interrupt servicing start address is 0x00
        ([bin_format(17)], 254), # Timer Interrupt servicing start address is 0x11 (17)

    ]

    return insert_functions(program, functions)

def get_mouse_demo_ram():
    return []