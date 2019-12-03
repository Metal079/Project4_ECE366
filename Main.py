from __future__ import print_function
import sys
import os


def main():
    mode = int(input("Select from the following, \n1) Processor Simulation of MC,\n2) Processor Simulation of AP, \n3) DataCache simulation of CacheSim. "))
    diagnosis_mode = input("Press a for diagnosis mode, press b for non-stop mode. ")

    file = open("mips.asm", 'r')  # Opens the file
    asm = file.readlines()  # Gets a list of every line in file

    program = []

    labelLocations = {}


    for line in asm:  # For every line in the asm file
        #if line.count('#'):
            #line = list(line)
           # line[line.index('#'):-1] = ''
            #line = ''.join(line)

        if line.count(':'):
            line = "\n"
        if line[0] == '#':
            line = '\n'
        # Removes empty lines from the file
        if line[0] == '\n':
            continue
        line = line.replace('\n', '')

        instr = line[0:]
        program.append(instr)
        program.append('0')
        program.append('0')
        program.append('0')

    saveJumpLabel(asm, labelLocations)

    # We SHALL start the simulation!
    # machineCode = machineTranslation(program) # Translates the english assembly code to machine code
    if mode == 1 or mode == 2:
        sim(program, diagnosis_mode, labelLocations)  # Starts the assembly simulation with the assembly program machine code as # FUNCTION: read input file


def sim(program, diagnosis_mode, labelLocations):
    stage = {}
    three_cycle_instructions = 0
    four_cycle_instructions = 0
    five_cycle_instructions = 0

    # Control Signals
    rows, columns = (1, 11)
    arr = [[""] * columns] * rows
    arr[0][0] = "Instruction"
    arr[0][1] = "RegDst"
    arr[0][2] = "ALUSrc"
    arr[0][3] = "MemtoReg"
    arr[0][4] = "RegWrite"
    arr[0][5] = "MemRead"
    arr[0][6] = "MemWrite"
    arr[0][7] = "Branch"
    arr[0][8] = "Jump"
    arr[0][9] = "ALUOp"
    arr[0][10] = "Cycles(total)"

    finished = False  # Is the simulation finished?
    PC = 0  # Program Counter
    register = [0] * 32  # Let's initialize 32 empty registers
    mem = [0] * 12288  # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
    # But my machine has 16GB of RAM, its ok :)
    DIC = 0  # Dynamic Instr Count

    while (not (finished)):
        instruction = ""
        instrDescription = ""
        if PC == (len(program) * 4):
            finished = True
        if PC > (len(program) * 4) and (PC < len(program) * 4):
            break
        try:
            fetch = program[PC]
        except:
            break
        DIC += 1

        # HERES WHERE THE INSTRUCTIONS GO!
        if fetch[0:4] == 'addi' or "addi" in stage:  # Reads the Opcode
            instruction_name = "addi"
            four_cycle_instructions += 1

            addiArr = [[""] * columns] * rows
            addiArr[0][0] = "addi"  # "Instruction"
            addiArr[0][1] = "       0"  # "RegDst"
            addiArr[0][2] = "       1"  # "ALUSrc"
            addiArr[0][3] = "       0"  # "MemtoReg"
            addiArr[0][4] = "       1"  # "RegWrite"
            addiArr[0][5] = "       0"  # "MemRead"
            addiArr[0][6] = "       0"  # "MemWrite"
            addiArr[0][7] = "       0"  # "Branch"
            addiArr[0][8] = "   0"  # "Jump"
            addiArr[0][9] = "001000"  # "ALUOp"
            addiArr[0][10] = "  4"  # "Cycle"
            curArr = addiArr

            # Below code decides the multi-cycle stage of the instruction
            if "addi" not in stage:
                stage["addi"] = "fetch"
            elif stage["addi"] == "fetch":
                stage["addi"] = "decode"
            elif stage["addi"] == "decode":
                stage["addi"] = "execute"
            elif stage["addi"] == "execute":
                stage["addi"] = "writeback"

            # These next two lines find the space where the rx register is.
            if stage["addi"] == "writeback":
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(
                    fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[
                         register_start_location + 1:comma_location])  # This is the register that will added by immediate

                try:
                    if(fetch[comma_location + 3] == 'x'):
                        imm = int(fetch[comma_location + 1:], 16)  # Reads the immediate
                    else:
                        imm = int(fetch[comma_location + 1:])
                except:
                    imm = int(fetch[comma_location + 1:])

                register[rx] = register[ry] + imm
                PC += 4

                if register[rx] > 2147483647:  # Overflow support
                    quit()
                    register[rx] = register[rx] - (2147483647 * 2) - 1

        if fetch[0:4] == 'addu' or "addu" in stage:  # Reads the Opcode
            instruction_name = "addu"
            four_cycle_instructions += 1

            adduArr = [[""] * columns] * rows
            adduArr[0][0] = "addu"  # "Instruction"
            adduArr[0][1] = "       0"  # "RegDst"
            adduArr[0][2] = "       1"  # "ALUSrc"
            adduArr[0][3] = "       0"  # "MemtoReg"
            adduArr[0][4] = "       1"  # "RegWrite"
            adduArr[0][5] = "       0"  # "MemRead"
            adduArr[0][6] = "       0"  # "MemWrite"
            adduArr[0][7] = "       0"  # "Branch"
            adduArr[0][8] = "   0"  # "Jump"
            adduArr[0][9] = "001001"  # "ALUOp"
            adduArr[0][10] = "  4"  # "Cycle"
            curArr = adduArr

            # Below code decides the multi-cycle stage of the instruction
            if "addu" not in stage:
                stage["addu"] = "fetch"
            elif stage["addu"] == "fetch":
                stage["addu"] = "decode"
            elif stage["addu"] == "decode":
                stage["addu"] = "execute"
            elif stage["addu"] == "execute":
                stage["addu"] = "writeback"

            if stage["addu"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(
                    fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[register_start_location + 1:comma_location])  # This is a register that will be added

                register_start_location = fetch.find('$', register_start_location + 1)
                # comma_location = fetch.find(',', comma_location + 1)
                rz = int(fetch[register_start_location + 1:])  # This is a register that will be added
                register[rx] = register[ry] + register[rz]
                if register[rx] > 2147483647:
                    register[rx] -= 2147483648 + 2147483648
                elif register[rx] < -2147483648:
                    register[rx] += 2147483648 + 2147483648
                PC += 4

        if fetch[0:3] == 'ori' or 'ori' in stage:
            instruction_name = 'ori'
            four_cycle_instructions += 1

            oriArr = [[""] * columns] * rows
            oriArr[0][0] = "ori"  # "Instruction"
            oriArr[0][1] = "       1"  # "RegDst"
            oriArr[0][2] = "       1"  # "ALUSrc"
            oriArr[0][3] = "       0"  # "MemtoReg"
            oriArr[0][4] = "       1"  # "RegWrite"
            oriArr[0][5] = "       0"  # "MemRead"
            oriArr[0][6] = "       0"  # "MemWrite"
            oriArr[0][7] = "       0"  # "Branch"
            oriArr[0][8] = "   0"  # "Jump"
            oriArr[0][9] = "001101"  # "ALUOp"
            oriArr[0][10] = "  4"  # "Cycle"
            curArr = oriArr

            # Below code decides the multi-cycle stage of the instruction
            if "ori" not in stage:
                stage["ori"] = "fetch"
            elif stage["ori"] == "fetch":
                stage["ori"] = "decode"
            elif stage["ori"] == "decode":
                stage["ori"] = "execute"
            elif stage["ori"] == "execute":
                stage["ori"] = "writeback"

            if stage["ori"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(
                    fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[
                         register_start_location + 1:comma_location])  # This is the register that will added by immediate

                imm = int(fetch[comma_location + 1:])  # Reads the immediate
                register[rx] = register[ry] | imm
                PC += 4

        if fetch[0:2] == 'sw' or 'sw' in stage:
            instruction_name = 'sw'
            four_cycle_instructions += 1

            swArr = [[""] * columns] * rows
            swArr[0][0] = "sw"  # "Instruction"
            swArr[0][1] = "       X"  # "RegDst"
            swArr[0][2] = "       1"  # "ALUSrc"
            swArr[0][3] = "       X"  # "MemtoReg"
            swArr[0][4] = "       0"  # "RegWrite"
            swArr[0][5] = "       0"  # "MemRead"
            swArr[0][6] = "       1"  # "MemWrite"
            swArr[0][7] = "       0"  # "Branch"
            swArr[0][8] = "   0"  # "Jump"
            swArr[0][9] = "101011"  # "ALUOp"
            swArr[0][10] = "  4"  # "Cycle"
            curArr = swArr

            # Below code decides the multi-cycle stage of the instruction
            if "sw" not in stage:
                stage["sw"] = "fetch"
            elif stage["sw"] == "fetch":
                stage["sw"] = "decode"
            elif stage["sw"] == "decode":
                stage["sw"] = "execute"
            elif stage["sw"] == "execute":
                stage["sw"] = "memory"

            if stage["sw"] == "memory":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                offset = int(fetch[comma_location + 1:comma_location + 8], 16)  # Reads the immediate

                register_start_location = fetch.find('$', register_start_location + 1)
                parenthesis_end_location = fetch.find(')')
                ry = int(fetch[register_start_location + 1:parenthesis_end_location])

                mem[register[ry] + offset] = register[rx]
                PC += 4

        if fetch[0:3] == 'beq' or 'beq' in stage:
            instruction_name = 'beq'
            three_cycle_instructions += 1

            beqArr = [[""] * columns] * rows
            beqArr[0][0] = "beq"  # "Instruction"
            beqArr[0][1] = "       0"  # "RegDst"
            beqArr[0][2] = "       1"  # "ALUSrc"
            beqArr[0][3] = "       0"  # "MemtoReg"
            beqArr[0][4] = "       0"  # "RegWrite"
            beqArr[0][5] = "       0"  # "MemRead"
            beqArr[0][6] = "       0"  # "MemWrite"
            beqArr[0][7] = "       1"  # "Branch"
            beqArr[0][8] = "   1"  # "Jump"
            beqArr[0][9] = "001000"  # "ALUOp"
            beqArr[0][10] = "  3"  # "Cycle"
            curArr = beqArr

            # Below code decides the multi-cycle stage of the instruction
            if "beq" not in stage:
                stage["beq"] = "fetch"
            elif stage["beq"] == "fetch":
                stage["beq"] = "decode"
            elif stage["beq"] == "decode":
                stage["beq"] = "execute"

            if stage["beq"] == "execute":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(
                    fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[
                         register_start_location + 1:comma_location])  # This is the register that will added by immediate

                label = str(fetch[comma_location + 2:])  # Reads the label
                if register[rx] == register[ry]:
                    PC = (labelLocations[label] * 4)
                else:
                    PC += 4

        if fetch[0:3] == 'bne' or 'bne' in stage:
            instruction_name = 'bne'
            three_cycle_instructions += 1

            bneArr = [[""] * columns] * rows
            bneArr[0][0] = "bne"  # "Instruction"
            bneArr[0][1] = "       0"  # "RegDst"
            bneArr[0][2] = "       1"  # "ALUSrc"
            bneArr[0][3] = "       0"  # "MemtoReg"
            bneArr[0][4] = "       0"  # "RegWrite"
            bneArr[0][5] = "       0"  # "MemRead"
            bneArr[0][6] = "       0"  # "MemWrite"
            bneArr[0][7] = "       1"  # "Branch"
            bneArr[0][8] = "   1"  # "Jump"
            bneArr[0][9] = "001000"  # "ALUOp"
            bneArr[0][10] = "  3"  # "Cycle"
            curArr = bneArr

            # Below code decides the multi-cycle stage of the instruction
            if "bne" not in stage:
                stage["bne"] = "fetch"
            elif stage["bne"] == "fetch":
                stage["bne"] = "decode"
            elif stage["bne"] == "decode":
                stage["bne"] = "execute"

            if stage["bne"] == "execute":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[
                         register_start_location + 1:comma_location])  # This is the register that will added by immediate

                label = str(fetch[comma_location + 2:])  # Reads the label
                if register[rx] != register[ry]:
                    PC = (labelLocations[label] * 4)
                else:
                    PC += 4
                pass

        if fetch[0:3] == 'sub' or 'sub' in stage:
            instruction_name = "sub"
            four_cycle_instructions += 1

            subArr = [[""] * columns] * rows
            subArr[0][0] = "sub"  # "Instruction"
            subArr[0][1] = "       0"  # "RegDst"
            subArr[0][2] = "       1"  # "ALUSrc"
            subArr[0][3] = "       0"  # "MemtoReg"
            subArr[0][4] = "       1"  # "RegWrite"
            subArr[0][5] = "       0"  # "MemRead"
            subArr[0][6] = "       0"  # "MemWrite"
            subArr[0][7] = "       0"  # "Branch"
            subArr[0][8] = "   0"  # "Jump"
            subArr[0][9] = "100010"  # "ALUOp"
            subArr[0][10] = "  4"  # "Cycle"
            curArr = subArr

            # Below code decides the multi-cycle stage of the instruction
            if "sub" not in stage:
                stage["sub"] = "fetch"
            elif stage["sub"] == "fetch":
                stage["sub"] = "decode"
            elif stage["sub"] == "decode":
                stage["sub"] = "execute"
            elif stage["sub"] == "execute":
                stage["sub"] = "writeback"

            if stage["sub"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[register_start_location + 1:comma_location])  # This is a register that will be added

                register_start_location = fetch.find('$', register_start_location + 1)
                # comma_location = fetch.find(',', comma_location + 1)
                rz = int(fetch[register_start_location + 1:])  # This is a register that will be added
                register[rx] = register[ry] - register[rz]
                if register[rx] < -2147483648:
                    register[rx] += 2147483648 + 2147483647
                PC += 4

        if fetch[0:2] == 'lw' or 'lw' in stage:
            instruction_name = 'lw'
            five_cycle_instructions += 1

            lwArr = [[""] * columns] * rows
            lwArr[0][0] = "lw"  # "Instruction"
            lwArr[0][1] = "       0"  # "RegDst"
            lwArr[0][2] = "       1"  # "ALUSrc"
            lwArr[0][3] = "       1"  # "MemtoReg"
            lwArr[0][4] = "       1"  # "RegWrite"
            lwArr[0][5] = "       1"  # "MemRead"
            lwArr[0][6] = "       0"  # "MemWrite"
            lwArr[0][7] = "       0"  # "Branch"
            lwArr[0][8] = "   0"  # "Jump"
            lwArr[0][9] = "100011"  # "ALUOp"
            lwArr[0][10] = "  5"  # "Cycle"
            curArr = lwArr

            # Below code decides the multi-cycle stage of the instruction
            if "lw" not in stage:
                stage["lw"] = "fetch"
            elif stage["lw"] == "fetch":
                stage["lw"] = "decode"
            elif stage["lw"] == "decode":
                stage["lw"] = "execute"
            elif stage["lw"] == "execute":
                stage["lw"] = "memory"
            elif stage["lw"] == "memory":
                stage["lw"] = "writeback"

            if stage["lw"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                offset = int(fetch[comma_location + 1:comma_location + 8], 16)  # Reads the immediate

                register_start_location = fetch.find('$', register_start_location + 1)
                parenthesis_end_location = fetch.find(')')
                ry = int(fetch[register_start_location + 1:parenthesis_end_location])

                register[rx] = mem[register[ry] + offset]
                PC += 4

        if fetch[0:3] == 'xor' or 'xor' in stage:
            instruction_name = 'xor'
            four_cycle_instructions += 1

            xorArr = [[""] * columns] * rows
            xorArr[0][0] = "xor"  # "Instruction"
            xorArr[0][1] = "       0"  # "RegDst"
            xorArr[0][2] = "       1"  # "ALUSrc"
            xorArr[0][3] = "       0"  # "MemtoReg"
            xorArr[0][4] = "       1"  # "RegWrite"
            xorArr[0][5] = "       0"  # "MemRead"
            xorArr[0][6] = "       0"  # "MemWrite"
            xorArr[0][7] = "       0"  # "Branch"
            xorArr[0][8] = "   0"  # "Jump"
            xorArr[0][9] = "100110"  # "ALUOp"
            xorArr[0][10] = "  4"  # "Cycle"
            curArr = xorArr

            # Below code decides the multi-cycle stage of the instruction
            if "xor" not in stage:
                stage["xor"] = "fetch"
            elif stage["xor"] == "fetch":
                stage["xor"] = "decode"
            elif stage["xor"] == "decode":
                stage["xor"] = "execute"
            elif stage["xor"] == "execute":
                stage["xor"] = "writeback"

            if stage["xor"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(
                    fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[register_start_location + 1:comma_location])  # This is the register that will added by immediate

                register_start_location = fetch.find('$', register_start_location + 1)
                rz = int(fetch[register_start_location + 1:])  # This is a register that will be added
                register[rx] = register[ry] ^ register[rz]
                PC += 4

        if fetch[0:3] == 'sll' or 'sll' in stage:
            instruction_name = 'sll'
            four_cycle_instructions += 1

            sllArr = [[""] * columns] * rows
            sllArr[0][0] = "sll"  # "Instruction"
            sllArr[0][1] = "       1"  # "RegDst"
            sllArr[0][2] = "       1"  # "ALUSrc"
            sllArr[0][3] = "       0"  # "MemtoReg"
            sllArr[0][4] = "       1"  # "RegWrite"
            sllArr[0][5] = "       0"  # "MemRead"
            sllArr[0][6] = "       0"  # "MemWrite"
            sllArr[0][7] = "       0"  # "Branch"
            sllArr[0][8] = "   0"  # "Jump"
            sllArr[0][9] = "000000"  # "ALUOp"
            sllArr[0][10] = "  4"  # "Cycle"
            curArr = sllArr

            # Below code decides the multi-cycle stage of the instruction
            if "sll" not in stage:
                stage["sll"] = "fetch"
            elif stage["sll"] == "fetch":
                stage["sll"] = "decode"
            elif stage["sll"] == "decode":
                stage["sll"] = "execute"
            elif stage["sll"] == "execute":
                stage["sll"] = "writeback"

            if stage["sll"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(
                    fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[
                         register_start_location + 1:comma_location])  # This is the register that will added by immediate

                imm = int(fetch[comma_location + 1:])  # Reads the immediate

                register[rx] = register[ry] << 1
                while imm > 1:
                    count = 1
                    register[rx] = register[rx] << count
                    imm -= 1
                binary = bin(register[rx])
                hexi = hex(register[rx])
                if (register[rx] > 2147483647 and (str(binary[0] != '-') and str(binary[2] != '1'))):  # Overflow support
                    test = str(binary)[-32:]
                    register[rx] = int(test, 2)
                elif register[rx] < -2147483648 or (register[rx] > 2147483647 and str(binary[0] == '-')):
                    negative = '-'
                    binary = str(binary)[-32:]
                    binary = negative + binary
                    register[rx] = int(binary, 2)
                PC += 4

        if fetch[0:3] == 'slt' or "slt" in stage:  # Reads the Opcode
            instruction_name = "slt"
            four_cycle_instructions += 1

            sltArr = [[""] * columns] * rows
            sltArr[0][0] = "slt"  # "Instruction"
            sltArr[0][1] = "       1"  # "RegDst"
            swArr[0][2] = "       1"  # "ALUSrc"
            swArr[0][3] = "       0"  # "MemtoReg"
            swArr[0][4] = "       1"  # "RegWrite"
            swArr[0][5] = "       0"  # "MemRead"
            swArr[0][6] = "       0"  # "MemWrite"
            swArr[0][7] = "       0"  # "Branch"
            swArr[0][8] = "   0"  # "Jump"
            swArr[0][9] = "101011"  # "ALUOp"
            swArr[0][10] = "  4"  # "Cycle"
            curArr = swArr

            # Below code decides the multi-cycle stage of the instruction
            if "slt" not in stage:
                stage["slt"] = "fetch"
            elif stage["slt"] == "fetch":
                stage["slt"] = "decode"
            elif stage["slt"] == "decode":
                stage["slt"] = "execute"
            elif stage["slt"] == "execute":
                stage["slt"] = "writeback"

            if stage["slt"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[register_start_location + 1:comma_location])  # This is a register that will be added

                register_start_location = fetch.find('$', register_start_location + 1)
                # comma_location = fetch.find(',', comma_location + 1)
                rz = int(fetch[register_start_location + 1:])  # This is a register that will be added
                if register[ry] < register[rz]:
                    register[rx] = 1
                else:
                    register[rx] = 0
                PC += 4

        # print out the diagnosis info
        if diagnosis_mode == 'a':
            instruction = str(fetch)
            print(instruction)
            print("PC is currently " + str(PC))
            print("Instruction is currently in the " + stage[instruction_name] + " stage of it's execution")
            print(arr)
            print(curArr)
            printInfo(register, DIC, mem[8192:8704], PC, instruction, instrDescription, three_cycle_instructions,
                      four_cycle_instructions, five_cycle_instructions)
            input()

        end_instruction(stage)

    #print("bye")
    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    printInfo(register, DIC, mem[8192:8704], PC, instruction, instrDescription, three_cycle_instructions,
              four_cycle_instructions, five_cycle_instructions)

def printInfo(_register, _DIC, _mem, _PC, instr, instrDes, three_cycle_total, four_cycle_total, five_cycle_total):
    num = int(_PC / 4)
    # print('******* Instruction Number ' + str(num) + '. ' + instr + ' : *********\n')
    print(str(three_cycle_total / 3) + " instructions take 3 cycles to complete")
    print(str(four_cycle_total / 4) + " instructions take 4 cycles to complete")
    print(str(five_cycle_total / 5) + " instructions take 5 cycles to complete")
    print('\nDynamic Instr Count: ', _DIC)
    print("\nCPI: " + str(three_cycle_total + four_cycle_total + five_cycle_total / int(_DIC)))
    print('\nPC = ', _PC)
    print('\nRegisters $0- $31 \n', _register)
    print('\nMemory contents 0x2000 - 0x21fc ', _mem)
    print('\nPress enter to continue.......')
    #input()


def end_instruction(stage):
    try:
        if stage["addi"] == 'writeback':
            stage.pop("addi")
    except:
        pass
    try:
        if stage["addu"] == 'writeback':
            stage.pop("addu")
    except:
        pass
    try:
        if stage["ori"] == 'writeback':
            stage.pop("ori")
    except:
        pass
    try:
        if stage["sw"] == 'memory':
            stage.pop("sw")
    except:
        pass
    try:
        if stage["beq"] == 'execute':
            stage.pop("beq")
    except:
        pass
    try:
        if stage["bne"] == 'execute':
            stage.pop("bne")
    except:
        pass
    try:
        if stage["sub"] == 'writeback':
            stage.pop("sub")
    except:
        pass
    try:
        if stage["lw"] == 'writeback':
            stage.pop("lw")
    except:
        pass
    try:
        if stage["xor"] == 'writeback':
            stage.pop("xor")
    except:
        pass
    try:
        if stage["sll"] == 'writeback':
            stage.pop("sll")
    except:
        pass
    try:
        if stage["slt"] == 'writeback':
            stage.pop("slt")
    except:
        pass


# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm, labelLocations):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if line[0] == '#':
            line = '\n'
            lineCount -= 1
        elif (line.count(":")):
            labelLocations[str(line[0:line.index(":")])] = lineCount
            lineCount -= 1
        lineCount += 1
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')
    print(str(lineCount))

def twos(val_str, bytes):
    val = int(val_str, 2)
    b = val.to_bytes(bytes, byteorder=sys.byteorder, signed=False)
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)

if __name__ == "__main__":
    main()