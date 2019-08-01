#include "IT8951.h"

//-----------------------------------------------------------
//Host controller function 1---Wait for host data Bus Ready
//-----------------------------------------------------------
void LCDWaitForReady()
{
  uint8_t ulData = bcm2835_gpio_lev(HRDY);
  while(ulData == 0)
    {
      ulData = bcm2835_gpio_lev(HRDY);
    }
}

uint8_t spi_transfer(uint8_t val) {
  uint8_t rtn;

  //  printf("send: 0x%x\n", val);
  rtn = bcm2835_spi_transfer(val);

  return rtn;
}

void Write(uint16_t preamble, uint32_t count, uint16_t* values)
{
  LCDWaitForReady();

  bcm2835_gpio_write(CS,LOW);

  spi_transfer(preamble>>8);
  spi_transfer(preamble);

  LCDWaitForReady();

  for(uint32_t i=0; i<count; i++)
    {
      spi_transfer(values[i]>>8);
      spi_transfer(values[i]);
    }

  bcm2835_gpio_write(CS,HIGH);
}

void WritePackedPixelBytes(uint32_t count, uint8_t* pixels)
{
  uint16_t preamble = 0x0000;

  for(uint32_t i=0; i<count; i+=2) {

    LCDWaitForReady();

    bcm2835_gpio_write(CS,LOW);

    spi_transfer(preamble>>8);
    spi_transfer(preamble);

    LCDWaitForReady();

    spi_transfer(pixels[i+1]);
    spi_transfer(pixels[i]);

    bcm2835_gpio_write(CS,HIGH);
  }

}

void Read(uint16_t preamble, uint32_t count, uint16_t* values)
{
  LCDWaitForReady();

  bcm2835_gpio_write(CS,LOW);

  spi_transfer(preamble>>8);
  spi_transfer(preamble);

  LCDWaitForReady();

  spi_transfer(0);
  spi_transfer(0);

  LCDWaitForReady();

  for(uint32_t i=0; i<count; i++)
    {
      values[i] = spi_transfer(0x00)<<8;
      values[i] |= spi_transfer(0x00);
    }
  bcm2835_gpio_write(CS,HIGH);
}

//-----------------------------------------------------------
//Test function 1---Software Initial
//-----------------------------------------------------------
uint8_t IT8951_Init()
{
  if (!bcm2835_init())
    {
      printf("bcm2835_init error \n");
      return 1;
    }

  bcm2835_spi_begin();
  bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);   		//default
  bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);               		//default
  bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32);		//default

  bcm2835_gpio_fsel(CS, BCM2835_GPIO_FSEL_OUTP);
  bcm2835_gpio_write(CS, HIGH);

  return 0;
}

void IT8951_Cancel()
{
  bcm2835_spi_end();
  bcm2835_close();
}
