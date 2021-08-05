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

Known issues:
* if the C64 OS is in RAM, RESET reboots the original Atari OS.
  Supposedly the old Translator disk got around this somehow.
* need to find a way to type the Commodore-logo graphics characters.
  The Atari logo key doesn't work as a qualifier, but might work as
  a dead key.  or i could use START/SELECT/OPTION.
* no way yet to save or load BASIC programs
* there's no I/O at all actually

WHY
===

Recently the 8-Bit Guy did a video about the Apple 1 computer, and
how you can simulate an Apple 1 with a Commodore 64 program that just
reproduces the terminal I/O and runs the programs natively.  It got
me thinking, why couldn't I do the same thing with two other machines?
The Atari 800XL and Commodore 64 have such similar memory maps and
ROM switching capabilities that it seemed my best bet was to try to
compile the CBM KERNAL on the Atari 800XL and see how much I could
get to work.

i wonder if I've hit the wall or if some mad genius will figure out
how to wire a real Datasette in there and run actual PET programs.

ACKNOWLEDGEMENTS
================

* CBM source code: https://github.com/mist64/cbmsrc

