#include "Display.h"

static void Reset(void) {
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(200);
    DEV_Digital_Write(EPD_RST_PIN, 0);
    DEV_Delay_ms(1);
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(200);
}

static void SendCommand(UBYTE Reg) {
    DEV_Digital_Write(EPD_DC_PIN, 0);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Reg);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

static void SendData(UBYTE Data) {
    DEV_Digital_Write(EPD_DC_PIN, 1);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Data);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}


static void BusyHigh(void) {
    // If BUSYN=0 then waiting
    while (!DEV_Digital_Read(EPD_BUSY_PIN));
}

static void BusyLow(void) {
    // If BUSYN=1 then waiting
    while (DEV_Digital_Read(EPD_BUSY_PIN));
}

void Display::Init(void) {
	Reset();
    BusyHigh();
    SendCommand(0x00);
    SendData(0xEF);
    SendData(0x08);
    SendCommand(0x01);
    SendData(0x37);
    SendData(0x00);
    SendData(0x23);
    SendData(0x23);
    SendCommand(0x03);
    SendData(0x00);
    SendCommand(0x06);
    SendData(0xC7);
    SendData(0xC7);
    SendData(0x1D);
    SendCommand(0x30);
    SendData(0x3C);
    SendCommand(0x41);
    SendData(0x00);
    SendCommand(0x50);
    SendData(0x37);
    SendCommand(0x60);
    SendData(0x22);
    SendCommand(0x61);
    SendData(0x02);
    SendData(0x58);
    SendData(0x01);
    SendData(0xC0);
    SendCommand(0xE3);
    SendData(0xAA);
	
	DEV_Delay_ms(100);
    SendCommand(0x50);
    SendData(0x37);
}

void Display::ShowImage(const UBYTE *image) {
    SendCommand(0x61);
    SendData(0x02);
    SendData(0x58);
    SendData(0x01);
    SendData(0xC0);
    SendCommand(0x10);

    for(int i = 0; i < HEIGHT; i++)
        for(int j = 0; j < WIDTH / 2; j++)
            SendData(image[i * WIDTH / 2 + j]);

    SendCommand(0x04);
    BusyHigh();
    SendCommand(0x12);
    BusyHigh();
    SendCommand(0x02);
    BusyLow();
    DEV_Delay_ms(200);
}

void Display::Clear(UBYTE color) {
    SendCommand(0x61);
    SendData(0x02);
    SendData(0x58);
    SendData(0x01);
    SendData(0xC0);
    SendCommand(0x10);

    for(int i = 0; i < HEIGHT; i++)
        for(int j = 0; j < WIDTH / 2; j++)
            SendData((color << 4) | color);

    SendCommand(0x04);
    BusyHigh();
    SendCommand(0x12);
    BusyHigh();
    SendCommand(0x02);
    BusyLow();
    DEV_Delay_ms(500);
}

void Display::Sleep(void) {
    DEV_Delay_ms(100);
    SendCommand(0x07);
    SendData(0xA5);
    DEV_Delay_ms(100);
	DEV_Digital_Write(EPD_RST_PIN, 0);
}
