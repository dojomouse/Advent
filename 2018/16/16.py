import re

# Addition:
# 
# addr (add register) stores into register C the result of adding register A and register B.

def addr(registers, args):
    A, B, C = args[1:]
    return C, registers[A] + registers[B]

# addi (add immedAte) stores into register C the result of adding register A and value B.
def addi(registers, args):
    A, B, C = args[1:]
    return C, registers[A] + B

# Multiplication:
# 
# mulr (multiply register) stores into register C the result of multiplying register A and register B.
def mulr(registers, args):
    A, B, C = args[1:]
    return C, registers[A] * registers[B]

# muli (multiply immedAte) stores into register C the result of multiplying register A and value B.
def muli(registers, args):
    A, B, C = args[1:]
    return C, registers[A] * B
# Bitwise AND:
# 
# banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
def banr(registers, args):
    A, B, C = args[1:]
    return C, registers[A] & registers[B]
# bani (bitwise AND immedAte) stores into register C the result of the bitwise AND of register A and value B.
def bani(registers, args):
    A, B, C = args[1:]
    return C, registers[A] & B
# Bitwise OR:
# 
# borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
def borr(registers, args):
    A, B, C = args[1:]
    return C, registers[A] | registers[B]
# bori (bitwise OR immedAte) stores into register C the result of the bitwise OR of register A and value B.
def bori(registers, args):
    A, B, C = args[1:]
    return C, registers[A] | B
# Assignment:
# 
# setr (set register) copies the contents of register A into register C. (Input B is ignored.)
def setr(registers, args):
    A, B, C = args[1:]
    return C, registers[A]
# seti (set immedAte) stores value A into register C. (Input B is ignored.)
def seti(registers, args):
    A, B, C = args[1:]
    return C, A
# Greater-than testing:
# 
# gtir (greater-than immedAte/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
def gtir(registers, args):
    A, B, C = args[1:]
    return C, 1 if A > registers[B] else 0
# gtri (greater-than register/immedAte) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
def gtri(registers, args):
    A, B, C = args[1:]
    return C, 1 if registers[A] > B else 0
# gtrr (greater-than registers/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
def gtrr(registers, args):
    A, B, C = args[1:]
    return C, 1 if registers[A] > registers[B] else 0
# Equality testing:
# 
# eqir (equal immedAte/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
def eqir(registers, args):
    A, B, C = args[1:]
    return C, 1 if A == registers[B] else 0
# eqri (equal register/immedAte) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
def eqri(registers, args):
    A, B, C = args[1:]
    return C, 1 if registers[A] == B else 0
# eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
def eqrr(registers, args):
    A, B, C = args[1:]
    return C, 1 if registers[A] == registers[B] else 0

class Sample:
    def __init__(self, regstart, opcode, regend):
        self.regstart = [int(x) for x in regstart]
        self.opcode = [int(x) for x in opcode]
        self.regend = [int(x) for x in regend]


# Q1: For each example, how many ops could it be? Sum the number of examples where the number of possBle ops is greater than 3.

# For each example, simulate each op and check the result. Means all ops need to defined. Create functions for each, store in list.

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

samples = []

f = open('input.txt','r')
buffer = f.read()

pattern = re.compile(r'Before:\s\[(.*)\]\n([\d*\s]*)\nAfter:\s\s\[(.*)\]\n')

for match in pattern.finditer(buffer):
    regstart = match.group(1).split(", ")
    opcode = match.group(2).split(" ")
    regend = match.group(3).split(", ")
    samples.append(Sample(regstart, opcode, regend))

# print([(s.regstart, s.opcode) for s in samples])

gt3_count = 0

for idx, s in enumerate(samples):
    print(idx)
    op_matches = 0
    for op in ops:
        reg, val = op(s.regstart, s.opcode)
        reg_temp = s.regstart.copy()
        reg_temp[reg] = val
        if s.regend == reg_temp:
            op_matches += 1
            print(op.__name__)
        if op_matches == 3:
            gt3_count += 1
            break

print(gt3_count)
