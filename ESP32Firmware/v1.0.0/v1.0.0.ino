#include "DEV_Config.h"
#include "Display.h"
#include "ImageData.h"
#include <WiFiManager.h>
#include <stdlib.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

void setup() {  
  // Init
  DEV_Module_Init();
	Display::Init();

  WiFiManager wm;
  bool res;
  res = wm.autoConnect("E-Ink Display");

  if (!res) {
    Serial.println("Failed to connect");
    return;    
  } else {
    Serial.println("connected..");
  }

  String serverPath = "https://mocki.io/v1/8215250a-db6b-4a1b-9e00-1fb242c61a45";
  HTTPClient http;
  http.begin(serverPath.c_str());
  http.addHeader("Content-Length", "179217");
  
  int httpResponseCode = http.GET();
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    const String& payload = http.getString();
    
    Serial.println("printing payload...");
    
    Serial.println(payload);
    JSONVar my_obj = JSON.parse(payload);
    if (JSON.typeof(my_obj) == "undefined") {
      Serial.println("Parsing input failed!");
      return;
    }
    Serial.print("JSON object = ");
    Serial.println(my_obj);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  
    // Main
//	Display::ShowImage(image);
//	DEV_Delay_ms(5000); 
//
//
//	printf("Sleep...\r\n");
//	Display::Sleep();
}

void loop() {
  // Will Not occur
}
