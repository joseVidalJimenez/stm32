#include "stm32f4xx.h"
#include "config.h"
#include "interrupt.h"
#define __Vendor_SysTickConfig    1 //used in:stm32f4xx.h

const int period = 16777215;

int main(void){
  gpioInit();
  SysTickInit(period);
  EnableInterrupts();
  while(1){
    WaitForInterrupt();
  }
}
