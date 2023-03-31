# Assembler for custom RISC-V like ISA

## Description

Assembler written using standard Python libraries for a custom, 8-bit softcore processor, implemented in `Verilog` for the `Basys 3 FPGA board`. The processor is implemented based on the `Harvard architecture` using a `128-byte RAM` and a `256-byte ROM`. The assembler supports `25` instructions and the use of `labels` to aid branching and function calls in the assembly.

The output of the assembler is a `.mem` file, containing the `HEX` encoding of the instructions along with comments for each instructions. The decision to generate `.mem` files instead of `.txt` files was taken as `Vivado` automatically picks up on memory files when added to the project, keeping them at the `root` of the project, making it easer to define the path to the `ROM` and `RAM` files in the project.

## Usage

The basic execution of the assembler is done using the following command:

```bash.sh
$ python3 asm.py -i /path/to/input/file.asm
```

By default, the assembler outputs a `.mem` file at the location of the provided assembly file with the same name. The extension can be specified using the `--extension` or `-e` flag.

```bash.sh
$ python3 asm.py -i /path/to/input/file.asm -e .txt
```

Alternatively, the output file can be specified using the `--output` or `-o` flag. In this case the file extension of the provided file is used for the output file.

```bash.sh
$ python3  asm.py -i /path/to/input/file.asm -o /path/to/output/file.txt
```

To view summary of the available options use the `--help` or `-h` flag which will display the following information:

```
$ python3 asm.py -h

usage: asm.py [-h] --input INPUT [--output OUTPUT] [--extension EXTENSION] [--force]

Welcome to the RISC-V assembler.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Path to the input .asm file to be compiled.
  --output OUTPUT, -o OUTPUT
                        Path to the output file.
  --extension EXTENSION, -e EXTENSION
                        File extension to be used for the output file if it is not provided.
  --force, -f           Flag to force overwriting of output file if it already exists.
```

To test the assembler, see the sample programs provided in the [programs](programs) directory.

## Instruction Set Architecture (ISA)

The 8-bit softcore processor operates using only 2 registers, `R[A]` and `R[B]`, that can be used as destination (`R[rd]`) and source (`R[rs]`) registers.

### Instruction formats

Instruction formats are distinguished based on operands taken and used to aid the parsing of the arguments.

#### **S-Type**: `<mnemonic> R <addr>`

S-Type instructions are the load and store instructions used to read and write the `RAM`. The address to read/write is given as a 2 digit `HEX` number, corresponding to the `0 based address` in the `RAM` to operate on. For load instructions, the register `R` is the register, where the read byte is stored, while for store instructions, the register `R` holds the value to be written to the `RAM`.

#### **R-Type**: `<mnemonic> R[rd]`

R-Type instructions are the arithmetic and register dereferencing operations. For the arithmetic operations, the register `R` is the destination register. For the dereferencing instructions it is both the source and the destination register as the specified register is dereferenced and the value read from `RAM` is stored back to the same register.

#### **RR-Type**: `<mnemonic> R[rd] R[rs]`

RR-Type instructions are the complex arithmetic operations where the source and destination registers may differ. At this point only the register value incrementation and decrementation instructions fall into this category.

#### **B-Type**: `<mnemonic> <label>`

B-Type instructions are the conditional and unconditional branch and the function call instructions, where the label corresponds to the label of condition handling block or the function that is called. Labels are suffixed by `":"` to indicate the end of the label and `must be placed on a line with a valid instruction`.

#### **D-Type**: `<mnemonic>`

D-Type instructions have specific purpose that is independend of any registers, resulting in a direct interpretation.

### Supported instructions

| Mnemonic  | Format| Name                                      |Description (Verilog)              |
| ---       | :---: | ---                                       | ---                               |
| LB        | S     | Load byte                                 | R[rd] = RAM[addr]                 |
| SB        | S     | Store byte                                | RAM[addr] = R[rd]                 |
| ADD       | R     | Add registers                             | R[rd] = R[A] + R[B]               |
| SUB       | R     | Subtract registers                        | R[rd] = R[A] - R[B]               |
| MUL       | R     | Multiply registers                        | R[rd] = R[A] * R[B]               |
| SLA       | R     | Shift register A right                    | R[rd] = R[A] << 1                 |
| SRA       | R     | Shift register A left                     | R[rd] = R[A] >> 1                 |
| INC       | RR    | Increment register                        | R[rd] = R[rs] + 1                 |
| DEC       | RR    | Decrement register                        | R[rd] = R[rs] - 1                 |
| SEQ       | R     | Set equal                                 | R[rd] = (R[A] == R[B]) ? 1 : 0    |
| SGT       | R     | Set greater than                          | R[rd] = (R[A] > R[B]) ? 1 : 0     |
| SLT       | R     | Set less than                             | R[rd] = (R[A] < R[B]) ? 1 : 0     |
| AND       | R     | Bitwise AND registers                     | R[rd] = R[A] & R[B]               |
| OR        | R     | Bitwise OR registers                      | R[rd] = R[A] \| R[B]              |
| XOR       | R     | Bitwise XOR registers                     | R[rd] = R[A] ^ R[B]               |
| NOT       | R     | Bitwise invert register A                 | R[rd] = ~R[A]                     |
| COPY      | R     | Copy register A                           | R[rd] = R[A]                      |
| BEQ       | B     | Branch equal                              | if (R[A] == R[B]) than PC = addr  |
| BGT       | B     | Branch greater than                       | if (R[A] > R[B]) than PC = addr   |
| BLT       | B     | Branch less than                          | if (R[A] < R[B]) than PC = addr   |
| JUMP      | B     | Jump to label (address)                   | PC = addr                         |
| IDLE      | D     | Go to idle state and wait for interrupts  |                                   |
| FUNC      | B     | Call function at label (address)          | Context = PC + 2; PC = addr       |
| RETURN    | D     | Return from function call                 | PC = Context                      |
| DEREF     | R     | Dereference register                      | R[rd] = RAM[R[rd]]                |

## Source (src) folder content
 * [asm.py](src/asm.py) is the main file of the assembler, used to parse the assembly codes written with the [supported instructions](#supported-instructions). See the [Usage](#usage) section for instructions to use the assembler.
 * [constants.py](src/constants.py) contains all the constants used across the definition and call of custom instructions defined for the 8-bit processor. Holds the size of the ROM and RAM for memory address checks, enumeration of instructions, arithmetic logic unit (ALU) operation codes and comments, and instruction type mappings.
 * [exceptions.py](src/exceptions.py) contains the definition for the custom exceptions used in the assembler.
 * [instructions.py](src/instructions.py) contains the custom function for each of the instructions to make the ROM content generation easier. Each call returns the `hexadecimal` string encoding of the instruction call.
 * [token_parser.py](src/token_parser.py) is used to parse the lines of the assembly code by extracting the tokens (mnemonic) and calling the instruction type parser. By modifying the parser functions, the assembler can be easily extended to support more instructions and instruction formats.
 * [utils.py](src/utils.py) contains helper functions to tie together the assemlber, along with functions to format instructions, to insert subfunctions into a program, and to generate and save `ROM` and `RAM` files.
