/*
notes:
  TIM6_DAC_IRQn = 54 (stm32f4xx.h)

IPRx register value = IRQ# MOD 4
  54%4=2 (reminder)
    byte offset = 8*reminder, (reminder = 0 to 3)
    hex(1<<8*2)

x in IPRx: (base address 0xE000E400)
  x = 54/4 = 13
  Address offset: 0x04 * x, (x = 0 to 59)
    hex(0x04*13)=34

IPR:
  0xE000E434:	0x00100000 //1<<8*2

A programmable priority level of 0-15 for each interrupt:
  A higher level corresponds to a lower priority, so level 0 is the highest interrupt priority

*/


//********************* Definition for TIM6
#define NVIC_IPR13  (*((volatile unsigned long *)0xE000E434))   //IRQ54:TIM6
#define PRIORITY 16 //max priority
#define SHIFT 8*2  //4 block of 8 bits each

#define NVIC_ISER1   (*((volatile unsigned long *)0xE000E104))   //
#define IRQTIM6 54
#define ISERVAL 1<<(IRQTIM6 & 0x1F)

void gpioInit(void);
void timerInit(void);
