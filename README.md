Atari 64
=========================

This is the Commodre 64 KERNAL, modified to run on the Atari 8-bit
line of computers. 
They're practically the same machine; why didn't someone try
this 30 years ago?

HOW TO BUILD
============

Working XEX file and ROM image can be downloaded at the release page:
https://github.com/unbibium/atari64/releases

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

The `atari64.xex` should run from any DOS or boot loader.

WHAT IT DOES
============

The keyboard, the PETSCII screen editor, and BASIC work.

Use the BREAK key to stop a running BASIC program.  you'll note
it doesn't work while an `INPUT` statement is running.
I'll get the RESET button working real soon.

The Atari logo key will type the pi character.

Shift-Atari logo will switch between uppercase-graphics and
lowercase-uppercase character set.

Hold the OPTION, SELECT, or START key to type the graphics
characters you'd ordinarily type with the Commodore logo key.

If a lot of text is scrolling by, you can hold the OPTION key
to slow down the scrolling, like you would hold down CTRL on
a real C64.

Known issues:
* if the C64 OS is in RAM, RESET reboots the original Atari OS.
  Supposedly the old Translator disk got around this somehow.
* no way yet to save or load BASIC programs
* there's no I/O at all actually
* PETSCII color will never work.

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

HOW
===

I used mist64's `cbmsrc` project as a starting point.  The first
thing I had to do was reformat the C64 KERNAL and BASIC's source
code so that it would compile in DASM.  I wrote a python script
for that, but still had to manually add segment definitions and
such, so that it would compile neatly.

Next, I had to make sure I could actually run these ROMs at all
on an Atari emulator.  The 8K BASIC ROM was straightforward enough,
and the original Atari 800 used 10K of ROM.  I used the extra 2K
for the chargen ROM, which only needs half the space because it
doesn't include the reverse characters.  I worked out how to
configure atari800 to run it -- if I got a black screen, I'd
press F8 and look around in the monitor to make sure everything
was there.

Next I rewrote the code that set up the screen and I/O.  I'd
add declarations to `kernal/declare` as I went.  I hard-coded
an ANTIC display list in ROM to point to where the C64 usually
draws the screen at $0400.  I'd rewrite the screen initialization
code to set up ANTIC and GTIA to point to that display list.
Once I got that working, I found it was already displaying the
C64 BASIC V2 splash screen.  The cursor wasn't blinking, and
of course the keyboard didn't work, but I could feed PETSCII
characters into the keyboard buffer through the monitor, and
I tested a few BASIC commands that way.

Getting the cursor to blink was my next task.  I looked at all
the Atari documentation I could find to figure out how the
vertical blank interrupt worked.  I was setting the right
flags, but nothing worked, until I realized that the vertical
blank is an NMI in the Atari.  On the Commodore it's an IRQ.
So I switched the addresses at $FFFA and $FFFE, and that got
me much closer.

I rewrote the keyboard scan routine to handle the Atari
keyboard, and removed most of the color code from the screen
editor.  

I also had to modify BASIC's `RND(0)` function to draw from the POKEY
instead of the CIA chips.  The lack of a CIA/POKEY equivalent on the
DCPU-16 is probably why I had to use `RND(1)` in my demo video
instead.

Currently, there's no I/O outside of the screen and keyboard
whatsoever.  I've torn out all the rs232 code to make room for 
other people to attempt stuff, even though the 800XL has a larger 
ROM space to work in already.  I'll leave the tape code in just 
because I have a hunch that isn't a total lost cause yet, but it's 
only a hunch.

LOADING PROGRAMS
================
There is one way to load programs, though it's a bit hacky.  Inspired
by a similar project called "c800", I found a way to pre-load programs
such that Atari 64 will boot into them.

    ./prg2obj file.prg file.xex

This will create a program in XEX format that just loads the program into
a segment of memory that isn't going to be used for anything else.  So,
if you load the resulting XEX file before you load Atari64, it will copy
that program to the proper place in the C64 memory map so that you can
RUN it right away.  If you see the word LOADING, it has detected and
loaded this program.

I made this in kind of a hurry so that I could show this off in public,
so it's limited, will not work on programs more than 8700 bytes, 
and the python script has to run in the same directory as roms.sym.  
Improvements will appear in future versions.

Sample programs include:
* dungeon.prg: PET dungeon ported to C64 with minor changes to make the joystick work on Atari
* pm1.prg: using CBM BASIC to do Atari player/missile graphics

ACKNOWLEDGEMENTS
================

* CBM source code: https://github.com/mist64/cbmsrc

