import os
import sys
import utils
import argparse
from token_parser import parse_tokens
import constants as const

def arg_parse() -> argparse.Namespace:
    '''
        Function to parse command line arguments.

        Returns:
            A namedtuple with the arguments.
    '''
    parser = argparse.ArgumentParser(
        prog='asm.py',
        description='Welcome to the RISC-V assembler.'
    )

    parser.add_argument('--input', '-i',
                        type=str,
                        required=True,
                        help='Path to the input .asm file to be compiled.')
    parser.add_argument('--output', '-o',
                        type=str,
                        default=None,
                        help='Path to the output file.')
    parser.add_argument('--extension', '-e',
                        type=str,
                        default=const.DEFAULT_FILE_EXTENSION,
                        help='File extension to be used for the output file if it is not provided.')
    parser.add_argument('--force', '-f',
                        action='store_true',
                        default=False,
                        help='Flag to force overwriting of output file if it already exists.')

    return parser.parse_args()

def main():
    # Parse command line arguments
    args = arg_parse()
    input_path = args.input
    output_path = args.output
    file_extension = args.extension
    force = args.force

    # Check if input file exists.
    if not os.path.exists(input_path):
        print(f'Input file {input_path} does not exists.')
        sys.exit(1)

    # Check if input file has the valid file extension
    if not input_path.endswith(const.ASSEMBLY_FILE_EXTENSION):
        print(f'File extension {os.path.splitext(input_path)[-1]} is not supported. Use {const.ASSEMBLY_FILE_EXTENSION} instead.')
        sys.exit(1)

    # Open program.
    program = utils.read_asm(input_path)

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
    if const.MOUSE_INTERRUPT in label_dict:
        functions.append(([utils.hex_format(label_dict[const.MOUSE_INTERRUPT])], const.MOUSE_INTERRUPT_ADDR))
    
    if const.TIMER_INTERRUPT in label_dict:
        functions.append(([utils.hex_format(label_dict[const.TIMER_INTERRUPT])], const.TIMER_INTERRUPT_ADDR))

    program = utils.insert_functions(program, functions)

    # Check for provided output file. If not provided, generate it from the input file.
    if not output_path:
        if not file_extension.startswith('.'):
            output_path = os.path.splitext(input_path)[0] + '.' + file_extension
        else:
             output_path = os.path.splitext(input_path)[0] + file_extension

    # Check for existing output file.
    if not force and os.path.exists(output_path):
        print(f'File {output_path} already exists! Pass the "--force" argument to force overwriting it.')
        sys.exit(1)

    # Save program
    utils.generate_rom(program, output_path)
    sys.exit(0)

if __name__ == '__main__':
    main()