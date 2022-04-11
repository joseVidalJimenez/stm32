#include "stm32f4xx.h"
#include "config.h"
#include "pins.h"

/*
output data written to: GPIOD->ODR
*/
void gpioInit(void){
  RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN;			// to enable GPIO port D
  __asm("dsb");                   // No instruction in program instruction executes until previous instruction completes
  GPIOD->MODER |= (1<<LED*2);		// GPIO port D mode register>> output port 15
  GPIOD->OTYPER &= ~(1<<LED);		// GPIO D Output type register, push pull, clearing bit
  GPIOD->OSPEEDR |= 0x00;		// GPIO D output Speed register>> low speed
  GPIOD->PUPDR |= 0x00;		// GPIO D port pull up/down register
}


void SysTickInit(unsigned long period){
  STK->CTRL = 0;  //disable before setup
  STK->LOAD = period-1;  // delay time
  STK->VAL = 0; // any value written to val clears it
  SHPR3 = (SHPR3&0x00FFFFFF)|0x20000000; // set priority 1
  STK->CTRL |= (STK_CTRL_CLKSOURCE|STK_CTRL_TICKINT|STK_CTRL_ENABLE);      // enable SysTick with core clock and exception request
}
