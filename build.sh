#!/bin/bash

dasm roms.a65 -oroms -f3 -lroms.lst -sroms.sym $*
# convert dasm symbols to atari800 labels
awk '{print $2, $1}' <roms.sym >roms.lbl

result=$?
if [[ result -ne 0 ]]
then
	echo "stopping because dasm returned $result" >/dev/stderr
	exit $result
fi

# 8k rom containing most of basic
dd bs=1024 count=8 <roms >rom.a000
# 10k rom containing chargen and kernal
dd bs=1024 skip=14 <roms >rom.d800

# try to build xex

dasm xex.a65 -oatari64.o -f2
./toxex.py atari64.o atari64.xex

# build any prg files in the current directory

for PRGFILE in *.prg
do
	./prg2obj.py ${PRGFILE} ${PRGFILE%.prg}.obj
done
