#ifndef __NTRP_ROUTER_H__
#define __NTRP_ROUTER_H__

#include <stdint.h>
#include <stdbool.h>
#include <Arduino.h>

#include "ntrp.h"
#include "RF24.h"

#define SERIAL_DEF          UARTClass //HardwareSerial
#define RADIO_DEF           RF24

#define NTRP_DEFAULT_BAUD   115200
#define NTRP_RX_NRF         0xE7E7E7E700LL
#define NRF_MAX_PIPE_SIZE   6

typedef enum{
  R_OPENPIPE    = 21,
  R_CLOSEPIPE   = 22,
  R_EXIT        = 23,
}NTRP_RouterHeader_e;

typedef struct{
  uint8_t id;
  uint8_t channel;
  uint8_t speedbyte;
  uint8_t bandwidth;
  uint8_t address[5];
}NTRP_Pipe_t;

class NTRP_Router{
    private:
    bool _ready;
    SERIAL_DEF* serial_port;
    RADIO_DEF* nrf;

    NTRP_Pipe_t nrf_pipe[NRF_MAX_PIPE_SIZE];
    uint8_t nrf_pipe_index;

    uint32_t _timer;
    void _timeout_tick(uint16_t tick = 1);
    
    uint8_t _buffer[NTRP_MAX_MSG_SIZE];
    
    public:
    NTRP_Router(SERIAL_DEF* serial_port_x , RADIO_DEF* radio);
    
    uint8_t sync(uint16_t timeout_ms = 60000);
    uint8_t receiveMaster(NTRP_Message_t* msg);

    void route(NTRP_Message_t* msg);
    void routerCOM(NTRP_Packet_t* packet, uint8_t size);
    
    void transmitPipe(uint8_t pipeno, uint8_t* cmd, uint8_t size);
    void transmitMaster(const NTRP_Message_t* msg);

    void openPipe(NTRP_Pipe_t cmd);
    void closePipe(char id);
    // void exit(void);
};

#endif