#include "stm32f4xx.h"
#include "config.h"

int main(void){
    gpioInit();

    unsigned int i = 0;
    while(1){
        GPIOD->ODR ^= (1<<LED);
        for(i=0;i<1000000;i++);
    }
}
