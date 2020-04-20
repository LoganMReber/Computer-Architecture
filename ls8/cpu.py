"""CPU functionality."""

import sys

# unit 0 - ALU , 1 - PC Mutator, 2 - Other

OPS = {
    0b00000001: {"unit": 1, "ops": 0, "code": 'HLT'},
    0b10000010: {"unit": 1, "ops": 2, "code": 'LDI'},
    0b01000111: {"unit": 1, "ops": 1, "code": 'PRN'},
}


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0]*8
        self.ram = [0]*256
        self.pc = 0

    def ram_read(self, loc):
        return self.ram[loc]

    def ram_write(self, loc, val):
        self.ram[loc] = val

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        # LDI
        else:
            raise Exception("Unsupported ALU operation")

    def cu(self, op, reg_a, reg_b):
        if op == "HLT":
            return
        elif op == 'LDI':
            self.reg[reg_a] = reg_b
        elif op == 'PRN':
            print(self.reg[reg_a])
        else:
            raise Exception("Unsupported CU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X %02X | %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        self.pc = 0
        ir = self.ram_read(self.pc)
        instruction = OPS[ir]["code"]
        while instruction != 'HLT':
            if OPS[ir]['unit'] == 0:
                self.alu(
                    instruction,
                    self.ram_read(self.pc+1),
                    self.ram_read(self.pc+2)
                )
            else:
                self.cu(
                    instruction,
                    self.ram_read(self.pc+1),
                    self.ram_read(self.pc+2)
                )
            self.pc += 1 + OPS[ir]['ops']
            ir = self.ram_read(self.pc)
            instruction = OPS[ir]["code"]
