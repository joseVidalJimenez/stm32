#include "stm32f4xx.h"
#include "config.h"
#include "interrupts.h"

int main(){
  DisableInterrupts();
  gpioInit();
  timerInit();
  EnableInterrupts();
  while(1){
    WaitForInterrupt();
  }
}
