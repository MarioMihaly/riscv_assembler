import os
import utils
from tokens import parse_tokens
from constants import MOUSE_INTERRUPT, TIMER_INTERRUPT, MOUSE_INTERRUPT_ADDR, TIMER_INTERRUPT_ADDR

def main():
    path = '../programs/test.asm'

    # Open program.
    program = utils.read_asm(path)

    # Remove comments and white space.
    program = utils.clean_program(program)

    # Get label mapping.
    program, label_dict = utils.get_labels(program)

    # Parse program and update label mapping.
    program, label_dict = parse_tokens(program, label_dict)

    # Replace labels with mapped addresses.
    program = utils.insert_labels(program, label_dict)

    # Insert interrupt addresses as needed.
    functions = []
    if MOUSE_INTERRUPT in label_dict:
        functions.append(([utils.bin_format(label_dict[MOUSE_INTERRUPT])], MOUSE_INTERRUPT_ADDR))
    
    if TIMER_INTERRUPT in label_dict:
        functions.append(([utils.bin_format(label_dict[TIMER_INTERRUPT])], TIMER_INTERRUPT_ADDR))

    program = utils.insert_functions(program, functions)

    # Save program.
    save_path = os.path.splitext(path)[0] + '.mem'
    utils.generate_rom(program, save_path)

if __name__ == '__main__':
    main()