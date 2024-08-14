// Matthew Buzalsky, Colby Connolly
// 7/13/2024
// Anemometer and Solar project
// Introduction to Renewable Energy

#include <LiquidCrystal.h>

// Define data pins

#define BAUD_RATE 9600
#define solar_pin A0
#define anemometer_pin A1

// LCD pins

int DB4 = 5;
int DB5 = 4;
int DB6 = 3;
int DB7 = 2;
int reg_select = 12;
int enable = 11;

// Define LCD display

LiquidCrystal lcd(reg_select, enable, DB4, DB5, DB6, DB7);

void setup() {
  // put your setup code here, to run once:
  // Initialize Serial Monitor
  Serial.begin(BAUD_RATE);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Solar data

  // Uses voltage divider to provide higher voltage values above 5V
  // R1 = 100k ohm and R2 = 10k ohm
  
  long r1 = 100000;
  int r2 = 10000;
  
  // Rated current through solar panels is 160 mA

  float current = 0.160;

  int solar_adc = analogRead(solar_pin);

  float solar_voltage = solar_adc * (5.0/1023);

  float adjusted_voltage = solar_voltage * ((r1 + r2)/r2);

  float power = adjusted_voltage * current;

  // Wind data

  int wind_adc = analogRead(anemometer_pin);

  float wind_voltage = wind_adc * (5.0/1023);

  // Wind speed calculation

  float wind_speed;

  if (wind_voltage <= 0.4) {
    wind_speed = 0;
  }
  else {
    wind_speed = map_number(wind_voltage, 0.4, 2.0, 0, 32.4);
  }

  // Print results to Serial Monitor
  
  Serial.print("Solar(W): ");
  Serial.print(power);
  Serial.print(", Wind: ");
  Serial.print(wind_voltage);
  Serial.print("V, ");
  Serial.print(wind_speed);
  Serial.println(" m/s");

  // Update LCD

  lcd.begin(16,2);

  lcd.setCursor(0,0);

  // Print first row (solar data)

  lcd.print("Solar: ");
  lcd.print(power);
  lcd.print(" W");

  // Print second row of data (wind data)

  lcd.setCursor(0,1);

  lcd.print("Wind: ");
  lcd.print(wind_speed);
  lcd.print(" m/s");

  // Delay for 1 second

  delay(1000);

}

// Map float data types into specific range
float map_number(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
