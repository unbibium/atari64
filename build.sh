#!/bin/sh

dasm roms.a65 -oroms -f3 -lroms.lst -sroms.sym $*
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

