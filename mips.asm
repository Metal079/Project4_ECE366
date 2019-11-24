addi $1, $0, 15
sb $1, 0x2000($0)
addi $2, $0, 4
sw $2, 0x2000($2)
lw $3, 0x2000($0)
ori $4, $0, 24
addi $5, $0, 32
ori $6, $5, 24
ori $7, $5, 48
addu $8, $7, $5
xor $8, $7, $8
addi $10, $0, $1
addi $9, $0, $1
loop9:
addi $9, $9, 1
beq $9, $10, loop9
bne $9, $2, loop9
