import sys

PRINT_BEEJ = 1  # OP CODE
HALT = 2  # OP CODE
PRINT_NUM = 3
SAVE = 4  # Save value to register
PRINT_REG = 5  # Print value from register
ADD = 6  # Takes 2 registers as values, adds value of second register and store it in first register (regA += regB)

memory = [PRINT_BEEJ, PRINT_NUM, 1, PRINT_NUM, 12, PRINT_BEEJ, PRINT_NUM, 37, HALT]

register = [0] * 8

pc = 0  # program counter
running = True

while running:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == HALT:
        running = False
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2

    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        pc += 3

    else:
        print(f"Unknown instruction {command}")
        sys.exit(1)
