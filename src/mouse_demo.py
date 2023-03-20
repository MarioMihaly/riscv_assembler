import os
from utils import mkdir, generate_rom, generate_ram
import sample_programs

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

def generate_test_rom():
    rom_path = os.path.join(DATA_DIR, 'ROM_test.mem')
    rom = sample_programs.get_test_rom()
    generate_rom(rom, rom_path)
    
def generate_test_ram():
    ram_path = os.path.join(DATA_DIR, 'RAM_test.mem')
    ram = sample_programs.get_test_ram()
    generate_ram(ram, ram_path)

def generate_processor_test():
    rom_path = os.path.join(DATA_DIR, 'ROM_processor_test.mem')
    ram_path = os.path.join(DATA_DIR, 'RAM_processor_test.mem')
    rom = sample_programs.get_processor_test_rom()
    ram = sample_programs.get_processor_test_ram()
    generate_rom(rom, rom_path)
    generate_ram(ram, ram_path)
    
def generate_mouse_demo():
    rom_path = os.path.join(DATA_DIR, 'ROM_MouseDemo.mem')
    ram_path = os.path.join(DATA_DIR, 'RAM_MouseDemo.mem')
    rom = sample_programs.get_mouse_demo_rom()
    ram = sample_programs.get_mouse_demo_ram()
    generate_rom(rom, rom_path)
    generate_ram(ram, ram_path)
    
def main():
    mkdir(DATA_DIR)
    generate_test_rom()
    generate_test_ram()
    generate_processor_test()
    generate_mouse_demo()

if __name__ == '__main__':
    main()