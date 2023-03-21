# Python scripts to generate ROM and RAM files

## Description
This directory contains everything needed to generate the required `.mem` files used for the testing of the Processor, ROM and RAM implementations via [test benches](../sim/). The scripts also generate the required `.mem` files for the `Mouse-Processor demo`.

The decision to generate `.mem` files instead of `.txt` files was taken as `Vivado` automatically picks up on memory files when added to the project, keeping them at the `root` of the project, making it easer to define the path to the `ROM` and `RAM` files in the project.

## Source (src) folder content
 * [constants.py](src/constants.py) contains all the constants used across the definition and call of custom instructions defined for the 8-bit processor. Holds the size of the ROM and RAM for memory address checks, enumeration of instructions, arithmetic logic unit (ALU) operation codes and comments.
 * [instructions.py](src/instructions.py) contains the custom function for each of the instructions to make the ROM content generation easier. Each call returns the `hexadecimal` string encoding of the instruction call. 
 * [mouse_demo.py](src/mouse_demo.py) is the main Python script used to generate the required `.mem` files. See the [Usage](#usage) section for usage.
 * [sample_programs.py](src/sample_programs.py) contains the `ROM` and `RAM` definitions for the different file generations.
 * [utils.py](src/utils.py) contains helper functions to format instructions, to insert subfunctions into a program, and to generate and save `ROM` and `RAM` files.

## Usage

Run the following code from the [src](src/) directory in command line. The script will generate a `data` directory in the [src](src/) directory that contains all the required `.mem` files.

```bash.sh
python mouse_demo.py
```