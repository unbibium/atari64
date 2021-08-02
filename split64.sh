#!/bin/sh

dd bs=1024 count=8 <roms >rom.a000
dd bs=1024 skip=16 <roms >rom.e000

