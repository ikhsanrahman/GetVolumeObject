#include "HX711.h"

#define DOUT  A0
#define CLK  A1
HX711 scale(DOUT, CLK);
float calibration_factor = -70.90;
int GRAM;

void setup() {
  Serial.begin(9600);
  scale.set_scale();
  scale.tare();
}

void loop() {
  scale.set_scale(calibration_factor);
  GRAM = scale.get_units(), 4;
  Serial.println(GRAM);
}
