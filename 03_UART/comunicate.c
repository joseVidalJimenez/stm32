#include "stm32f4xx.h"

void UART2_SendChar (char c){
	/*********** STEPS FOLLOWED *************

	1. Write the data to send in the USART_DR register (this clears the TXE bit). Repeat this
		 for each data to be transmitted in case of single buffer.
	2. After writing the last data into the USART_DR register, wait until TC=1. This indicates
		 that the transmission of the last frame is complete. This is required for instance when
		 the USART is disabled or enters the Halt mode to avoid corrupting the last transmission.

	****************************************/

	USART2->DR = c;   // LOad the Data
	while (!(USART2->SR & (1<<6)));  // Wait for TC to SET.. This indicates that the data has been transmitted
}


uint8_t UART2_GetChar (void){
		/*********** STEPS FOLLOWED *************

	1. Wait for the RXNE bit to set. It indicates that the data has been received and can be read.
	2. Read the data from USART_DR  Register. This also clears the RXNE bit

	****************************************/
	uint8_t Temp;

	while (!(USART2->SR & (1<<5)));  // Wait for RXNE to SET.. This indicates that the data has been Received
	Temp = USART2->DR;  // Read the data.
	return Temp;
}
