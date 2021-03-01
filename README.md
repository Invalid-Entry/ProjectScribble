# ProjectScribble
Code for a completely home-made V wall plotter.

This repo is a bit of a mono-repo containing multiple sub-projects and libraries.
Because its a prototyping project, various extra libraries are needed.

# Code

* `Arduino/` Contains the code that goes onto the arduino
* `Notebooks/` Contains various Jupyter notebooks that were used in prototyping

# Running the code

* Need an arduino mega, with a ramps shield, and the Accelstepper lib.
* Notebooks require various libraries (such as PIL), but should be used for reference.

# Protocol Information

* The control characters are Ascii and the numbers are Big Endian.
* Serial connection with baud is 115200 (standard Arduino serial interface).
* Bytes have 8 bits in this system.


`AXXXX` where XXXX is a unsigned 4 byte integer. Sets the target length of the A (left) wire from home.
`BXXXX` where XXXX is a unsigned 4 byte integer. Sets the target length of the B (right) wire from home. 
`G` is Go (start) the motors moving.
`S` is Stop (stop it moving mid movement) - currently doesn't work due to stepper motor.
`X` is pen Down (X makes the mark)
`C` is Pen Up (Clear pen)
`D` is Debug
`R` is 'you are at home, reset your coordinates'. Note this does not reset the target, so use with A0x00000000 and B0x00000000

New line characters are ignored (unless one is in the 4 bytes after an `A` or `B` command).
The replies are desgined to be one per line, seperated with `\r\n`. If the line starts with a `!--` it is a comment for a human.
At the moment, there is only these comments, and :. detection of 'reached path' should be done by looking for the word 'end' in the comment.