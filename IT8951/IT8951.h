#ifndef _IT8951_H_
#define _IT8951_H_

#include <bcm2835.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define CS 				8
#define HRDY 	        24
#define RESET 	        17

uint8_t IT8951_Init(void);
void IT8951_Cancel(void);
void LCDWaitForReady(void);

#endif
