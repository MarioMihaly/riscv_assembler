from enum import Enum

# Width and size of ROM
ROM_ADDR_WIDTH = 8
ROM_SIZE = 2 ** ROM_ADDR_WIDTH

# Width and size of RAM
RAM_ADDR_WIDTH = 7
RAM_SIZE = 2 ** RAM_ADDR_WIDTH

# Base addresses
MOUSE_BASE_ADDR   = int('0xA0', base=16)
LEDS_BASE_ADDR    = int('0xC0', base=16)
SEG7_BASE_ADDR    = int('0xD0', base=16)
SWITCH_BASE_ADDR  = int('0xE0', base=16)

# ALU op-codes
ALU_OPS = Enum('ALU_OPS',
               names=['ADD', 
                      'SUB',
                      'MUL',
                      'SL_A',
                      'SR_A',
                      'INC_A',
                      'INC_B',
                      'DEC_A',
                      'DEC_B',
                      'EQ',
                      'GT',
                      'LT',
                      'OUT_A'],
               start=0,
               type=int)

ALU_OPS_COMMENTS = {
    ALU_OPS.ADD : 'A + B',
    ALU_OPS.SUB : 'A - B', 
    ALU_OPS.MUL : 'A * B', 
    ALU_OPS.SL_A : 'A << 1', 
    ALU_OPS.SR_A : 'A >> 1', 
    ALU_OPS.INC_A : 'A + 1', 
    ALU_OPS.INC_B : 'B + 1', 
    ALU_OPS.DEC_A : 'A - 1', 
    ALU_OPS.DEC_B : 'B - 1', 
    ALU_OPS.EQ: 'A == B', 
    ALU_OPS.GT : 'A > B', 
    ALU_OPS.LT : 'A < B', 
    ALU_OPS.OUT_A : 'A'
}

# Conditional branch types
BRANCH_TYPES = Enum('BRANCH_TYPES',
                    names=['EQ', 'GT', 'LT'],
                    start=9,
                    type=int)

# Instruction codes
INST = Enum('INST',
            names=['READ_MEM_TO_A',
                   'READ_MEM_TO_B',
                   'WRITE_A_TO_MEM',
                   'WRITE_B_TO_MEM',
                   'ALU_OP_TO_A',
                   'ALU_OP_TO_B',
                   'BRANCH',
                   'GOTO',
                   'GOTO_IDLE',
                   'FUNC_CALL',
                   'RETURN',
                   'DEREF_A',
                   'DEREF_B'],
            start=0,
            type=int)