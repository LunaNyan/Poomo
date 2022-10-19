from core.poomoRead import poomoRead
from sys import argv, exit
from zlib import compress

if len(argv) > 5 or len(argv) < 4:
    print("Usage : poomoEncode.py [poomo] [target] [output] (nocomp)")
    exit(1)

# Open Poomo
poomo = open(argv[1], 'rb')
codebook = poomoRead(poomo)

# Open Target File
targetFile = open(argv[2], 'rb')
readCarry = targetFile.read()

compressed = True

# Compress It
if len(argv) == 5:
    if argv[4].lower() == "nocomp":
        zCarry = readCarry
        compressed = False
    else:
        zCarry = compress(readCarry, -1)
        print("Compressed Size : " + str(len(zCarry)) + " Bytes")
else:
    zCarry = compress(readCarry, -1)
    print("Compressed Size : " + str(len(zCarry)) + " Bytes")

# Ready for Encode
encodeCarry = b''
encodedTemp = b''

currentRound = 0
countRound = 0
bytesCount = 0

print("Encode Start")

for b in zCarry:
    if countRound == 7:
        if currentRound == 3:
            currentRound = 0
        else:
            currentRound += 1
        countRound = 0
    # Checkpoint
    if bytesCount % 16384 == 0:
        print("Checkpoint : " + str(encodedTemp[:16]))
        print(str(bytesCount) + " Bytes encoded, Total " + str(len(readCarry)) + " Bytes")
        encodeCarry += encodedTemp
        encodedTemp = b''
    bytesCount += 1
    cbAddress = 256 * currentRound
    codebookFiltered = codebook[cbAddress:cbAddress + 256]
    encodedTemp += codebookFiltered[b].to_bytes(1, byteorder='big')
    countRound += 1

# Reverse It
reversedCarry = bytearray(encodeCarry + encodedTemp)
reversedCarry.reverse()

# Add Magic
if compressed:
    cmpMagic = bytes(3) + b'CP'
else:
    cmpMagic = bytes(5)

realCarry = b'EPUMO' + cmpMagic
realCarry += len(reversedCarry).to_bytes(10, byteorder='big')
realCarry += bytes([255] * 80)
realCarry += reversedCarry
realCarry += bytes([255] * 10)
realCarry += b'FUTAGOHIME'

print("written " + str(len(reversedCarry)) + " Bytes")

# Save
fxf = open(argv[3], 'wb')
fxf.write(realCarry)
fxf.close()

print("done")
