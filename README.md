# STM32 Playground

## Motivation:
I wrote this project in order to learn how to use the arm tool chain using the command line to program and debug ARM STM32 microcontrollers.
I originally I wanted to use the learning methodology called building blocks, so the project numbering resembles the knowledge stacking from one project to the next.
		
## Challenges:
My previous experience with microcontrollers it was using keil microvision IDE.
At the beginning of the project, all what I wanted was to reach that stage where you build your application, and from there on troubleshoot my own code. However this road took longer than expected, I had to learn how to write makefiles, gain some understanding of link files, and how to debug using gdb. Moreover, to make my life "easier" I decided that I wanted to use the register model, so no: CMSIS, libraries, etc.

## Setup:
* [Virtual box](https://www.virtualbox.org/)
* [Ubuntu](https://ubuntu.com/#download)
* [Arm GNU Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
* [stm32f407 discovery board](https://www.st.com/en/evaluation-tools/stm32f4discovery.html)
		
## Learning outcomes:
How to run automatic test using the built-in Python interpreter and gdb
Create custom rules on make files
Improve git skills
Debug using gdb
Write makefiles
