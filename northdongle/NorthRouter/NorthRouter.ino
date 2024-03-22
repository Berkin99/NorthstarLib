#include <Arduino.h>
#include <SPI.h>
#include "RF24.h"
#include "ntrp.h"
#include "ntrp_router.h"


/*Arduino Uno
#define LEDPIN 13
RF24 rfmodule(8,9);
NTRP_Router router(&Serial,&rfmodule);
*/

/*Arduino Due*/
#define LEDPIN 14
RF24 rfmodule(A8,A9);
NTRP_Router router(&SerialUSB,&rfmodule);

void setup() {
  pinMode(LEDPIN, OUTPUT);
  SerialUSB.begin(ROUTER_BAUD);

  /* Halt if NRF Module does not begin*/
  if(!rfmodule.begin()) while(1);
  rfmodule.setDataRate(RF24_2MBPS);
  while(!router.sync(10)); 

  delay(100);
  router.debug("NTRP Router Start v.7");
}

uint32_t counter = 0;
bool ledvalue = HIGH;

void loop() {
  router.task();
  counter++;
  if(counter%1000 == 0){
    digitalWrite(LEDPIN, ledvalue);
    ledvalue = !ledvalue;
  }
}
