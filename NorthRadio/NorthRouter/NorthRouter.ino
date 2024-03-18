
#include "RF24.h"
#include "ntrp.h"
#include "ntrp_router.h"

RF24 radio(8,9);

NTRP_Router router(&Serial,&radio);
NTRP_Message_t ntrp_message;

void setup() {
  Serial.begin(115200);
  if(!router.sync())  Serial.print("NTRP Router syncronisation error. Error Code : 0x0A");
  if(!radio.begin()) {Serial.print("NRF Error. Radio module not begin. Error Code : 0x0B"); while(1);}
}

void loop() {
  if(router.receiveMaster(&ntrp_message)){
    router.route(&ntrp_message);
  }
}
