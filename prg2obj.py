#!/usr/bin/env python3
#
# Convert CBM BASIC file to an Atari OBJ file relocated to $2000
# for preloading to Atari

import sys
import os

PREAMBLE=b"CBM\0"
C64_START=0x0801

# get atari_start from symbol table if it exists
if os.path.exists("roms.sym"):
    with open('roms.sym') as fi:
        for line in fi.readlines():
            if "PRG_SOURCE" in line:
                ATARI_START = int(line.split()[1], 16)+1
                break
        else:
            print("run build.sh before running this")
            sys.exit(1)


def to_int(word):
    if type(word) is not bytes: raise TypeError
    if len(word) != 2: raise ValueError
    return word[0] + word[1]*256

def to_bytes(i):
    if type(i) is not int: raise TypeError
    if i < 0 or i > 65535: raise ValueError
    return bytes([ i % 256, i // 256 ])

assert to_int(b'\xff\xff') == 65535
assert to_bytes(65535) == b'\xff\xff'

assert to_int(b'\x02\x01') == 258
assert to_bytes(259) == b'\x03\x01'

if len(sys.argv) < 3:
    print("Usage:",sys.argv[0],"infile outfile")
    sys.exit(1)

print("converting %r to %r" % (sys.argv[1], sys.argv[2]))

# for PET programs we may need to re-address everything
# i'm having a little trouble making the built-in relocator work
def apply_offset(petBytes, offset):
    c64Bytes = bytes()
    petAddr = C64_START+offset
    print("relocating PET/VIC program from %4x" % petAddr)
    c64Addr = C64_START
    ptr = 0
    while ptr < len(petBytes):
        nextPetAddr = to_int(petBytes[ptr:ptr+2])
        if nextPetAddr == 0:
            print("BASIC ends at %x" % nextC64Addr)
            return c64Bytes + petBytes[ptr:]
        nextC64Addr = nextPetAddr - offset
        lineNum = to_int(petBytes[ptr+2:ptr+4])
        print("moving end of line %d (%d bytes) from %04x to %04x" % (lineNum, nextPetAddr-petAddr, nextPetAddr, nextC64Addr))
        nextPtr = ptr + (nextPetAddr - petAddr)
        c64Bytes += to_bytes(nextC64Addr) + petBytes[ptr+2:nextPtr]
        ptr = nextPtr
        petAddr = nextPetAddr
        c64Addr = nextC64Addr
    print("oh no, relocating went off the edge")
    print("ptr=%d len(petBytes)=%d" % (ptr, len(petBytes)))
    sys.exit(3)


# main program

with open(sys.argv[1],'rb') as fi:
    startAddr = to_int(fi.read(2))
    if(startAddr & 0xFF != 1):
        print("probably not CBM BASIC, starting word is %x" % startAddr)
        sys.exit(2)
    offset=startAddr - C64_START
    if offset != 0:
        print("WARNING: may be CBM BASIC for a different machine")
    sourceBytes = fi.read()
    if sourceBytes[9] == 0x9E:
        if offset != 0:
            print("cannot relocate machine language from another machine")
            sys.exit(4)
        print("WARNING: SYS on first line. may be ML and unlikely to work on Atari")

if offset != 0:
    sourceBytes = apply_offset(sourceBytes, offset)

dstBytes = PREAMBLE + sourceBytes
dstStart = ATARI_START - len(PREAMBLE)
dstEnd = dstStart + len(dstBytes) -1
print("%4x-%4x (%d bytes)" % (dstStart, dstEnd, len(dstBytes)))

# consider further validation

with open(sys.argv[2],'wb') as fo:
    fo.write(b'\xff\xff')  # header magic number
    fo.write(to_bytes(dstStart))
    fo.write(to_bytes(dstEnd))
    fo.write(dstBytes)
    print("done writing OBJ file")

