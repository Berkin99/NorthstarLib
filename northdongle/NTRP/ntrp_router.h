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

#ifndef __NTRP_ROUTER_H__
#define __NTRP_ROUTER_H__

#include <stdint.h>
#include <stdbool.h>
#include <Arduino.h>

#include "ntrp.h"
#include "RF24.h"

#define SERIAL_DEF          Serial_ //HardwareSerial //UARTClass /*Serial Com Object*/
#define RADIO_DEF           RF24                       /*NRF Object*/ 

#define NTRP_DEFAULT_BAUD   115200
#define NTRP_RX_NRF         0xE7E7E7E900LL
#define NRF_MAX_PIPE_SIZE   6

typedef enum{
  R_OPENPIPE    = 21,
  R_CLOSEPIPE   = 22,
  R_EXIT        = 23,
}NTRP_RouterHeader_e;

typedef struct{
  uint8_t id;         /*Pipe ID (Unique) : Represents the 5 byte address*/
  uint8_t channel;    /*Channel (Not Implemented)*/
  uint8_t bandwidth;  /*Bandwidth (Not Implemented)*/
  uint8_t address[5]; /*5 byte address (Unique)*/
}NTRP_Pipe_t;

class NTRP_Router{
    
    private:
    bool _ready; /* Syncronisation ? OK : ERROR */       
    SERIAL_DEF* serial_port;
    RADIO_DEF* nrf;

    NTRP_Pipe_t nrf_pipe[NRF_MAX_PIPE_SIZE];  /* 6 PIPE */
    uint8_t nrf_pipe_index;                   /* Current PIPE Index */
    int8_t nrf_last_transmit_index;           /* Last Transmit Channel Index */

    uint32_t _timer;
    void _timeout_tick(uint16_t tick = 1);
    
    uint8_t _buffer[NTRP_MAX_MSG_SIZE];   /* Master RX buffer */
    uint8_t _txBuffer[NTRP_MAX_MSG_SIZE]; /* Slave Transmit buffer */

    public:
    NTRP_Router(SERIAL_DEF* serial_port_x , RADIO_DEF* radio);

    uint8_t sync(uint16_t timeout_ms = 10000);
    void task(void);
    void debug(const char* msg);

    uint8_t receiveMaster(NTRP_Message_t* msg);
    void transmitMaster(const NTRP_Message_t* msg);
    
    uint8_t receivePipe(NTRP_Message_t* msg);
    uint8_t transmitPipe( uint8_t pipeid, const NTRP_Packet_t* packet, uint8_t size);
    void transmitPipeFast( uint8_t pipeid,const uint8_t* raw_sentence, uint8_t size);

    void route(NTRP_Message_t* msg);
    
    void    routerCOM(NTRP_Packet_t* packet, uint8_t size);
    uint8_t openPipe(NTRP_Pipe_t cmd);
    void    closePipe(char id);
    // void exit(void);
};

#endif