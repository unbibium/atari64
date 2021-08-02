TARGET = target


all: roms

roms: roms.a65 kernal/* basic/*
	dasm roms.a65 -oroms -f3 -lroms.lst -sroms.sym

$(shell  mkdir -p $(TARGET))

