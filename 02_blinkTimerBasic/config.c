#include "stm32f4xx.h"
#include "config.h"
#include "pins.h"

/*
Initializing LED
*/
void gpioInit(void){
  RCC->AHB1ENR |= RCC_AHB1ENR_GPIODEN;			// to enable GPIO port D
  __asm("dsb");                   // No instruction in program instruction executes until previous instruction completes
  GPIOD->MODER |= (1<<LED*2);		// GPIO port D mode register>> output port 15
  GPIOD->OTYPER &= ~(1<<LED);		// GPIO D Output type register, push pull, clearing bit
  GPIOD->OSPEEDR |= 0x00;		// GPIO D output Speed register>> low speed
  GPIOD->PUPDR |= 0x00;		// GPIO D port pull up/down register
  GPIOD->ODR ^= (1<<LED);
}

/*
Check:
  Bit definition for TIM_CR1 register@stm32f4xx.h

NVIC_IPR13
*/

void timerInit(void){
  RCC->APB1ENR |= RCC_APB1ENR_TIM6EN;
  __asm("dsb");    // No instruction in program instruction executes until previous instruction completes

  NVIC_IPR13 |= (PRIORITY<<SHIFT);
  NVIC_ISER1 |= (uint32_t) ISERVAL; //1<<22

  // Set priority level 1 for TIM6 interrupt
	// NVIC_SetPriority(TIM6_DAC_IRQn, 1);
	// Enable TIM6 interrupts
	// NVIC_EnableIRQ(TIM6_DAC_IRQn);

  TIM6->PSC = (uint16_t) 48000 -1;  // Set TIM6 prescaler
  TIM6->ARR = (uint16_t) 200 -1;  // Set TIM6 auto-reload register
  TIM6->CR1 |= TIM_CR1_ARPE;  // Enable auto-reload preload

	TIM6->DIER |= TIM_DIER_UIE; // Enable Interrupt upon Update Event
	TIM6->CR1 |= TIM_CR1_CEN;  // Start TIM6 counter
}
