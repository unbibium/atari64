OH GOD WHAT ARE YOU DOING
=========================

I'm compiling the Commodore 64 kernal to run on the Atari 800XL.
They're practically the same machine; why didn't someone try
this 30 years ago?

HOW TO BUILD
============

You will need bash, dasm, and Python 3.

You can get dasm at https://github.com/dasm-assembler/dasm/

Run `./build.sh` and it should do everything.

WHAT YOU GET
============

* `rom.a000` an 8K BASIC ROM
* `rom.d800` a 10K ROM containing PETSCII font and OS
* `atari64.xex` an executable that you can load into an 800XL.
  It will copy itself behind the ROM and run from RAM.
  I patched the `RAMTAS` section so it doesn't think the BASIC
  area is free for BASIC programs.

HOW TO RUN
==========

To run it in the emulator as if you'd taken an Atari 800's ROMs and
swapped them out with these: 
* `atari800 -config atari64.cfg`
You can extrapolate this to decide how to run it on real hardware.

WHAT IT DOES
============

The keyboard, the PETSCII screen editor, and BASIC work.

Use the BREAK key to stop a running BASIC program.  you'll note
it doesn't work while an `INPUT` statement is running.
I'll get the RESET button working real soon.

The Atari logo key will type the pi character.

Shift-Atari logo will switch between uppercase-graphics and
lowercase-uppercase character set.

Still missing:
* RESET button
* A way to type the Commodore-logo graphics characters
* Any I/O whatsoever: tape, disk, printer, RS232... 

WHY
===

lol

