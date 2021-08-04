#!/usr/bin/env python3
#
# Convert dasm -f2 output into an Atari DOS object file

import sys

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

with open(sys.argv[1],'rb') as fi, open(sys.argv[2],'wb') as fo:
    fo.write(b'\xff\xff')  # header magic number
    while True:
        startWord = fi.read(2)
        if not startWord:
            print( "not startWord:", repr(startWord))
            break
        startAddr = to_int(startWord)
        chunkSize = to_int(fi.read(2))
        endAddr = startAddr+chunkSize-1
        print("%4x-%4x" % (startAddr,endAddr))
        fo.write(startWord)
        fo.write(to_bytes(endAddr))
        fo.write(fi.read(chunkSize))
    print("done")



    
    pass

