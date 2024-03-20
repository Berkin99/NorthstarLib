
#include <SPI.h>
#include "RF24.h"

#include "ntrp.h"
#include "ntrp_router.h"

RF24 rfmodule(8,9);
NTRP_Router router(&Serial,&rfmodule);

NTRP_Packet_t testpacket;
NTRP_Pipe_t pipe ={'1',0,0,"00001"};

void setup() {

  testpacket.header = NTRP_MSG;
  testpacket.dataID = 2;
  testpacket.data.bytes[0]='O';
  testpacket.data.bytes[1]='K';
  testpacket.data.bytes[2]='\n';
  
  Serial.begin(115200);
  
  if(!rfmodule.begin())while(1);
  if(!router.sync()) while(1);

  delay(100);
  router.debug("NTRP Router Start v.5");
  //router.openPipe(pipe);
}

void loop() {
  router.task();
  //router.transmitPipe('1',&testpacket,5);
}
