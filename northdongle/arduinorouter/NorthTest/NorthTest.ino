/**
 * __  __ ____ _  __ ____ ___ __  __
 * \ \/ // __// |/ //  _// _ |\ \/ /
 *  \  // _/ /    /_/ / / __ | \  /
 *  /_//___//_/|_//___//_/ |_| /_/
 *
 * Yeniay Control Computer Firmware
 *
 * Copyright (C) 2022 Yeniay
 *
 * This program is free software: you
 * can redistribute it and/or modify it
 * under the terms of the GNU General
 * Public License as published by the
 * Free Software Foundation, in version 3.
 *
 * You should have received a copy of
 * the GNU General Public License along
 * with this program. If not, see
 * <http://www.gnu.org/licenses/>.
 */

#include <Arduino.h>
#include <SPI.h>
#include "RF24.h"
#include "ntrp.h"
#include "ntrp_router.h"


#ifdef ARDUINO_AVR_UNO
#define LEDPIN 13
RF24 rfmodule(8,9);
NTRP_Router router(&Serial,&rfmodule);
#define SERIAL_BEGIN Serial.begin
#endif

#ifdef _SAM_INCLUDED_
#define LEDPIN 14
RF24 rfmodule(A8,A9);
NTRP_Router router(&SerialUSB,&rfmodule);
#define SERIAL_BEGIN SerialUSB.begin
#endif


uint32_t counter = 0;
bool ledvalue = HIGH;
NTRP_Pipe_t cmd = {
  '1',0,0,
  {0xE7,0xE7,0xE7,0xE3,0x00},
  {0xE7,0xE7,0xE7,0xE3,0x01},
};

NTRP_Message_t cmdmsg = {
  '0','1', 6 ,
  {0}
};


void setup() {
  pinMode(LEDPIN, OUTPUT);

  SERIAL_BEGIN(ROUTER_BAUD);

  cmdmsg.packet.header = 3;
  cmdmsg.packet.dataID = 0;
  cmdmsg.packet.data.bytes[0] = 31;
  cmdmsg.packet.data.bytes[1] = 32;
  cmdmsg.packet.data.bytes[2] = 33;
  cmdmsg.packet.data.bytes[3] = 34;
  /* Halt if NRF Module does not begin*/
  if(!rfmodule.begin()) while(1);
  rfmodule.setDataRate(RF24_2MBPS);
  //while(!router.sync(100)); 

  delay(100);
  router.debug("NTRP Router Start v.8");
  router.openPipe(cmd);
  //NTRP_Packet_t pack = {24,0,{0}};
  //router.routerCOM(&pack,3);
}

NTRP_Message_t msg;
void loop() {
  NTRP_InitMessage(&msg);
  if(router.receiveMaster(&msg)){
    router.route(&msg);
    digitalWrite(LEDPIN, ledvalue);
    ledvalue = !ledvalue; 
  }
  //cmdmsg.packet.data.bytes[3] +=1;
  //router.route(&cmdmsg);
}
