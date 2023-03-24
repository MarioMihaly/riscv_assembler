from enum import Enum

############################################################
# Default file extension.
ASSEMBLY_FILE_EXTENSION = '.asm'
DEFAULT_FILE_EXTENSION = '.mem'

############################################################
# Width and size of ROM
ROM_ADDR_WIDTH = 8
ROM_SIZE = 2 ** ROM_ADDR_WIDTH

############################################################
# Width and size of RAM
RAM_ADDR_WIDTH = 7
RAM_SIZE = 2 ** RAM_ADDR_WIDTH

############################################################
# Base addresses
MOUSE_BASE_ADDR   = int('0xA0', base=16)
LEDS_BASE_ADDR    = int('0xC0', base=16)
SEG7_BASE_ADDR    = int('0xD0', base=16)
SWITCH_BASE_ADDR  = int('0xE0', base=16)

############################################################
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
                      'AND',
                      'OR',
                      'XOR',
                      'NOT_A',
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
    ALU_OPS.AND : 'A AND B',
    ALU_OPS.OR : 'A OR B',
    ALU_OPS.XOR : 'A XOR B',
    ALU_OPS.NOT_A : 'NOT A',
    ALU_OPS.OUT_A : 'A'
}

############################################################
# Conditional branch types
BRANCH_TYPES = Enum('BRANCH_TYPES',
                    names=['EQ', 'GT', 'LT'],
                    start=9,
                    type=int)

############################################################
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

############################################################
# Assembly tokens supported by the assembler
TOKENS = Enum('TOKENS',
              names=[
                    'LB',
                    'SB',
                    'ADD',
                    'SUB',
                    'MUL',
                    'SLA',
                    'SRA',
                    'INC',
                    'DEC',
                    'SEQ',
                    'SGT',
                    'SLT',
                    'AND',
                    'OR',
                    'XOR',
                    'NOT', 
                    'COPY',
                    'BEQ',
                    'BGT',
                    'BLT',
                    'JUMP',
                    'IDLE',
                    'FUNC',
                    'RETURN',
                    'DEREF'],
              type=str)

# Registers used by the processor
REGISTERS = Enum('REGISTERS', names=['A', 'B'], type=str)

############################################################
# Instruction type mapping
# Memory operation, e.g. <TOKEN> {A, B} <ADDRESS>
S_ARG_COUNT = 2
S_TYPE = {TOKENS.LB.name,
          TOKENS.SB.name}

# Simple register operation, e.g. <TOKEN> {A, B}
R_ARG_COUNT = 1
R_TYPE = {TOKENS.ADD.name,
          TOKENS.SUB.name,
          TOKENS.MUL.name,
          TOKENS.SLA.name,
          TOKENS.SRA.name,
          TOKENS.SEQ.name,
          TOKENS.SGT.name,
          TOKENS.SLT.name,
          TOKENS.AND.name,
          TOKENS.OR.name,
          TOKENS.XOR.name,
          TOKENS.NOT.name, 
          TOKENS.COPY.name,
          TOKENS.DEREF.name}

# Complex register operation, e.g. <TOKEN> {A, B} {A, B}
RR_ARG_COUNT = 2
RR_TYPE = {TOKENS.INC.name,
           TOKENS.DEC.name}

# Branch like operation, e.g. <TOKEN> <LABEL>
B_ARG_COUNT = 1
B_TYPE = {TOKENS.BEQ.name,
          TOKENS.BGT.name,
          TOKENS.BLT.name,
          TOKENS.JUMP.name, 
          TOKENS.FUNC.name}
# Direct operation, e.g. <TOKEN> (no additional operand)
D_ARG_COUNT = 0
D_TYPE = {TOKENS.IDLE.name,
          TOKENS.RETURN.name}

############################################################
# Interrupt call labels
MOUSE_INTERRUPT = 'MOUSE'
TIMER_INTERRUPT = 'TIMER'

# Interrupt addresses
MOUSE_INTERRUPT_ADDR = int('FF', base=16)
TIMER_INTERRUPT_ADDR = int('FE', base=16)