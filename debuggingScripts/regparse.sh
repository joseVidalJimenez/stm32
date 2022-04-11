#!/bin/bash

FILE="../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Device/ST/STM32F4xx/Include/stm32f4xx.h"
cat ${FILE} | awk '$2 !~ /_BASE/ && \
                $1 ~ /#define/ && \
                $2 !~ /\(/ && \
                $2 !~ /^_/ && \
                !/defined/ && \
                !/endif/ && \
                !/ifdef/ && \
                !/STM32/ && \
                !/\// && \
                $2 !~ /TypeDef/ \
                {print $2}'
