from __future__ import print_function
import os


def main():
    mode = int(input("Select from the following, \n1) Processor Simulation of MC,\n2) Processor Simulation of AP, \n3) DataCache simulation of CacheSim. "))
    diagnosis_mode = input("Press a for diagnosis mode, press b for non-stop mode. ")
    file = open("mips.asm", 'r')  # Opens the file
    asm = file.readlines()  # Gets a list of every line in file

    program = []  # Whats this? list

    for line in asm:  # For every line in the asm file
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)

        # Removes empty lines from the file
        if line[0] == '\n':
            continue
        line = line.replace('\n', '')

        instr = line[0:]
        program.append(instr)
        program.append('0')
        program.append('0')
        program.append('0')

    # We SHALL start the simulation!
    # machineCode = machineTranslation(program) # Translates the english assembly code to machine code
    if mode == 1 or mode == 2:
        sim(program, diagnosis_mode)  # Starts the assembly simulation with the assembly program machine code as # FUNCTION: read input file


def sim(program, diagnosis_mode):
    stage = {}
    three_cycle_instructions = 0
    four_cycle_instructions = 0
    five_cycle_instructions = 0

    #Control Signals
    rows, columns = (1, 11)
    arr = [[""]*columns]*rows
    #print(arr)
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
    register = [0] * 32  # Let's initialize 4 empty registers
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

            addiArr = [[""]*columns]*rows
            addiArr[0][0] = "addi" #"Instruction"
            addiArr[0][1] = "       0" #"RegDst"
            addiArr[0][2] = "       1" #"ALUSrc"
            addiArr[0][3] = "       0" #"MemtoReg"
            addiArr[0][4] = "       1" #"RegWrite"
            addiArr[0][5] = "       0" #"MemRead"
            addiArr[0][6] = "       0" #"MemWrite"
            addiArr[0][7] = "       0" #"Branch"
            addiArr[0][8] = "   0" #"Jump"
            addiArr[0][9] = "001000" #"ALUOp"
            addiArr[0][10] = "  4" #"Cycle"

            # Below code decides the multi-cycle stage of the instruction
            if "addi" not in stage:
                stage["addi"] = "fetch"
            elif stage["addi"] == "fetch":
                stage["addi"] = "decode"
            elif stage["addi"] == "decode":
                stage["addi"] = "execute"
            elif stage["addi"] == "execute":
                stage["addi"] = "writeback"
                PC += 4

            # These next two lines find the space where the rx register is.
            register_start_location = fetch.find('$')
            comma_location = fetch.find(',')
            rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

            register_start_location = fetch.find('$', register_start_location + 1)
            comma_location = fetch.find(',', comma_location + 1)
            ry = int(fetch[register_start_location + 1:comma_location])  # This is the register that will added by immediate

            imm = int(fetch[comma_location + 1:])  # Reads the immediate
            register[rx] = register[ry] + imm

            if register[rx] > 2147483647:  # Overflow support
                register[rx] = register[rx] - (2147483647 * 2) - 1

        if fetch[0:4] == 'addu' or "addu" in stage:  # Reads the Opcode
            instruction_name = "addu"
            four_cycle_instructions += 1

            adduArr = [[""]*columns]*rows
            adduArr[0][0] = "addi" #"Instruction"
            adduArr[0][1] = "       0" #"RegDst"
            adduArr[0][2] = "       1" #"ALUSrc"
            adduArr[0][3] = "       0" #"MemtoReg"
            adduArr[0][4] = "       1" #"RegWrite"
            adduArr[0][5] = "       0" #"MemRead"
            adduArr[0][6] = "       0" #"MemWrite"
            adduArr[0][7] = "       0" #"Branch"
            adduArr[0][8] = "   0" #"Jump"
            adduArr[0][9] = "001001" #"ALUOp"
            adduArr[0][10] = "  4" #"Cycle"

            # Below code decides the multi-cycle stage of the instruction
            if "addu" not in stage:
                stage["addu"] = "fetch"
            elif stage["addu"] == "fetch":
                stage["addu"] = "decode"
            elif stage["addu"] == "decode":
                stage["addu"] = "execute"
            elif stage["addu"] == "execute":
                stage["addu"] = "writeback"
                PC += 4

            if stage["addu"] == "writeback":
                # These next two lines find the space where the rx register is.
                register_start_location = fetch.find('$')
                comma_location = fetch.find(',')
                rx = int(fetch[register_start_location + 1:comma_location])  # This is the register where the result will be

                register_start_location = fetch.find('$', register_start_location + 1)
                comma_location = fetch.find(',', comma_location + 1)
                ry = int(fetch[register_start_location + 1:comma_location])  # This is a register that will be added

                register_start_location = fetch.find('$', register_start_location + 1)
                #comma_location = fetch.find(',', comma_location + 1)
                rz = int(fetch[register_start_location + 1:]) # This is a register that will be added
                register[rx] = register[ry] + register[rz]



        # print out the diagnosis info
        if diagnosis_mode == 'a':
            instruction = str(fetch)
            print(instruction)
            print("Instruction is currently in the " + stage[instruction_name] + " stage of it's execution")
            print(arr)
            print(addiArr)
            input()

        try:
            if stage["addi"] == 'writeback':
                stage.pop("addi")
            if stage["addu"] == 'writeback':
                stage.pop("addu")
        except:
            pass

    # Finished simulations. Let's print out some stats
    print('***Simulation finished***\n')
    printInfo(register, DIC, mem[0:259], PC, instruction, instrDescription)
'''
        elif (fetch[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")
            check = line[2]
            if ((len(line[2]) >= 4) and (check[1] == 'x')):  # if (int(line[2]) > 0) else (65536 + int(line[2]))
                imm = int(check, 16)
            else:
                imm = int(check)
            rs = int(line[1])
            rt = int(line[0])
            registers[rt] = registers[rs] + imm
            print("TEST FOR ADDI")
            print("The value in $" + str(rt) + " is " + str(registers[rt]))
            instCount = instCount + 1
            ii += 1
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
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(addiArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)

        elif (fetch[0:4] == "addu"):  # ADD
            line = line.replace("addu", "")
            line = line.split(",")
            rd = int(line[0])
            rs = registers[int(line[1])]
            rt = registers[int(line[2])]
            registers[rd] = rs + rt
            # registers.insert(rd,rs + rt )
            value = registers[rd]
            print("TEST FOR ADDU")
            print("The value in $" + str(rd) + " is " + str(value))
            instCount = instCount + 1
            r += 1
            adduArr = [[""] * columns] * rows
            adduArr[0][0] = "addi"  # "Instruction"
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
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(adduArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)

        elif (fetch[0:3] == "add"):  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = int(line[0])
            rs = registers[int(line[1])]
            rt = registers[int(line[2])]
            registers[rd] = rs + rt
            # registers.insert(rd,rs + rt )
            value = registers[rd]
            print("TEST FOR ADD")
            print("The value in $" + str(rd) + " is " + str(value))
            instCount = instCount + 1
            r += 1

        elif (fetch[0:4] == "andi"):  # ADDI
            line = line.replace("andi", "")
            line = line.split(",")
            check = line[2]
            if ((len(line[2]) >= 4) and (check[1] == 'x')):  # if (int(line[2]) > 0) else (65536 + int(line[2]))
                imm = int(check, 16)
            else:
                imm = int(check)
            rs = int(line[1])
            rt = int(line[0])
            registers[rt] = registers[rs] & imm

        elif (fetch[0:3] == "and"):  # AND
            line = line.replace("and", "")
            line = line.split(",")
            rd = int(line[0])
            rs = registers[int(line[1])]
            rt = registers[int(line[2])]
            print(rs)
            print(rt)
            value = rs & rt
            registers.insert(rd, value)
            print("TEST FOR AND")
            print("The value in $" + str(rd) + " is " + str(registers[rd]))
            instCount = instCount + 1
            r += 1

        elif (fetch[0:3] == "ori"):  # ORI
            line = line.replace("ori", "")
            line = line.split(",")
            rd = int(line[0])
            if ("x" in line[2]):
                line[2] = line[2].replace("0x", "")
                line[2] = format(int(line[2], 16))
            rs = int(registers[int(line[1])])
            rt = int(line[2])
            value = rs | rt
            registers[rd] = value
            # registers.insert(rd,value)
            print("TEST FOR ORI")
            print("The value in $" + str(rd) + " is " + str(registers[rd]))
            instCount = instCount + 1
            ii += 1
            oriArr = [[""] * columns] * rows
            oriArr[0][0] = "ori"  # "Instruction"
            oriArr[0][1] = "       0"  # "RegDst"
            oriArr[0][2] = "       1"  # "ALUSrc"
            oriArr[0][3] = "       0"  # "MemtoReg"
            oriArr[0][4] = "       1"  # "RegWrite"
            oriArr[0][5] = "       0"  # "MemRead"
            oriArr[0][6] = "       0"  # "MemWrite"
            oriArr[0][7] = "       0"  # "Branch"
            oriArr[0][8] = "   0"  # "Jump"
            oriArr[0][9] = "001000"  # "ALUOp"
            oriArr[0][10] = "  4"  # "Cycle"
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(oriArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)

        elif (fetch[0:2] == "or"):  # OR
            line = line.replace("or", "")
            line = line.split(",")
            rd = int(line[0])
            rs = registers[int(line[1])]
            rt = registers[int(line[2])]
            value = rs | rt
            registers.insert(rd, value)
            print("TEST FOR OR")
            print("The value in $" + str(rd) + " is " + str(registers[rd]))
            instCount = instCount + 1
            r += 1

        elif (fetch[0:3] == "xor"):  # XOR
            line = line.replace("xor", "")
            line = line.split(",")
            rd = int(line[0])
            rs = registers[int(line[1])]
            rt = registers[int(line[2])]
            value = rs ^ rt
            registers[rd] = value
            print("TEST FOR XOR")
            print("The value in $" + str(rd) + " is " + str(registers[rd]))
            instCount = instCount + 1
            r += 1
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
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(xorArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)

        elif (fetch[0:3] == "sub"):  # SUB
            line = line.replace("sub", "")
            line = line.split(",")
            rd = int(line[0])
            rs = registers[int(line[1])]
            rt = registers[int(line[2])]
            value = rs - rt
            registers.insert(rd, value)
            print("TEST FOR AND")
            print("The value in $" + str(rd) + " is " + str(registers[rd]))
            instCount = instCount + 1
            r += 1


        elif (fetch[0:5] == "multu"):  # MULTU
            print(line)
            line = line.replace("multu", "")
            line = line.split(",")
            print(line)
            rs = registers[int(line[0])]  # if (registers[int(line[0])] > 0) else (65536 + registers[int(line[0])])
            rt = registers[int(line[1])]  # if (registers[int(line[1])] > 0) else (65536 + registers[int(line[1])])
            if rs < 0:
                rs += 2 ** 32
            if rt < 0:
                rt += 2 ** 32

            print('RS ', rs)
            print('RT ', rt)
            value = format(int(rs * rt), '064b')
            hexval = format(hex(rs * rt))
            vallo = value[32:64]
            valhi = value[0:32]

            print("TEST FOR MULTU")
            print("The value in rs is " + str(rs) + " The value is rt is " + str(rt) + " Temp result is " + str(hexval))
            print("lo = " + str(vallo) + " hi = " + str(valhi))
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000') + format(int('19', 16), '06b') + '\n')
            instCount = instCount + 1
            r += 1


        elif (fetch[0:4] == "mult"):  # MULT
            line = line.replace("mult", "")
            line = line.split(",")
            rs = registers[int(line[0])]
            rt = registers[int(line[1])]
            value = rs * rt
            if (value < 0):
                bitresult = format(int(~value), '64b')
            else:
                bitresult = format(int(value), '64b')
            bitresult = bitresult.replace(" ", "0")
            if (value < 0):
                bitresult = bitresult.replace("0", "?")
                bitresult = bitresult.replace("1", "0")
                bitresult = bitresult.replace("?", "1")
            vallo = bitresult[33:65]
            if (value < 0):
                valtemp = vallo
                valtemp = valtemp.replace("0", "?")
                valtemp = valtemp.replace("1", "0")
                valtemp = valtemp.replace("?", "1")
                vallo = valtemp
            valhi = bitresult[0:33]
            print("TEST FOR MULT")
            print("The value in rs is " + str(rs) + " The value is rt is " + str(rt) + " Temp result is " + str(
                value) + " or " + str(bitresult))
            print("lo = " + str(vallo) + " hi = " + str(valhi))
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000') + format(int('18', 16), '06b') + '\n')
            instCount = instCount + 1
            r += 1


        elif (fetch[0:4] == "mfhi"):  # MFHI
            line = line.replace("mfhi", "")
            line = line.split(",")

            rd = int(line[0])
            # print(rd)
            # if(diff < 32):
            #     valhi = valhi.replace('0', '', diff-1)
            # else:
            #     valhi == '0'
            # print(valhi)
            dechi = int(valhi, 2)
            # print(dechi)
            # if(valhi[0] == '1'):
            #     valtemp = valhi
            #     valtemp = valtemp.replace("0", "?")
            #     valtemp = valtemp.replace("1", "0")
            #     valtemp = valtemp.replace("?", "1")
            #     print(valtemp)
            #     dechi = ~int(valtemp, 2) + 1
            # else:
            #     dechi = int(valhi, 2)
            registers[rd] = dechi
            print("TEST FOR MFHI")
            print("The value in $" + str(rd) + " is " + str(dechi) + " repesented by " + str(valhi))
            instCount = instCount + 1

        elif (fetch[0:4] == "mflo"):  # MFLO
            line = line.replace("mflo", "")
            line = line.split(",")
            rd = int(line[0])
            declo = int(vallo, 2)
            registers[rd] = declo
            print("TEST FOR MFLO")
            print("The value in $" + str(rd) + " is " + str(declo) + " repesented by " + str(vallo))
            instCount = instCount + 1
            r += 1

        elif (fetch[0:2] == "lw"):  # lw
            line = line.replace("lw", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            rt = int(line[0])
            mem = int(line[1], 16)
            rs = int(line[2])
            imm = registers[rs] + mem  # adding the $rs + offset
            registers.insert(rt, memory[imm])
            print_mem = hex(imm)
            print("TEST FOR LW");
            print("$" + str(rt) + " is " + str(registers[rt]))
            instCount = instCount + 1
            ii += 1
            loadArr = [[""] * columns] * rows
            loadArr[0][0] = "lw"  # "Instruction"
            loadArr[0][1] = "       0"  # "RegDst"
            loadArr[0][2] = "       1"  # "ALUSrc"
            loadArr[0][3] = "       1"  # "MemtoReg"
            loadArr[0][4] = "       1"  # "RegWrite"
            loadArr[0][5] = "       1"  # "MemRead"
            loadArr[0][6] = "       0"  # "MemWrite"
            loadArr[0][7] = "       0"  # "Branch"
            loadArr[0][8] = "   0"  # "Jump"
            loadArr[0][9] = "100011"  # "ALUOp"
            loadArr[0][10] = "  5"  # "Cycle"
            totalCycles = totalCycles + 5
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(loadArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")


        elif (fetch[0:2] == "sw"):  # sw
            # line = line.replace("sw", "")
            # line = line.replace("(", ",")
            # line = line.replace(")", "")
            # line = line.split(",")
            line = line.replace("sw", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            print(line)
            rt = int(line[0])
            mem = int(line[1], 16)
            print(mem)
            rs = int(line[2])
            print(rs)
            print(registers[rs])
            imm = registers[rs] + mem  # adding the $rs + offset
            memory.insert(imm, registers[rt])
            print_mem = hex(imm)
            print("TEST FOR SW")
            print(imm)
            print(print_mem)
            print("memory location " + str(print_mem) + " is stored to $" + str(rt) + " with value of " + str(
                memory[imm]))
            instCount = instCount + 1
            ii += 1
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
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(swArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")


        elif (fetch[0:3] == "slt"):  # slt
            line = line.replace("slt", "")
            line = line.split(",")
            rd = int(line[0])
            rt = registers[int(line[1])]
            rs = registers[int(line[2])]
            if (rt < rs):
                registers[rd] = 1
            else:
                registers[rd] = 0
            print("TEST FOR SLT")
            print("Is " + str(rt) + " less than " + str(rs) + " : " + str(registers[rd]))
            instCount = instCount + 1
            r += 1

            # f.write(str('0000000') + str(rs) + str(rt) + str(rd) +str('00000')+ str(format(int('2a',16),'06b')) +'\n')

        elif (fetch[0:3] == "srl"):  # srl
            line = line.replace("srl", "")
            line = line.split(",")

            rd = int(line[0])
            try:
                rt = registers[int(line[1])]
            except:
                try:
                    rt = registers[int(line[1], 16)]
                except:
                    rt = int(line[1], 16)
            shift = int(line[2])
            print("TEST FOR SRL")
            print(str(rt))
            rt = bin(rt)
            rt = rt.replace("b", "")
            print(str(rt))
            y = len(rt)
            z = 0
            rt = rt[0: y - shift]
            for x in range(0, shift):
                rt = '0' + rt
            print(str(rt))
            instCount = instCount + 1
            r += 1

        elif (fetch[0:3] == "lui"):  # LUI
            line = line.replace("lui", "")
            line = line.split(",")
            z = 0
            print("TEST FOR LUI")
            if ("x" in line[1]):
                line[1] = line[1].replace("0x", "")
                line[1] = format(int(line[1], 16))
            rd = int(line[0])
            imm = int(line[1])
            print(str(imm))
            imm = format(int(imm), '16b')
            imm = imm.replace(" ", "0")
            print(imm)
            temp = format(int(registers[rd]), '16b')
            temp = temp.replace(" ", "0")
            print(temp)
            temp = str(imm) + str(temp)
            print(temp)
            if (temp[0] == '1'):
                newtemp = temp
                newtemp = newtemp.replace("0", "?")
                newtemp = newtemp.replace("1", "0")
                newtemp = newtemp.replace("?", "1")
                registers[rd] = format(~int(newtemp, 2))
            else:
                registers[rd] = format(int(temp, 2))
            print(registers[rd])
            instCount = instCount + 1
            ii += 1


        elif (fetch[0:2] == "lbu"):  # lw
            # line = line.replace("lbu", "")
            # line = line.replace("(", ",")
            # line = line.replace(")", "")
            # line = line.split(",")
            line = line.replace("lbu", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            rt = int(line[0])
            mem = int(line[1], 16)
            rs = int(line[2])
            imm = registers[rs] + mem  # adding the $rs + offset
            registers.insert(rt, memory[imm])
            print_mem = hex(imm)
            print("TEST FOR Lbu");
            print("$" + str(rt) + " is " + str(registers[rt]))
            instCount = instCount + 1
            ii += 1


        elif (fetch[0:2] == "lhu"):  # lw
            line = line.replace("lhu", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            rt = int(line[0])
            mem = int(line[1], 16)
            rs = int(line[2])
            imm = registers[rs] + mem  # adding the $rs + offset
            registers.insert(rt, memory[imm])
            print_mem = hex(imm)
            print("TEST FOR Lhu");
            print("$" + str(rt) + " is " + str(registers[rt]))
            instCount = instCount + 1
            ii += 1


        elif (fetch[0:3] == "sbu"):  # sw
            line = line.replace("sbu", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            print(line)
            rt = int(line[0])
            mem = int(line[1], 16)
            print(mem)
            rs = int(line[2])
            print(rs)
            print(registers[rs])
            imm = registers[rs] + mem  # adding the $rs + offset
            memory.insert(imm, registers[rt])
            print_mem = hex(imm)
            print("TEST FOR Sbu")
            print(imm)
            print(print_mem)
            print("memory location " + str(print_mem) + " is stored to $" + str(rt) + " with value of " + str(
                memory[imm]))
            instCount = instCount + 1


        elif (fetch[0:2] == "sb"):  # sw
            line = line.replace("sb", "")
            # print(line)
            # line = line.replace("(", ",")
            # line = line.replace("$", "")
            # print(line)
            # line = line.replace(")", "")
            # line = line.replace("0x", ",")
            # print(line)
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            print(line)
            rt = int(line[0])
            mem = int(line[1], 16)

            # Eric's edit
            # print("this is the memory \n")
            print(mem)
            rs = int(line[2])
            print(rs)
            print(registers[rs])
            imm = registers[rs] + mem  # adding the $rs + offset
            memory.insert(imm, registers[rt])
            print_mem = hex(imm)
            print("TEST FOR Sb")
            print(imm)
            print(print_mem)
            print("memory location " + str(print_mem) + " is stored to $" + str(rt) + " with value of " + str(
                memory[imm]))
            instCount = instCount + 1
            ii += 1
            sbArr = [[""] * columns] * rows
            sbArr[0][0] = "sb"  # "Instruction"
            sbArr[0][1] = "       X"  # "RegDst"
            sbArr[0][2] = "       1"  # "ALUSrc"
            sbArr[0][3] = "       X"  # "MemtoReg"
            sbArr[0][4] = "       0"  # "RegWrite"
            sbArr[0][5] = "       0"  # "MemRead"
            sbArr[0][6] = "       1"  # "MemWrite"
            sbArr[0][7] = "       0"  # "Branch"
            sbArr[0][8] = "   0"  # "Jump"
            sbArr[0][9] = "101000"  # "ALUOp"
            sbArr[0][10] = "  4"  # "Cycle"
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(sbArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")

        elif (fetch[0:3] == "bne"):  # Branch if not equal
            line = line.replace("bne", "")
            line = line.split(",")
            try:
                if 30 < int(line[0]):
                    rt = int(line[0])
                else:
                    rt = registers[int(line[0])]

                if 30 < int(line[1]):
                    rs = int(line[1])
                else:
                    rs = registers[int(line[1])]
            except:
                rt = int(line[0])
                rs = int(line[1])
            name = str(line[2])

            if (rs != rt):
                lineUpdate = True  # lets the program know that the line location has changed
                z = labelName.index(name)
                print("LABEL INDEX #" + str(z))
                w = labelIndex[z]
                print("line number" + str(w))

            instCount = instCount + 2
            ii += 1
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
            totalCycles = totalCycles + 3
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(beqArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)


        elif (fetch[0:3] == "beq"):  # Branch if not equal
            line = line.replace("beq", "")
            line = line.split(",")
            try:
                if 30 < int(line[0]):
                    rt = int(line[0])
                else:
                    rt = registers[int(line[0])]

                if 30 < int(line[1]):
                    rs = int(line[1])
                else:
                    rs = registers[int(line[1])]
            except:
                rt = int(line[0])
                rs = int(line[1])
            name = str(line[2])

            if (rs == rt):  # Checks that rs and rt are not equal
                lineUpdate = True  # lets the program know that the line location has changed
                z = labelName.index(name)
                print("LABEL INDEX #" + str(z))
                w = labelIndex[z]
                print("line number" + str(w))
                print(asm[w])
            instCount = instCount + 2
            ii += 1
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
            totalCycles = totalCycles + 3
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(beqArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)

        elif (fetch[0:1] == "j"):  # Jump function
            line = line.replace("j", "")
            # line = line.split(",")
            name = str(line[0:])

            lineUpdate = True  # lets the program know that the line location has changed
            z = labelName.index(name)
            print("JUMP LABEL INDEX #" + str(z))
            w = labelIndex[z]
            print("JUMP line number" + str(w))
            print(asm[w])
            instCount = instCount + 2
            j += 1
            jArr = [[""] * columns] * rows
            jArr[0][0] = "j"  # "Instruction"
            jArr[0][1] = "       0"  # "RegDst"
            jArr[0][2] = "       1"  # "ALUSrc"
            jArr[0][3] = "       0"  # "MemtoReg"
            jArr[0][4] = "       0"  # "RegWrite"
            jArr[0][5] = "       0"  # "MemRead"
            jArr[0][6] = "       0"  # "MemWrite"
            jArr[0][7] = "       1"  # "Branch"
            jArr[0][8] = "   1"  # "Jump"
            jArr[0][9] = "001000"  # "ALUOp"
            jArr[0][10] = "  3"  # "Cycle"
            totalCycles = totalCycles + 2
            totalInstrcutions = totalInstrcutions + 1
            if (mode == 'a'):
                print(arr)
                print(jArr)
                move = ""
                # while(move != "\n"):
                move = input("Press enter:  ")
                # print(move)


        elif (fetch[0:4] == 'HASH'):  # Special instruction, performs MULTU and XOR, skips MFHI and MFLO
            line = line.replace('HASH', '')
            line = line.split(",")
            rd = int(line[0])  # save to this register
            rt = registers[int(line[1])]  # operand 1
            rs = registers[int(line[2])]  # operand 2
            if rs < 0:
                rs += 2 ** 32
            if rt < 0:
                rt += 2 ** 32

            print('RS ', rs)
            print('RT ', rt)
            value = format(int(rs * rt), '064b')
            hexval = format(hex(rs * rt))
            print(str(rt) + " Times " + str(rs) + " is " + str(hexval))
            hival = int(value[:32], 2)
            print(hival)
            loval = int(value[32:], 2)
            print(loval)
            xorval = hival ^ loval
            registers[rd] = xorval
            print("The folded result of xor is " + str(xorval) + " or " + str(hex(xorval)))
            instCount = instCount + 1
'''


def printInfo(_register, _DIC, _mem, _PC, instr, instrDes):
    num = int(_PC / 4)
    print('******* Instruction Number ' + str(num) + '. ' + instr + ' : *********\n')
    print(instrDes)
    print('\nRegisters $0- $31 \n', _register)
    print('\nDynamic Instr Count ', _DIC)
    print('\nMemory contents 0xff - 0x64 ', _mem)
    print('\nPC = ', _PC)
    print('\nPress enter to continue.......')
    #input()

if __name__ == "__main__":
    main()