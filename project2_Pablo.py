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

        elif (line[0:2] == "sw"):  # sw
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
            print("TEST FOR Sb")
            print(imm)
            print(print_mem)
            print("memory location " + str(print_mem) + " is stored to $" + str(rt) + " with value of " + str(
                memory[imm]))
            instCount = instCount + 1
            ii += 1

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

        print(registers)
        print("\n\n")
        i += 1

    # print(registers)
    f.close()
    instCount += (len(labelName) * 1)
    print("The instruction count is ", str(instCount))
    print("For loop ended")
    for i in range(len(registers)):
        print("register $" + str(i) + str(register[i]))
    j = 8192
    while (j <= 12288):
        print("memory:" + hex(i) + " is " + str(memory[j]))
        j = j + 4


if __name__ == "__main__":
    main()