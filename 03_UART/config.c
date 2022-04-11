#include "stm32f4xx.h"
#include "config.h"

void Uart2Config(void){
  RCC->APB1ENR |= RCC_APB1ENR_USART2EN; // Enable UART CLOCK
  RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;  // Enable GPIOA CLOCK

  GPIOA->MODER 	 |= GPIO_MODER_MODER2_1;   // Alternate Function for Pin PA2 (2<<4)
  GPIOA->MODER 	 |= GPIO_MODER_MODER3_1;   // Alternate Function for Pin PA3 (2<<6)

  USART2->CR1 = 0x00;   // Clear ALL
  USART2->CR1 |= (1<<13);   // UE = 1... Enable USART
  USART2->BRR = (7<<0) | (24<<4);   // Baud rate of 115200, PCLK1 at 45MHz
  USART2->CR1 |= (1<<2); // RE=1.. Enable the Receiver
  USART2->CR1 |= (1<<3);  // TE=1.. Enable Transmitter
}
