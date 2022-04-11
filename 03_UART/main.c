#include "stm32f4xx.h"
#include "config.h"
#include "comunicate.h"


void delay (uint32_t time){
	while (time--);
}

int main(void){
  Uart2Config();

  while(1){
    //send
    // UART2_SendString ('G');
    UART2_SendChar ('G');
    delay (100000000);

    //receive
    // buffer[indx] = UART2_GetChar ();
    // indx++;
    // if (indx>=30) indx = 0;
  }
}
