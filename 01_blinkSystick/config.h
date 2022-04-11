
void gpioInit(void);

/********************SysTick**************************/
// Func prototypes
void SysTickInit(unsigned long period);

#define STK_CTRL  (*((volatile unsigned long *)0xE000E010))
#define SHPR3   (*((volatile unsigned long *)0xE000ED20)) //System handler priority register

#define STK_VAL_CURRENT     0xFFFFFF //current value
#define STK_CTRL_COUNTFLAG  0x01<<16 //1: if the timer returned 0 @bit16
#define STK_CTRL_CLKSOURCE  0x01<<2  //processor clock, @bit2, AHB/8|AHB
#define STK_CTRL_TICKINT    0x01<<1 //Counting down to zero to asserts the SysTick exception request
#define STK_CTRL_ENABLE     0x01    //counter enable, @bit0

#define STK_BASE &STK_CTRL
// #define STK_BASE 0xE000E010

typedef struct {
  volatile uint32_t CTRL;
  volatile uint32_t LOAD;
  volatile uint32_t VAL;
  volatile uint32_t CALIB;
} STK_Typedef;

#define STK ((STK_Typedef *)STK_BASE)
