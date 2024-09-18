//define pin numbers
const int trigPin = 9;
const int echoPin = 10;
const int ledPin = 13;
const int buzzerPin = 12;
#include "pitches.h"
int notes[] = {NOTE_C5, NOTE_E5};
int check = 0

//define variables
long duration;                          // long: used for extended size variables --> 32 bits (numbers -2,147,483,648 to 2,147,483,647)
int distance;

void setup() {
  pinMode(trigPin, OUTPUT);             // trigPin is Output (waves going out)
  pinMode(echoPin, INPUT);              // echoPin is Input (returning waves from trigPin)
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
    digitalWrite(trigPin, LOW);           // Make sure that trigPin values are clear. Only a 2 microsecond delay is required for this to be completed
    delayMicroseconds(2); 

    digitalWrite(trigPin, HIGH);          // To generate Ultra sound waves, trigPin is set to HIGH for 10 microseconds before being set back to LOW
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);    // pulseIn: reads the time that it takes for the sound wave to travel (reads the time it takes to go from HIGH to LOW to HIGH)
    distance = duration*0.034/2 ;         // Sounds travels at 0.034cm/microsecond and the wave travels to the object and then back, thus traveling the distance twice and muse be divided by 2
    Serial.print("Distance: ");           // Write distance in serial monitor
    Serial.print(distance);
    Serial.print(" cm");
    Serial.println();
    delay(500);

  if(distance < 8){
    digitalWrite(ledPin, HIGH);
    for(int x = distance; x < 8;){
      tone(buzzerPin, notes[0], 500);
      delay(distance*100);
      tone(buzzerPin, notes[1], 500);
      check++;
      if(check > 20){
        exit();
      }
      else{
        break;   
      }
    } 
  }
  else{
    digitalWrite(ledPin, LOW);
    digitalWrite(buzzerPin, LOW);
  }
} 
