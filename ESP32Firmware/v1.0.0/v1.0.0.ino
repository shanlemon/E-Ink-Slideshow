#include "DEV_Config.h"
#include "Display.h"
#include "ImageData.h"
#include <stdlib.h>

void setup() {
    // Init
    DEV_Module_Init();
	Display::Init();
  
    // Main
	Display::ShowImage(image);
	DEV_Delay_ms(5000); 


	printf("Sleep...\r\n");
	Display::Sleep();
}

void loop() {
  // Will Not occur
}
