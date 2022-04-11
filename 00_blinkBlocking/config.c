#include "stm32f4xx.h"
#include "config.h"

void gpioInit(void){
  RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN;			// to enable GPIO port D
  __asm("dsb");                   //stall CPU pipeline until the instruction is completed: dm00037591
  GPIOD->MODER |= (1<<LED*2);		// GPIO port D mode register>> output port 15
  GPIOD->OTYPER &= ~(1<<LED);		// GPIO D Output type register, push pull, clearing bit
  GPIOD->OSPEEDR |= 0x00;		// GPIO D output Speed register>> low speed
  GPIOD->PUPDR |= 0x00;		// GPIO D port pull up/down register
}
//GPIOD->ODR &= 0x00000000;	// GPIO output data
