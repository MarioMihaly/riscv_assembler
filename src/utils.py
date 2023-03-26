import os
from constants import ROM_SIZE, RAM_SIZE
import exceptions as exc
from typing import Tuple, List, Union, Dict

def mkdir(path:str) -> None:
    '''
        Function to make directory and parents if it doesn't exists already.
        
        Parameters:
            path: String corresponding to the path to the directory to be created.
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def read_asm(path:str) -> List[str]:
    '''
        Fucntion to read .asm file line-by-line.

        Parameters:
            path: String corresponding to the path to the .asm file to be read.

        Returns:
            List of string corresponding to the lines read from the file.
    '''
    with open(path, 'r') as f:
        return f.readlines()

def clean_program(program:List[str], prefix:str='//') -> List[str]:
    '''
        Function to clean assembly program. Removes comments based on the specified
        prefix, leading and trailing white space and makes the whole code upper case.

        Parameters:
            program: List of string corresponding to the raw program lines.
            prefix (optional): String indicating the start of a comment.

        Returns:
            List of string, each string corresponding to an assembly instruction.
    '''
    cleaned_program = []
    
    for line in program:
        line = line.strip()
        # Remove empty lines
        if line == '': continue
        
        idx = line.find(prefix)
        if idx == -1: cleaned_program.append(line.strip().upper())
        elif idx == 0: continue
        else: cleaned_program.append(line[:idx-1].strip().upper())
            
    return cleaned_program

def get_labels(program:List[str], suffix:str=':') -> Tuple[List[str], Dict[str, int]]:
    '''
        Function to extract labels from program specified by suffix.

        Parameters:
            program: List of string corresponding to lines of program.
            suffix (optional): String indicating the end of a label.

        Returns:
            stripped_program: List of string corresponding to the lines of program without the labels.
            label_to_idx_dict: Dictionary mapping the labels to their original location in the program
                               starting from 0.

        Raises:
            InvalidLabelException: if the label is an empty string or placed on an empty line or comment line or
                                   if a label is not unique.
    '''
    label_to_idx_dict = dict()
    stripped_program = []
    
    for label_idx, line in enumerate(program):
        idx = line.find(suffix)
        
        if idx == 0:
            raise exc.InvalidLabelException(f'Label suffixed by "{suffix}" can\'t be empty in line "{line}"')
        
        if idx == len(line) - 1:
            print(line)
            raise exc.InvalidLabelException(f'Label suffixed by "{suffix}" must be followed by instruction in line "{line}"')
        
        if idx > 0:
            stripped_program.append(line[idx+1:].strip())
            label = line[:idx]
            if label in label_to_idx_dict:
                raise exc.InvalidLabelException(f'Label {label} already used! You can only use each label once and they are case insensitive.')
            label_to_idx_dict[label] = label_idx
            continue
            
        stripped_program.append(line)
   
    return stripped_program, label_to_idx_dict

def update_labels(label_to_idx_dict:Dict[str, int], curr_idx:int):
    '''
        Function to update label to ROM index mapping for assembly parsing. Only labels
        after the current line index are updated by incrementing their address.

        Parameters:
            label_to_idx_dict: Label to current index mapping in the current loop of the
                               assembl file parsing.
            curr_idx: Index of the currently processed line.

        Returns:
            Label to index mapping with necessary adjusments.
    '''
    for key in label_to_idx_dict.keys():
        # Only update labels that are after the current line
        if label_to_idx_dict[key] <= curr_idx: continue
        
        # Shift address by 1
        label_to_idx_dict[key] += 1
   
    return label_to_idx_dict
            
def insert_labels(program:List[str], labels:Dict[str, int]) -> List[str]:
    '''
        Function to replace placeholder labels with actual ROM address in the assembly
        program.

        Parameters:
            program: HEX encoded assembly program with comments.
            labels: Label to ROM address mapping for the program.

        Returns:
            Program with labels replaced with corresponding ROM addresses.
    '''
    joined_program = '\n'.join(program)
    
    for key in labels.keys():
        joined_program = joined_program.replace(key, bin_format(labels[key]))
        
    return joined_program.split('\n')

def convert_hex(num:str) -> int:
    '''
        Function to convert string hexadecimal to integer to facilitate address checking in integer format.
        
        Parameters:
            num: String corresponding to hexadecimal number to be converted.
            
        Returns:
            Integer value of hexadecimal number.
            
        Raises:
            InvalidAddressException if the provided address is not a valid HEX value.
    '''
    if not isinstance(num, str): return num
    try:
        num = int(num, base=16)
        return num
    
    except ValueError:
        raise exc.InvalidAddressException(f'String {num} is not a valid hexadecimal value.')
        
def bin_format(value:Union[int, str]) -> str:
    '''
        Function to format integer into 8-bit hex representation.
        
        Parameter:
            value: Integer or string to be formatted.
            
        Returns:
            String corresponding to formatted number.
            
        Raises:
            AssertionError if value converted to integer doesn't fit in 8-bit.
    '''
    num = convert_hex(value)
    
    assert 0 <= num < 2**8, f'Number {num} is too big for 8-bit representation!'
    return f'{num:02X}'

def insert_functions(program:List[str], functions:List[Tuple[List[str], int]], rom_size:int=ROM_SIZE) -> List[str]:
    '''
        Function to insert functions at a specific locations.
        
        Each function consist of a list of instuctions (strings) and a start index.
        
        Parameters:
            program: base program to insert functions into.
            functions: list of functions to insert.
            rom_size: size of the ROM to fit final program.
            
        Returns:
            Copy of the program with inserted functions.
            
        Raises:
            AssertionError: if function with given start index doesn't fit in ROM or
                            if region is already occupied in ROM where function is inserted.
    
    '''
    prog_copy = [''] * rom_size
    
    for i, line in enumerate('\n'.join(program).split('\n')):
        prog_copy[i] = line 
    
    for function, idx in functions:
        # Check function fits in the ROM
        assert idx + len(function) <= rom_size,\
            f'Function length of {len(function)} is too long at index={idx} from {rom_size} bytes ROM.'

        # Insert the function line by line
        for line in '\n'.join(function).split('\n'):
            # Check location in ROM is empty
            if prog_copy[idx]:
                raise Exception(f'ROM region {idx} is not empty. Risk of overwriting instructions.')

            # Insert function line and move ROM index
            prog_copy[idx] = line
            idx += 1
    
    return prog_copy

def generate_rom(program:List[str], filename:str, size:int=ROM_SIZE) -> None:
    '''
        Function to generate ROM .mem file from a program and write it to a file.
        
        Parameters:
            program: list of instructions (str).
            filename: path to file to write ROM.
            size: size of the ROM to fit program into.
            
        Raises:
            AssertionError: if program doesn't fit in given ROM size.
    '''
    rom = '\n'.join(program)
    rom_size = len(rom.split('\n'))
    assert rom_size <= size, f'Program is {rom_size} bytes for {size} bytes ROM.'
    
    # Fill empty lines in ROM with FF
    for i, line in enumerate(program):
        if not line: program[i] = 'FF'
    
    rom = '\n'.join(program)
    
    with open(filename, 'w') as f:
        f.write(rom)
        
def generate_ram(data_entries:List[Tuple[int, str]], filename, size=RAM_SIZE) -> None:
    '''
        Function to generate RAM .mem file from entries and write it to a file.
        
        Parameters:
            data_entries: list of (RAM address, value (str)) pairs.
            filename: path to file to write RAM.
            size: size of the RAM to fit entries into.
            
        Raises:
            IndexError: list index out of range error if RAM address isn't in the RAM.
    '''
    ram = [0]*size
    for i, d in data_entries:
        ram[i] = d
    
    ram = '\n'.join(map(bin_format, ram))
    with open(filename, 'w') as f:
        f.write(ram)