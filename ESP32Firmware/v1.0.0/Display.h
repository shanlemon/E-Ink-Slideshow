#ifndef __EPD_5IN65F_H__
#define __EPD_5IN65F_H__

#include "DEV_Config.h"

/**********************************
Color Index
**********************************/
#define BLACK   0x0	/// 000
#define WHITE   0x1	///	001
#define GREEN   0x2	///	010
#define BLUE    0x3	///	011
#define RED     0x4	///	100
#define YELLOW  0x5	///	101
#define ORANGE  0x6	///	110
#define CLEAN   0x7	///	111 

#define WIDTH       600
#define HEIGHT      448

class Display {
  public:
    static void Init(void);
    static void ShowImage(const UBYTE *image);
    static void Clear(UBYTE color);
    static void Sleep(void);
};

#endif
