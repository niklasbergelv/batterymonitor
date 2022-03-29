#include <ArduinoJson.h>

int analogSoCInput = 1;
int analogVoltInput = 0;
float arduinoVoltage = 4.61;
int delaytime = 10000;
StaticJsonDocument<48> doc;

void setup() {
    pinMode(analogSoCInput, INPUT); //assigning the input port
    pinMode(analogVoltInput, INPUT); //assigning the input port
    Serial.begin(9600);
    //while (!Serial) {
    //; // wait for serial port to connect. Needed for native USB port only
    //}
}

float measureVoltage(int analogInput) {
    float Vout = 0.00;
    float Vin = 0.00;
    float R1 = 100000.00; // resistance of R1 (100K) 
    float R2 = 10000.00; // resistance of R2 (10K) 
    int val = 0;
  
    val = analogRead(analogInput);//reads the analog input
    Vout = (val * arduinoVoltage) / 1024.00; // formula for calculating voltage out i.e. V+, here 5.00
    Vin = Vout / (R2/(R1+R2)); // formula for calculating voltage in i.e. GND
    if (Vin<0.09) {//condition
        Vin=0.00;//statement to quash undesired reading !
    }
    return Vin;
}

void loop() {
    doc["voltage"] = measureVoltage(analogVoltInput);
    doc["soc"] = measureVoltage(analogSoCInput);
    serializeJson(doc, Serial);
    Serial.println();
    delay(delaytime); //for maintaining the speed of the output in serial moniter  
}
