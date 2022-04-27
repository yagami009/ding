#include <ezOutput.h> // ezOutput library

ezOutput led7(7);  // create ezOutput object that attach to pin 7;
ezOutput led8(8);  // create ezOutput object that attach to pin 8;
ezOutput led9(9);  // create ezOutput object that attach to pin 9;

void setup() {
//  led7.blink(71, 71); 
//  led8.blink(50, 50); 
//  led9.blink(42, 42); 
//    led7.blink(71, 71); 
//    led8.blink(71, 71); 
//    led9.blink(71, 71); 
//    led7.blink(50, 50); 
//    led8.blink(50, 50); 
//    led9.blink(50, 50); 
    led7.blink(42, 42); 
    led8.blink(42, 42); 
    led9.blink(42, 42);
}

void loop() {
  led7.loop(); 
  led8.loop(); 
  led9.loop();
}
