# Prog A, parameter = 24
# version slt
# asd
# tayt
ori $8, $0, 24
addi $9, $0, 0x40
sw_loop:
sw $8, 0x2000($9)
addi $9, $9, -4
beq $9, $0, sw_done
sll $10, $8, 24
addu $10, $10, $8
sub $8, $0, $8
xor $8, $10, $8
beq $0, $0, sw_loop
sw_done:
addi $10, $0, 0x40
addu $12, $0, $0
lw_loop:
lw $8, 0x2000($9)
slt $11, $8, $0
bne $11, $0, skip
addi $12, $12, 1
skip:
addi $9, $9, 4
bne $9, $10, lw_loop
sw $12, 0x2000($0) 