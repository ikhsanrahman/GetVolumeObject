//defines pins
const int stepPin = 4;  //PUL -Pulse
const int dirPin = 5; //DIR -Direction
const int enPin = 6;  //ENA -Enable

void setup(){
  //Sets the pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);
  Serial.begin(9600);
}

void loop(){
  //Enables the motor direction to move
    digitalWrite(dirPin,HIGH);
    //Makes 200 Pulses for making one full cycle rotation
    for(int x = 0; x < 1300; x++){
      digitalWrite(stepPin,HIGH);
//      Serial.print(x);
//      delayMicroseconds(100); 
      digitalWrite(stepPin,LOW); 
//      delayMicroseconds(100); 
  }
  
    //One second delay
//      delay(1000);

  //Changes the rotations direction
    digitalWrite(dirPin,LOW);
  
  // Makes 200 pulses for making one full cycle rotation
    for(int x = 0; x <1300; x++) {
      digitalWrite(stepPin,HIGH);
//    delayMicroseconds(100);
      digitalWrite(stepPin,LOW);
//    delayMicroseconds(100);
    }
  
    //One second delay
//      delay(1000);   

}
