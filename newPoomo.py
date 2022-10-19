from sys import argv, exit
from datetime import datetime
import random

if len(argv) != 2:
    print("Usage : newPoomo.py [Output]")
    exit(1)

def generateCodebook():
    retCarry = b''

    codebookBlockB = []
    for i in range(256):
        codebookBlockB.append(i)

    random.shuffle(codebookBlockB)

    for i in codebookBlockB:
        retCarry += i.to_bytes(1, byteorder='big')

    return retCarry

# Magic
poomoCarry = b'PUMO' + bytes(6)
# Timestamp
poomoCarry += int(datetime.now().timestamp()).to_bytes(10, byteorder='big')
poomoCarry += bytes(10)

# Make Codebook

# Block A (Address : 100)
poomoCarry += bytes([127] * 70)
poomoCarry += generateCodebook()

# Block B (Address : 400)
poomoCarry += bytes([127] * 44)
poomoCarry += generateCodebook()

# Block C (Address : 700)
poomoCarry += bytes([127] * 44)
poomoCarry += generateCodebook()

# Block D (Address : 1000)
poomoCarry += bytes([127] * 44)
poomoCarry += generateCodebook()

# Tail
poomoCarry += bytes([127] * 34) + b'FUTAGOHIME'

# Save to File
fxf = open(argv[1], 'wb')
fxf.write(poomoCarry)
fxf.close()
