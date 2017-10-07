#include <DigitalPin.h>

DigitalPin forward(13);
DigitalPin backward(12);
DigitalPin left(9);
DigitalPin right(8);

void setup(){
}

void loop() {
 backward.off();
 right.off();
 delay(1000);
 forward.on();
 delay(1000); 
 forward.off();
 delay(1000); 
 backward.on();
 right.on();
 delay(1000);
}
