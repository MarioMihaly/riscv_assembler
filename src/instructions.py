from utils import bin_format, convert_hex
from constants import *
import exceptions as exc

def read_mem_to_A(mem_addr:int, ram_size=RAM_SIZE, check=True):
    mem_addr = convert_hex(mem_addr)
    if check:
        assert mem_addr >= 0 and mem_addr < ram_size,\
            f'Memory address {mem_addr} out of range for {ram_size} bytes RAM!'
    
    comment = f' // A <- Mem[{mem_addr}]'
    
    return '\n'.join([bin_format(INST.READ_MEM_TO_A) + comment, bin_format(mem_addr)])

def read_mem_to_B(mem_addr:int, ram_size=RAM_SIZE, check=True):
    mem_addr = convert_hex(mem_addr)
    if check:
        assert mem_addr >= 0 and mem_addr < ram_size,\
            f'Memory address {mem_addr} out of range for {ram_size} bytes RAM!'
    
    comment = f' // B <- Mem[{mem_addr}]'
    
    return '\n'.join([bin_format(INST.READ_MEM_TO_B) + comment, bin_format(mem_addr)])

def write_A_to_mem(mem_addr:int, ram_size=RAM_SIZE, check=True):
    mem_addr = convert_hex(mem_addr)
    if check:
        assert mem_addr >= 0 and mem_addr < ram_size,\
            f'Memory address {mem_addr} out of range for {ram_size} bytes RAM!'
    
    comment = f' // Mem[{mem_addr}] <- A'
    
    return '\n'.join([bin_format(INST.WRITE_A_TO_MEM) + comment, bin_format(mem_addr)])

def write_B_to_mem(mem_addr:int, ram_size=RAM_SIZE, check=True):
    mem_addr = convert_hex(mem_addr)
    if check:
        assert mem_addr >= 0 and mem_addr < ram_size,\
            f'Memory address {mem_addr} out of range for {ram_size} bytes RAM!'
    
    comment = f' // Mem[{mem_addr}] <- B'
    
    return '\n'.join([bin_format(INST.WRITE_B_TO_MEM) + comment, bin_format(mem_addr)])

def alu_to_A(op_code:int):
    assert op_code in ALU_OPS._value2member_map_, f'Op-code {op_code} is not valid!'
    
    comment = f' // A <- {ALU_OPS_COMMENTS[op_code]}'
    
    if op_code == ALU_OPS.OUT_A:
        return f'Z{hex(INST.ALU_OP_TO_A)[-1]}' + comment
    
    return bin_format((op_code << 4) + INST.ALU_OP_TO_A) + comment

def alu_to_B(op_code:int):
    assert op_code in ALU_OPS._value2member_map_, f'Op-code {op_code} is not valid!'
    
    comment = f' // B <- {ALU_OPS_COMMENTS[op_code]}'
    
    if op_code == ALU_OPS.OUT_A:
        return f'Z{hex(INST.ALU_OP_TO_B)[-1]}' + comment
    
    return bin_format((op_code << 4) + INST.ALU_OP_TO_B) + comment

def breq(mem_addr:int=None, label:str=None, rom_size=ROM_SIZE):
    if mem_addr:
        mem_addr = convert_hex(mem_addr)
        assert mem_addr >= 0 and mem_addr < rom_size,\
            f'Memory address {mem_addr} out of range for {rom_size} bytes ROM!'

        comment = f' // if A == B go to ROM[{mem_addr}]'

        return '\n'.join([bin_format((BRANCH_TYPES.EQ << 4) + INST.BRANCH) + comment, bin_format(mem_addr)])
    
    if label:
        comment = f' // if A == B go to ROM[{label}]'

        return '\n'.join([bin_format((BRANCH_TYPES.EQ << 4) + INST.BRANCH) + comment, label])

    raise exc.InvalidArgumentException('Either mem_addr or label must be specified for breq function!')
    
def bgtq(mem_addr:int=None, label=None, rom_size=ROM_SIZE):
    if mem_addr:
        mem_addr = convert_hex(mem_addr)
        assert mem_addr >= 0 and mem_addr < rom_size,\
            f'Memory address {mem_addr} out of range for {rom_size} bytes ROM!'

        comment = f' // if A > B go to ROM[{mem_addr}]'

        return '\n'.join([bin_format((BRANCH_TYPES.GT << 4) + INST.BRANCH) + comment, bin_format(mem_addr)])
    
    if label:
        comment = f' // if A > B go to ROM[{label}]'

        return '\n'.join([bin_format((BRANCH_TYPES.GT << 4) + INST.BRANCH) + comment, label])
    
    raise exc.InvalidArgumentException('Either mem_addr or label must be specified for bgtq function!')
        
def bltq(mem_addr:int=None, label=None, rom_size=ROM_SIZE):
    if mem_addr:
        mem_addr = convert_hex(mem_addr)
        assert mem_addr >= 0 and mem_addr < rom_size,\
            f'Memory address {mem_addr} out of range for {rom_size} bytes ROM!'

        comment = f' // if A < B go to ROM[{mem_addr}]'

        return '\n'.join([bin_format((BRANCH_TYPES.LT << 4) + INST.BRANCH) + comment, bin_format(mem_addr)])
    
    if label:
        comment = f' // if A < B go to ROM[{label}]'

        return '\n'.join([bin_format((BRANCH_TYPES.LT << 4) + INST.BRANCH) + comment, label])
    
    raise exc.InvalidArgumentException('Either mem_addr or label must be specified for bltq function!')

def goto(mem_addr:int=None, label=None, rom_size=ROM_SIZE):
    if mem_addr:
        mem_addr = convert_hex(mem_addr)
        assert mem_addr >= 0 and mem_addr < rom_size,\
            f'Memory address {mem_addr} out of range for {rom_size} bytes ROM!'

        comment = f' // Go to ROM[{mem_addr}]'

        return '\n'.join([bin_format(INST.GOTO) + comment, bin_format(mem_addr)])
    
    if label:
        comment = f' // Go to ROM[{label}]'

        return '\n'.join([bin_format(INST.GOTO) + comment, label])
    
    raise exc.InvalidArgumentException('Either mem_addr or label must be specified for goto function!')

def goto_idle():
    comment = ' // Go to Idle state and wait for Interrupts'
    return bin_format(INST.GOTO_IDLE) + comment

def func_call(mem_addr:int, rom_size=ROM_SIZE):
    mem_addr = convert_hex(mem_addr)
    assert mem_addr >= 0 and mem_addr < rom_size,\
        f'Memory address {mem_addr} out of range for {rom_size} bytes ROM!'
    
    comment = f' // Function call to ROM[{mem_addr}]. Context saved.'
    
    return '\n'.join([bin_format(INST.FUNC_CALL) + comment, bin_format(mem_addr)])

def func_return():
    comment = ' // Restoring saved context after function call.'
    return bin_format(INST.RETURN) + comment

def deref_A():
    comment = ' // A <- Mem[A]'
    return bin_format(INST.DEREF_A) + comment

def deref_B():
    comment = ' // B <- Mem[B]'
    return bin_format(INST.DEREF_B) + comment