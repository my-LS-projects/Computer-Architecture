"""CPU functionality."""

import sys

### OP CODES ###
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 8 general-purpose registers
        self.reg = [0] * 8
        # 256 bytes of memory
        self.ram = [0] * 256
        # program counter
        self.pc = 0

    def load(self, file):
        """Load a program into memory."""
        try:
            address = 0

            with open(file) as f:
                for line in f:
                    # strip out white space, split at inline comment
                    cleaned_line = line.strip().split("#")
                    # grab number
                    value = cleaned_line[0].strip()

                    # check if blank or not, if blank skip to next line
                    if value != "":
                        # convert from binary to num
                        num = int(value, 2)
                        self.ram[address] = num
                        address += 1

                    else:
                        continue

        except FileNotFoundError:
            # exit and give error
            print("ERROR: File not found")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc

        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def ram_read(self, mar):
        """
        should accept the address to read and 
        return the value stored there.

        MAR = Memory Address Register
        MAR contains the address that is being read or written to.
        """
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        """
        should accept a value to write, and 
        the address to write it to.

        MDR = Memory Data Register
        MAR = Memory Address Register

        MAR contains the address that is being read or written to. The MDR contains
        the data that was read or the data to write.
        """
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        while True:
            op = self.ram_read(self.pc)
            if op == LDI:
                # Set the value of a register to an integer.
                index = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[index] = value
                self.pc += 3

            elif op == PRN:
                # Print numeric value stored in the given register.
                index = self.ram[self.pc + 1]
                print(self.reg[index])
                self.pc += 2

            elif op == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3

            elif op == HLT:
                # hHalt the CPU (and exit the emulator).
                print("Exiting...")
                sys.exit(0)

            else:
                print("ERROR: Unknown command")
                sys.exit(1)
