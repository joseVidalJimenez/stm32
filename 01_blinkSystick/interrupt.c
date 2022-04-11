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

//WaitForInterrupt: low power mode
void WaitForInterrupt(void){
	__asm  ("    WFI\n");
}

//ISR: do not rename
void SysTick_Handler(void) {
  GPIOD->ODR ^= (1<<LED);
}
