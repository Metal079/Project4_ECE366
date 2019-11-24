# Authors: Lohith Muppala and Kishan Patel (Based of the base code provided by Trung Le)
# I used the base code provided by Trung Le and implemented the other functions
global w

# Remember where each of the jump label is, and the target location
def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            # asm[lineCount] = line[line.index(":")+1:] #Dont include labels in linecount
        lineCount += 1
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')
    print(str(lineCount))


def main():
    registers = []  # 0$ = 0, $8=1, $9 = 2, $10 = 3, .......
    for i in range(100):
        registers.append(0)
    memory = []  # allocates the memory till 12288 which is 0x3000
    for i in range(12288):
        memory.append(0)
    memory.insert(8192, 79)  # test value
    labelIndex = []
    labelName = []
    instCount = 1
    f = open("mc.txt", "w+")
    h = open("mips.asm", "r")
    asm = h.readlines()
    for item in range(asm.count('\n')):  # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm, labelIndex, labelName)  # Save all jump's destinations
    lineUpdate = False
    mayo = str(0)
    #for line in asm:
    i=0
    j = 0
    ii = 0
    r = 0
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
    arr[0][10] = "Cycle"
    #for row in arr:
        #print(arr)
    #print(arr)

    #print("Press a for diagnosis mode. Press b for non-stop mode")
    mode = input("Press a for diagnosis mode. Press b for non-stop mode:    ")
    print(mode)

    totalCycles = 0
    totalInstrcutions = 0
    while(i < len(asm) + 9999):
        try:
            line = asm[i]
        except:
            pass
        if lineUpdate == True: #tells if the function was updated ex: jump function
            try:
                line = asm[w]
                w += 1
                #lineUpdate = False
            except:
                f.close()
                instCount += (len(labelName) * 1)
                print("The instruction count is ", str(instCount))
                #print("J type instruction total is %s", j)
                #print("R type instruction total is %s", r)
                #print("I type instruction total is %s", ii)
                c = 0
                while (c <= 99):
                    if (registers[c] != 0):
                        print("register $" + str(c) + " is " + str(registers[c]))
                    c = c + 1
                print("MEMORY VALUES:")
                k = 8192
                while (k <= 12288):
                    if (memory[k] != 0):
                        print("memory:" + hex(k) + " is " + str(memory[k]))
                    k = k + 4
                exit()
        else:
            pass
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0

        if (line[0:5] == "addiu"):  # ADDIU
            line = line.replace("addiu", "")
            line = line.split(",")
            imm = int(line[2])  # if (int(line[2]) > 0) else (65536 + int(line[2]))
            rs = int(line[1])
            rt = int(line[0])
            registers[rt] = registers[rs] + imm
            instCount = instCount + 1
            ii += 1

        elif (line[0:4] == "addi"):  # ADDI
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
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(addiArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)

        elif (line[0:4] == "addu"):  # ADD
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
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(adduArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)

        elif (line[0:3] == "add"):  # ADD
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

        elif (line[0:4] == "andi"):  # ADDI
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

        elif (line[0:3] == "and"):  # AND
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

        elif (line[0:3] == "ori"):  # ORI
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
            oriArr = [[""]*columns]*rows
            oriArr[0][0] = "ori" #"Instruction"
            oriArr[0][1] = "       0" #"RegDst"
            oriArr[0][2] = "       1" #"ALUSrc"
            oriArr[0][3] = "       0" #"MemtoReg"
            oriArr[0][4] = "       1" #"RegWrite"
            oriArr[0][5] = "       0" #"MemRead"
            oriArr[0][6] = "       0" #"MemWrite"
            oriArr[0][7] = "       0" #"Branch"
            oriArr[0][8] = "   0" #"Jump"
            oriArr[0][9] = "001000" #"ALUOp"
            oriArr[0][10] = "  4" #"Cycle"
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(oriArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)

        elif (line[0:2] == "or"):  # OR
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

        elif (line[0:3] == "xor"):  # XOR
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
            xorArr = [[""]*columns]*rows
            xorArr[0][0] = "xor" #"Instruction"
            xorArr[0][1] = "       0" #"RegDst"
            xorArr[0][2] = "       1" #"ALUSrc"
            xorArr[0][3] = "       0" #"MemtoReg"
            xorArr[0][4] = "       1" #"RegWrite"
            xorArr[0][5] = "       0" #"MemRead"
            xorArr[0][6] = "       0" #"MemWrite"
            xorArr[0][7] = "       0" #"Branch"
            xorArr[0][8] = "   0" #"Jump"
            xorArr[0][9] = "100110" #"ALUOp"
            xorArr[0][10] = "  4" #"Cycle"
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(xorArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)

        elif (line[0:3] == "sub"):  # SUB
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


        elif(line[0:5] == "multu"): # MULTU
            print(line)
            line = line.replace("multu","")
            line = line.split(",")
            print(line)
            rs = registers[int(line[0])] #if (registers[int(line[0])] > 0) else (65536 + registers[int(line[0])])
            rt = registers[int(line[1])] #if (registers[int(line[1])] > 0) else (65536 + registers[int(line[1])])
            if rs < 0:
                rs += 2**32
            if rt < 0:
                rt += 2**32

            print('RS ',rs)
            print('RT ',rt)
            value = format(int(rs * rt),'064b')
            hexval = format(hex(rs * rt))
            vallo = value[32:64]
            valhi = value[0:32]

            print("TEST FOR MULTU")
            print("The value in rs is " + str(rs) + " The value is rt is " + str(rt) + " Temp result is " + str(hexval))
            print("lo = " + str(vallo) + " hi = " + str(valhi))
            f.write(str('000000') + str(rs) + str(rt) + str('0000000000') + format(int('19',16),'06b')+ '\n')
            instCount = instCount + 1
            r += 1


        elif (line[0:4] == "mult"):  # MULT
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


        elif(line[0:4] == "mfhi"): # MFHI
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

        elif(line[0:4] == "mflo"): # MFLO
            line = line.replace("mflo", "")
            line = line.split(",")
            rd = int(line[0])
            declo = int(vallo, 2)
            registers[rd] = declo
            print("TEST FOR MFLO")
            print("The value in $" + str(rd) + " is " + str(declo) + " repesented by " + str(vallo))
            instCount = instCount + 1
            r += 1

        elif (line[0:2] == "lw"):  # lw
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
            loadArr = [[""]*columns]*rows
            loadArr[0][0] = "lw" #"Instruction"
            loadArr[0][1] = "       0" #"RegDst"
            loadArr[0][2] = "       1" #"ALUSrc"
            loadArr[0][3] = "       1" #"MemtoReg"
            loadArr[0][4] = "       1" #"RegWrite"
            loadArr[0][5] = "       1" #"MemRead"
            loadArr[0][6] = "       0" #"MemWrite"
            loadArr[0][7] = "       0" #"Branch"
            loadArr[0][8] = "   0" #"Jump"
            loadArr[0][9] = "100011" #"ALUOp"
            loadArr[0][10] = "  5" #"Cycle"
            totalCycles = totalCycles + 5
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(loadArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")


        elif (line[0:2] == "sw"):  # sw
            #line = line.replace("sw", "")
            #line = line.replace("(", ",")
            #line = line.replace(")", "")
            #line = line.split(",")
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
            ii +=1
            swArr = [[""]*columns]*rows
            swArr[0][0] = "sw" #"Instruction"
            swArr[0][1] = "       X" #"RegDst"
            swArr[0][2] = "       1" #"ALUSrc"
            swArr[0][3] = "       X" #"MemtoReg"
            swArr[0][4] = "       0" #"RegWrite"
            swArr[0][5] = "       0" #"MemRead"
            swArr[0][6] = "       1" #"MemWrite"
            swArr[0][7] = "       0" #"Branch"
            swArr[0][8] = "   0" #"Jump"
            swArr[0][9] = "101011" #"ALUOp"
            swArr[0][10] = "  4" #"Cycle"
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(swArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")


        elif (line[0:3] == "slt"):  # slt
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

        elif (line[0:3] == "srl"):  # srl
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
            r +=1

        elif (line[0:3] == "lui"):  # LUI
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
            ii +=1


        elif (line[0:2] == "lbu"):  # lw
            #line = line.replace("lbu", "")
            #line = line.replace("(", ",")
            #line = line.replace(")", "")
            #line = line.split(",")
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


        elif (line[0:2] == "lhu"):  # lw
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


        elif (line[0:3] == "sbu"):  # sw
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


        elif (line[0:2] == "sb"):  # sw
            line = line.replace("sb", "")
            #print(line)
            #line = line.replace("(", ",")
             #line = line.replace("$", "")
            #print(line)
            #line = line.replace(")", "")
             #line = line.replace("0x", ",")
            #print(line)
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            print(line)
            rt = int(line[0])
            mem = int(line[1], 16)

            #Eric's edit
            #print("this is the memory \n")
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
            sbArr = [[""]*columns]*rows
            sbArr[0][0] = "sb" #"Instruction"
            sbArr[0][1] = "       X" #"RegDst"
            sbArr[0][2] = "       1" #"ALUSrc"
            sbArr[0][3] = "       X" #"MemtoReg"
            sbArr[0][4] = "       0" #"RegWrite"
            sbArr[0][5] = "       0" #"MemRead"
            sbArr[0][6] = "       1" #"MemWrite"
            sbArr[0][7] = "       0" #"Branch"
            sbArr[0][8] = "   0" #"Jump"
            sbArr[0][9] = "101000" #"ALUOp"
            sbArr[0][10] = "  4" #"Cycle"
            totalCycles = totalCycles + 4
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(sbArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")

        elif (line[0:3] == "bne"):  # Branch if not equal
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
            bneArr = [[""]*columns]*rows
            bneArr[0][0] = "bne" #"Instruction"
            bneArr[0][1] = "       0" #"RegDst"
            bneArr[0][2] = "       1" #"ALUSrc"
            bneArr[0][3] = "       0" #"MemtoReg"
            bneArr[0][4] = "       0" #"RegWrite"
            bneArr[0][5] = "       0" #"MemRead"
            bneArr[0][6] = "       0" #"MemWrite"
            bneArr[0][7] = "       1" #"Branch"
            bneArr[0][8] = "   1" #"Jump"
            bneArr[0][9] = "001000" #"ALUOp"
            bneArr[0][10] = "  3" #"Cycle"
            totalCycles = totalCycles + 3
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(beqArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)


        elif (line[0:3] == "beq"):  # Branch if not equal
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
            beqArr = [[""]*columns]*rows
            beqArr[0][0] = "beq" #"Instruction"
            beqArr[0][1] = "       0" #"RegDst"
            beqArr[0][2] = "       1" #"ALUSrc"
            beqArr[0][3] = "       0" #"MemtoReg"
            beqArr[0][4] = "       0" #"RegWrite"
            beqArr[0][5] = "       0" #"MemRead"
            beqArr[0][6] = "       0" #"MemWrite"
            beqArr[0][7] = "       1" #"Branch"
            beqArr[0][8] = "   1" #"Jump"
            beqArr[0][9] = "001000" #"ALUOp"
            beqArr[0][10] = "  3" #"Cycle"
            totalCycles = totalCycles + 3
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(beqArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)

        elif (line[0:1] == "j"):  # Jump function
            line = line.replace("j", "")
            #line = line.split(",")
            name = str(line[0:])

            lineUpdate = True # lets the program know that the line location has changed
            z = labelName.index(name)
            print("JUMP LABEL INDEX #" + str(z))
            w = labelIndex[z]
            print("JUMP line number" + str(w))
            print(asm[w])
            instCount = instCount + 2
            j += 1
            jArr = [[""]*columns]*rows
            jArr[0][0] = "j" #"Instruction"
            jArr[0][1] = "       0" #"RegDst"
            jArr[0][2] = "       1" #"ALUSrc"
            jArr[0][3] = "       0" #"MemtoReg"
            jArr[0][4] = "       0" #"RegWrite"
            jArr[0][5] = "       0" #"MemRead"
            jArr[0][6] = "       0" #"MemWrite"
            jArr[0][7] = "       1" #"Branch"
            jArr[0][8] = "   1" #"Jump"
            jArr[0][9] = "001000" #"ALUOp"
            jArr[0][10] = "  3" #"Cycle"
            totalCycles = totalCycles + 2
            totalInstrcutions = totalInstrcutions + 1
            if(mode == 'a'):
                print(arr)
                print(jArr)
                move = ""
                #while(move != "\n"):
                move = input("Press enter:  ")
                #print(move)


        elif (line[0:4] == 'HASH'): #Special instruction, performs MULTU and XOR, skips MFHI and MFLO
                    line = line.replace('HASH', '')
                    line = line.split(",")
                    rd = int(line[0]) #save to this register
                    rt = registers[int(line[1])] #operand 1
                    rs = registers[int(line[2])] #operand 2
                    if rs < 0:
                        rs += 2**32
                    if rt < 0:
                        rt += 2**32

                    print('RS ',rs)
                    print('RT ',rt)
                    value = format(int(rs * rt),'064b')
                    hexval = format(hex(rs * rt))
                    print(str(rt) + " Times " + str(rs) + " is " + str(hexval))
                    hival = int(value[:32],2)
                    print(hival)
                    loval = int(value[32:],2)
                    print(loval)
                    xorval = hival ^ loval
                    registers[rd] = xorval
                    print("The folded result of xor is " + str(xorval) + " or " + str(hex(xorval)))
                    instCount = instCount + 1
        CPI = totalCycles / totalInstrcutions
        print("CPI: ")
        print(CPI)
        j = 8192
        while (j <= 8300):
            #index = 2000 + (j - 8192)
            print("memory: " + hex(j) + " is " + str(memory[j]))
            j = j + 4

        print(registers)
        print("\n\n")
        i += 1

    # print(registers)
    f.close()
    instCount += (len(labelName) * 1)
    print("The instruction count is ", str(instCount))
    print("For loop ended")
    for i in range(len(registers)):
        print("register $" + str(i) + str(registers[i]))
    j = 8192
    while (j <= 12288):
        print("memory:" + hex(i) + " is " + str(memory[j]))
        j = j + 4
    CPI = totalCycles / totalInstrcutions
    print("CPI: ")
    print(CPI)


if __name__ == "__main__":
    main()