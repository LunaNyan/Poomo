from core.poomoRead import poomoRead
from sys import argv, exit
from zlib import decompress

if len(argv) != 4:
    print("Usage : poomoDecode.py [poomo] [target] [output]")
    exit(1)

# Open Poomo
poomo = open(argv[1], 'rb')
codebook = poomoRead(poomo)

# Open Target File
targetFile = open(argv[2], 'rb')

# Check Magic
targetFile.seek(0)
if targetFile.read(5) != b'EPUMO':
    print("Target File has Invalid Magic")
    exit(1)

# Check if Compressed
targetFile.seek(5)
if targetFile.read(5) != bytes(5):
    print("Compressed")
    compressed = True
else:
    print("Not Compressed")
    compressed = False

# Get Binary Size
targetFile.seek(10)
targetSize = int.from_bytes(targetFile.read(10), byteorder='big')
print("Received " + str(targetSize) + " Bytes")

# Read Whole Data
targetFile.seek(100)
targetBinary = bytearray(targetFile.read(targetSize))
targetBinary.reverse()

# Ready for Decode
decodeCarry = b''
decodedTemp = b''

currentRound = 0
countRound = 0
bytesCount = 0

print("Decode Start")
for b in targetBinary:
    if countRound == 7:
        if currentRound == 3:
            currentRound = 0
        else:
            currentRound += 1
        countRound = 0
    # Checkpoint
    if bytesCount % 16384 == 0:
        print("Checkpoint : " + str(decodedTemp[:16]))
        print(str(bytesCount) + " Bytes encoded, Total " + str(len(targetBinary)) + " Bytes")
        decodeCarry += decodedTemp
        decodedTemp = b''
    bytesCount += 1
    cbAddress = 256 * currentRound
    codebookFiltered = codebook[cbAddress:cbAddress + 256]
    decodedTemp += (codebookFiltered.index(b)).to_bytes(1, byteorder='big')
    countRound += 1

decodeCarry += decodedTemp
if compressed:
    decodeCarry = decompress(decodeCarry)

fxf = open(argv[3], 'wb')
fxf.write(decodeCarry)
fxf.close()

print("written " + str(len(decodeCarry)) + " Bytes")
print("done")
