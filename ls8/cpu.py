"""CPU functionality."""

import sys


'''
0b00000001: {'HLT'}
0b10000010: {'LDI'}
0b01000111: {'PRN'}
'''


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

    def load(self, filepath):
        """Load a program into memory."""

        address = 0
        file = open(filepath)
        program = []
        for line in file:
            cmd = line.strip()
            cmd = cmd.split(' ')[0]
            if len(cmd) == 8:
                program.append(int(cmd, 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == 0b00000:  # ADD
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 0b00001:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 0b00010:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 0b00011:
            self.reg[reg_a] //= self.reg[reg_b]
        elif op == 0b00100:
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 0b00101:
            self.reg[reg_a] += 1
        elif op == 0b00110:
            self.reg[reg_a] -= 1
        else:
            raise Exception("Unsupported ALU operation")

    def cu(self, op, reg_a, reg_b):
        if op == 0b00000:  # NOP
            return
        elif op == 0b00010:  # LDI
            self.reg[reg_a] = reg_b
        elif op == 0b00111:  # PRN
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

        while True:
            ir = self.ram_read(self.pc)
            if ir == 1:
                break
            size = (ir & 0b11000000) >> 6
            alu = (ir & 0b00100000) >> 5
            cmd = ir & 0b00011111
            if alu:
                self.alu(
                    cmd,
                    self.ram_read(self.pc+1),
                    self.ram_read(self.pc+2)
                )
            else:
                self.cu(
                    cmd,
                    self.ram_read(self.pc+1),
                    self.ram_read(self.pc+2)
                )
            self.pc += size + 1
