#include <Arduino.h>
#include <SPI.h>
#include "RF24.h"

#include "ntrp.h"
#include "ntrp_router.h"

RF24 rfmodule(8,9);
NTRP_Router router(&SerialUSB,&rfmodule);

NTRP_Packet_t testpacket;
NTRP_Pipe_t pipe = {'1',0,0,'00001'};

void setup() {

  //Serial.begin(115200);
  SerialUSB.begin(2000000);

  if(!rfmodule.begin())while(1);
  if(!router.sync()) while(1);

  delay(100);
  router.debug("NTRP Router Start v.5");
  //router.openPipe(pipe);
}

uint32_t loop_timer = 0;

char test[32];

void loop() {
  router.task();
}
