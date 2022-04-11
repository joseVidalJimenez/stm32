#include "stm32f4xx.h"
#include "pins.h"

//DisableInterrupts
void DisableInterrupts(void){
	__asm ("    CPSID  I\n");
}

//EnableInterrupts
void EnableInterrupts(void){
	__asm  ("    CPSIE  I\n");
}

//WaitForInterrupt
void WaitForInterrupt(void){
	__asm  ("    WFI\n");
}

void TIM6_DAC_IRQHandler()
{
	// Test for TIM6 update pending interrupt
	if ((TIM6->SR & TIM_SR_UIF) == TIM_SR_UIF)
	{
		// Clear pending interrupt flag
		TIM6->SR &= ~TIM_SR_UIF;

		// Do what you need
		GPIOD->ODR ^= (1<<LED);
	}
}
