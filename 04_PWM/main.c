#include "stm32f4xx.h"
#include "config.h"


int main(void){
  gpioInit();
  SysTickInit(period);
  EnableInterrupts();
  while(1){
    WaitForInterrupt();
  }
}
