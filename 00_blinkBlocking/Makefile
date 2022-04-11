#########################
# Attemt to create a bare-metal project using register only model
# Architechture: STM32F407
# Specs:

# Notes:
# To be compiled from a Linux machine
#########################
# Binary firmware name
FW_NAME = blink
#########################
# Binaries
CC = arm-none-eabi-gcc
AS = arm-none-eabi-as
LD = arm-none-eabi-ld
BIN = arm-none-eabi-objcopy
GDB ?= arm-none-eabi-gdb
GDBPY ?= arm-none-eabi-gdb-py
STL ?= st-flash
#########################
# Linker Script
LDSCRIPT = ../LINKER/stm32_flash.ld
#LDSCRIPT = ../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Project/STM32F4xx_StdPeriph_Templates/TrueSTUDIO/STM32F40_41xxx/STM32F417IG_FLASH.ld
#########################
# Config file and startup script
SYSTEM = ../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Device/ST/STM32F4xx/Source/Templates/system_stm32f4xx.c
STARTUP = ../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Device/ST/STM32F4xx/Source/Templates/gcc_ride7/startup_stm32f40xx.s
HEADER = ../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Device/ST/STM32F4xx/Include/stm32f4xx.h
#########################
# Define all object files
SRC := $(shell find $(./) -name '*.c')
OBJ = $(SRC:.c=.o) startup_stm32f40xx.o system_stm32f4xx.o
#########################
# Include paths
INC = -I../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Include/ #core_cm4.h
INC += -I../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Device/ST/STM32F4xx/Include/ #stm32f4xx.h, system_stm32f4xx.h
#########################
# MCU Flags
MCFLAGS = -mthumb -mcpu=cortex-m4 -march=armv7e-m -mlittle-endian -mfloat-abi=hard -mfpu=fpv4-sp-d16
# Compile flags
CFLAGS = -std=gnu11 -O0 -gdwarf-4 -g3 -Wall -Wextra --specs=nosys.specs -save-temps
DEFS += -DSTM32F40_41xxx -DUSE_HAL_DRIVER
CFLAGS += $(MCFLAGS) $(DEFS) $(INC)
#########################
# Linker flags (LD vs GCC)
LDFLAGS = -Wall -T$(LDSCRIPT) $(MCFLAGS) -Wl,-Map=$(FW_NAME).map,--gc-sections,-u,Reset_Handler -ffunction-sections -fdata-sections --specs=nosys.specs
#########################

all: $(FW_NAME).bin

startup_stm32f40xx.o: $(STARTUP)
	$(CC) -c $< -o $@ $(CFLAGS)
	@echo ">>>Compiled: "$<"\n"

system_stm32f4xx.o: $(SYSTEM)
	$(CC) -c $< -o $@ $(CFLAGS)
	@echo ">>>Compiled: "$<"\n"

%.o: %.c
	$(CC) -c $< -o $@ $(CFLAGS)
	@echo ">>>Compiled: "$<"\n"

$(FW_NAME).elf: $(OBJ)
	$(CC) $(LDFLAGS) -o $(FW_NAME).elf $(OBJ)
	@echo ">>>Linked file: "$<"\n"

$(FW_NAME).bin: $(FW_NAME).elf
	$(BIN) -O binary $^ $@
	@echo ">>>Bin file created: "$<"\n"

clean:
	rm -f *.o *.i *.elf *.map *.h.gch *.bin *.s
	@echo ">>>Clean \n"

flash: $(FW_NAME).bin
	$(shell killall arm-none-eabi-gdb-py arm-none-eabi-gdb openocd)
	$(STL) write $(FW_NAME).bin 0x8000000


reset:
	$(STL) reset

ocdserver:
	@echo ">>>Running OpenOcd server... \n"
	@echo ">>>type ona a separate window:\n"
	@echo "		arm-none-eabi-gdb -q blink.elf\n"
	@echo ">>>type in gdb:\n"
	@echo "		target remote localhost:3333\n"
	@echo "Or simply: make gdbconnect \n"
	openocd -f board/stm32f4discovery.cfg

gdbconnect:
	$(GDB) -q -ex "target remote localhost:3333" -ex "monitor reset init" -ex "monitor halt" -ex "break main" $(FW_NAME).elf

gdbconnectpy:
	$(GDBPY) -q -ex "target remote localhost:3333" -ex "monitor halt" $(FW_NAME).elf

.PHONY: clean flash reset ocdserver gdbconnect gdbconnectpy
