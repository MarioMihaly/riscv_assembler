import os
from constants import ROM_SIZE, RAM_SIZE
from typing import Tuple, List

def mkdir(path:str):
    '''
        Function to make directory and parents if it doesn't exists already.
        
        Parameters:
            path: string corresponding to the path to the directory to be created.
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def bin_format(num:int):
    '''
        Function to format integer into 8-bit hex representation.
        
        Parameter:
            num: integer to be formatted.
            
        Returns:
            String corresponding to formatted number.
            
        Raises:
            AssertionError if number doesn't fit in 8-bit.
    '''
    assert 0 <= num < 2**8, f'Number {num} is too big for 8-bit representation!'
    return f'{num:02X}'

def insert_functions(program:List[str], functions:List[Tuple[List[str], int]], rom_size:int=ROM_SIZE):
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
            AssertionError: if function with given start index doesn't fit in ROM OR
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

def generate_rom(program:List[str], filename:str, size:int=ROM_SIZE):
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
        
def generate_ram(data_entries:List[Tuple[int, str]], filename, size=RAM_SIZE):
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