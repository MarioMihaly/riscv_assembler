from enum import Enum
from typing import List, Dict
import exceptions as exc
import instructions as inst
from constants import *
from utils import update_labels

############################################################
# Instruction type parsing functions
def parse_S(line:str) -> str:
    '''
        Function to parse preprocessed S-Type instructions, e.g. <TOKEN> {A, B} <ADDRESS>.

        Parameters:
            line: String corresponding to an S-Type instruction.
            
        Returns:
            String corresponding to the HEX representation of the instruction.
            
        Raises:
            InvalidArgumentException if incorrect number of arguments found.
            InvalidRegisterException if the target register is not supported.
    '''
    args = line.split()
    if len(args) != S_ARG_COUNT + 1:
        raise exc.InvalidArgumentException(f'S-Type instruction expects {S_ARG_COUNT} \
                                           arguments but got {len(args) - 1} in line "{line}".')
    
    # Parse line
    token = args[0]
    reg = args[1]
    addr = args[2]
    
    if reg not in REGISTERS._member_map_:
        raise exc.InvalidRegisterException(f'Register {reg} provided for {token} \
                                           is not supported. Use one of {REGISTERS._member_names_} instead.')
    
    opps_A = {
        TOKENS.LB.name : lambda: inst.read_mem_to_A(addr, check=False),
        TOKENS.SB.name : lambda: inst.write_A_to_mem(addr, check=False)
    }
    opps_B = {
        TOKENS.LB.name : lambda: inst.read_mem_to_B(addr, check=False),
        TOKENS.SB.name : lambda: inst.write_B_to_mem(addr, check=False)
    }
    
    if reg == REGISTERS.A.name:
        return opps_A[token]()
    
    return opps_B[token]()
    
def parse_R(line:str) -> str:
    '''
        Function to parse R-Type instructions, e.g. <TOKEN> {A, B}.

        Parameters:
            line: String corresponding to an R-Type instruction.
            
        Returns:
            String corresponding to the HEX representation of the instruction.
            
        Raises:
            InvalidArgumentException if incorrect number of arguments found.
            InvalidRegisterException if the target register is not supported.
    '''
    args = line.split()
    if len(args) != R_ARG_COUNT + 1:
        raise exc.InvalidArgumentException(f'R-Type instruction expects {R_ARG_COUNT} \
                                           arguments but got {len(args) - 1} in line "{line}".')
    
    # Parse line
    token = args[0]
    reg = args[1]
    
    if reg not in REGISTERS._member_map_:
        raise exc.InvalidRegisterException(f'Register {reg} provided for {token} \
                                           is not supported. Use one of {REGISTERS._member_names_} instead.')
        
    opps_A = {
        TOKENS.ADD.name   : lambda: inst.alu_to_A(ALU_OPS.ADD),
        TOKENS.SUB.name   : lambda: inst.alu_to_A(ALU_OPS.SUB),
        TOKENS.MUL.name   : lambda: inst.alu_to_A(ALU_OPS.MUL),
        TOKENS.SLA.name   : lambda: inst.alu_to_A(ALU_OPS.SL_A),
        TOKENS.SRA.name   : lambda: inst.alu_to_A(ALU_OPS.SR_A),
        TOKENS.SEQ.name   : lambda: inst.alu_to_A(ALU_OPS.EQ),
        TOKENS.SGT.name   : lambda: inst.alu_to_A(ALU_OPS.GT),
        TOKENS.SLT.name   : lambda: inst.alu_to_A(ALU_OPS.LT),
        TOKENS.AND.name   : lambda: inst.alu_to_A(ALU_OPS.AND),
        TOKENS.OR.name    : lambda: inst.alu_to_A(ALU_OPS.OR),
        TOKENS.XOR.name   : lambda: inst.alu_to_A(ALU_OPS.XOR),
        TOKENS.NOT.name   : lambda: inst.alu_to_A(ALU_OPS.NOT_A),
        TOKENS.COPY.name  : lambda: inst.alu_to_A(ALU_OPS.OUT_A),
        TOKENS.DEREF.name : lambda: inst.deref_A()
    }
    opps_B = {
        TOKENS.ADD.name   : lambda: inst.alu_to_B(ALU_OPS.ADD),
        TOKENS.SUB.name   : lambda: inst.alu_to_B(ALU_OPS.SUB),
        TOKENS.MUL.name   : lambda: inst.alu_to_B(ALU_OPS.MUL),
        TOKENS.SLA.name   : lambda: inst.alu_to_B(ALU_OPS.SL_A),
        TOKENS.SRA.name   : lambda: inst.alu_to_B(ALU_OPS.SR_A),
        TOKENS.SEQ.name   : lambda: inst.alu_to_B(ALU_OPS.EQ),
        TOKENS.SGT.name   : lambda: inst.alu_to_B(ALU_OPS.GT),
        TOKENS.SLT.name   : lambda: inst.alu_to_B(ALU_OPS.LT),
        TOKENS.AND.name   : lambda: inst.alu_to_B(ALU_OPS.AND),
        TOKENS.OR.name    : lambda: inst.alu_to_B(ALU_OPS.OR),
        TOKENS.XOR.name   : lambda: inst.alu_to_B(ALU_OPS.XOR),
        TOKENS.NOT.name   : lambda: inst.alu_to_B(ALU_OPS.NOT_A),
        TOKENS.COPY.name  : lambda: inst.alu_to_B(ALU_OPS.OUT_A),
        TOKENS.DEREF.name : lambda: inst.deref_B()
    }
    
    if reg == REGISTERS.A.name:
        return opps_A[token]()
    
    return opps_B[token]()
    
def parse_RR(line:str) -> str:
    '''
        Function to parse RR-Type instructions, e.g. e.g. <TOKEN> {A, B} {A, B}.
        
        Parameters:
            line: String corresponding to an RR-Type instruction.
            
        Returns:
            String corresponding to the HEX representation of the instruction.
            
        Raises:
            InvalidArgumentException if incorrect number of arguments found.
            InvalidRegisterException if the target or source register is not supported.
    '''
    args = line.split()
    if len(args) != RR_ARG_COUNT + 1:
        raise exc.InvalidArgumentException(f'RR-Type instruction expects {RR_ARG_COUNT} \
                                           arguments but got {len(args) - 1} in line "{line}".')
    
    # Parse line
    token = args[0]
    target_reg = args[1]
    source_reg = args[2]
    
    if target_reg not in REGISTERS._member_map_:
        raise exc.InvalidRegisterException(f'Target register {target_reg} provided for {token} \
                                           is not supported. Use one of {REGISTERS._member_names_} instead.')
    if source_reg not in REGISTERS:
        raise exc.InvalidRegisterException(f'Source register {source_reg} provided for {token} \
                                           is not supported. Use one of {REGISTERS._member_names_} instead.')
      
    opps_A = {
        REGISTERS.A.name : {
            TOKENS.INC.name : lambda: inst.alu_to_A(ALU_OPS.INC_A),
            TOKENS.DEC.name : lambda: inst.alu_to_A(ALU_OPS.DEC_A)
        },
        REGISTERS.B.name : {
            TOKENS.INC.name : lambda: inst.alu_to_A(ALU_OPS.INC_B),
            TOKENS.DEC.name : lambda: inst.alu_to_A(ALU_OPS.DEC_B)
        }
    }
    opps_B = {
        REGISTERS.A.name: {
            TOKENS.INC.name : lambda: inst.alu_to_B(ALU_OPS.INC_A),
            TOKENS.DEC.name : lambda: inst.alu_to_B(ALU_OPS.DEC_A)
        },
        REGISTERS.B.name: {
            TOKENS.INC.name : lambda: inst.alu_to_B(ALU_OPS.INC_B),
            TOKENS.DEC.name : lambda: inst.alu_to_B(ALU_OPS.DEC_B)
        }
    }
    
    if target_reg == REGISTERS.A.name:
        return opps_A[source_reg][token]()
    
    return opps_B[source_reg][token]()

def parse_B(line:str):
    '''
        Function to parse B-Type instructions, e.g. <TOKEN> <LABEL>.

        Parameters:
            line: String corresponding to an B-Type instruction.
            
        Returns:
            String corresponding to the HEX representation of the instruction.
            
        Raises:
            InvalidArgumentException if incorrect number of arguments found.
    '''
    args = line.split()
    if len(args) != B_ARG_COUNT + 1:
        raise exc.InvalidArgumentException(f'B-Type instruction expects {B_ARG_COUNT} \
                                           arguments but got {len(args) - 1} in line "{line}".')
    
    # Parse line
    token = args[0]
    label = args[1]
    
    opps = {
        TOKENS.BEQ.name  : lambda: inst.breq(label=label),
        TOKENS.BGT.name  : lambda: inst.bgtq(label=label),
        TOKENS.BLT.name  : lambda: inst.bltq(label=label),
        TOKENS.JUMP.name : lambda: inst.goto(label=label),
        TOKENS.FUNC.name : lambda: inst.func_call(label=label)
    }
    
    return opps[token]()
    
def parse_D(line:str):
    '''
        Function to parse D-Type instructions, <TOKEN> (no additional operand).

        Parameters:
            line: String corresponding to an D-Type instruction.
            
        Returns:
            String corresponding to the HEX representation of the instruction.
            
        Raises:
            InvalidArgumentException if incorrect number of arguments found.
    '''
    args = line.split()
    if len(args) != D_ARG_COUNT + 1:
        raise exc.InvalidArgumentException(f'D-Type instruction expects {D_ARG_COUNT} \
                                           arguments but got {len(args) - 1} in line "{line}".')
    
    # Parse line
    token = args[0]
    
    opps = {
        TOKENS.IDLE.name   : lambda: inst.goto_idle(),
        TOKENS.RETURN.name : lambda: inst.func_return()
    }
    
    return opps[token]()

def parse_tokens(program:List[str], label_to_idx_dict:Dict[str, int]) -> List[str]:
    '''
        Function to parse tokens in a program and update label mapping accordingly.

        Parameters:
            program: List of string corresponding to the cleaned lines of the assembly file.
            label_to_idx_dict: Label to original index in the cleaned assembly file mapping.
    
        Returns:
            List of string corresponding to the HEX encoding of the program.

        Raises:
            InvalidTokenException if token found in an instruction is not supported.
            ImplementationErrorException if a supported token is not mapped to an instruction type.
    '''
    parsed_program = []
    
    # Index to keep track of location in ROM.
    idx = 0
    
    for line in program:
        token = line.split()[0]
        
        if token not in TOKENS._member_map_:
            raise exc.InvalidTokenException(f'Unsupported token {token} found in line "{line}"')
        
        # S-Type instruction
        if token in S_TYPE:
            parsed_program.append(parse_S(line))
            label_to_idx_dict = update_labels(label_to_idx_dict, idx)
            idx += 2
            continue
                
        # R-Type instruction
        if token in R_TYPE:
            parsed_program.append(parse_R(line))
            idx += 1
            continue
            
        # RR-Type instruction
        if token in RR_TYPE:
            parsed_program.append(parse_RR(line))
            idx += 1
            continue
            
        # B-Type instruction
        if token in B_TYPE:
            parsed_program.append(parse_B(line))
            label_to_idx_dict = update_labels(label_to_idx_dict, idx)
            idx += 2
            continue
            
        # D-Type instruction
        if token in D_TYPE:
            parsed_program.append(parse_D(line))
            idx += 1
            continue

        # If it falls through all checks, unmapped token -> should not happend.
        raise exc.ImplementationErrorException(f'Token {token} is not mapped to any instruction type!')
        
    return parsed_program, label_to_idx_dict