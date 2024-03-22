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

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
using namespace std;

#include "ntrp_router.h"

#define SERIAL_TIMEOUT_US    1000

NTRP_Router::NTRP_Router(SERIAL_DEF* serial_port_x, RADIO_DEF* radio){
    serial_port = serial_port_x;
    nrf = radio;
    nrf_pipe_index = 0;
    nrf_last_transmit_index = -1;
    _ready = false;
    mode = R_MODE_TRX;
}

uint8_t NTRP_Router::sync(uint16_t timeout_ms){

    char syncdata[] = "---";
    _timer = 0;
    while (serial_port->available()<3){
        serial_port->print(NTRP_SYNC_DATA);
        _timeout_tick(100);
        if(_timer>timeout_ms*1000)return 0;
    }

    syncdata[0] = serial_port->read();
    syncdata[1] = serial_port->read();
    syncdata[2] = serial_port->read();
    if(strcmp(syncdata,NTRP_PAIR_DATA)!=0)return 0;

    _ready = true;
    return 1;

}

void NTRP_Router::task(void){
    /* Continously checks serial port for catch a success ntrp_message */
    NTRP_Message_t ntrp_message;
    if(receiveMaster(&ntrp_message)){
        route(&ntrp_message);
    }
    /* Continously checks nrf buffer for catch a success ntrp_message */
    if(receivePipe(&ntrp_message)){
        route(&ntrp_message); 
    }
}

void NTRP_Router::debug(const char* msg){
    NTRP_Message_t temp;
    temp.talkerID = NTRP_ROUTER_ID;
    temp.receiverID = NTRP_MASTER_ID;

    uint8_t i = 0;
    i=0;
    temp.packet.header = NTRP_MSG;
    while(i<=(NTRP_MAX_PACKET_SIZE-2) && msg[i]!=0x00){
        temp.packet.data.bytes[i] = msg[i];
        i++;    
    }
    temp.packet.dataID = i;
    temp.packetsize = i+2;
    transmitMaster(&temp);
}


/* Transmit the NTRP_Message_t to MASTER COMPUTER */
void NTRP_Router::transmitMaster(const NTRP_Message_t* msg){
    if(NTRP_Unite(_txBuffer, msg)){
        serial_port->write(_txBuffer,msg->packetsize+5);
    }
}

/** Receive the NTRP_Message_t from MASTER COMPUTER 
 *  Tries to receive new msg ? OK : Error
*/
uint8_t NTRP_Router::receiveMaster(NTRP_Message_t* msg){
    if(!serial_port->available())return 0;
    _buffer[0] = serial_port->read();

    if(_buffer[0]!=NTRP_STARTBYTE)return 0; /*Not starting with start byte*/

    _timer = 0;
    while((serial_port->available()<3) && (_timer<SERIAL_TIMEOUT_US)){
        _timeout_tick(50);}

    for (uint8_t i = 0; i < 3; i++){_buffer[i+1] = serial_port->read();}

    if(_buffer[1]!=NTRP_MASTER_ID)return 0; /* talker ID should be MASTER ID */
    uint8_t packetsize = _buffer[3];
    if(_buffer[3]>NTRP_MAX_PACKET_SIZE)return 0; /* Max Packet size error */

    _timer = 0;
    while((serial_port->available()<packetsize+1) && (_timer<SERIAL_TIMEOUT_US)){
        _timeout_tick(50);}

    for (uint8_t i = 0; i < packetsize+1; i++)
    {_buffer[i+4] = serial_port->read(); /*_buffer[4] is start of the NTRP_Packet*/
    }

    return NTRP_Parse(msg , _buffer);
}

/* Transmit the NTRP_Message_t to TARGET NRF PIPE */
uint8_t NTRP_Router::transmitPipe( uint8_t pipeid, const NTRP_Packet_t* packet,uint8_t size){
    if(mode==R_MODE_FULLRX) return 0;
    uint8_t isFound = 0;
    if (pipeid==0) return 0; /*Pipe ID needs to be a ascii char*/
    for (uint8_t i = 0; i < nrf_pipe_index; i++)
    {
        if(nrf_pipe[i].id != pipeid) continue;
        
        if(mode==R_MODE_TRX) nrf->stopListening();        /* RF24 -> Standby I */
        
        isFound = 1;
        if(nrf_last_transmit_index!=i){
            nrf->openWritingPipe(nrf_pipe[i].address);   /* RF24 -> TX Settling (!!!CHANGES THE RX0_ADDRESS TOO!!!)*/
            nrf_last_transmit_index = i;
        }    
         
        NTRP_PackUnite(_txBuffer,size,packet);    
        nrf->write(_txBuffer,size); /*Write to TX FIFO*/

        if(mode==R_MODE_TRX) nrf->startListening();  /*Set to RX Mode again*/
    }
    return isFound;
}

void NTRP_Router::transmitPipeFast(uint8_t pipeid,const uint8_t* raw_sentence, uint8_t size){
    if(mode==R_MODE_FULLRX) return;

    for (uint8_t i = 0; i < nrf_pipe_index; i++)
    {
        if(nrf_pipe[i].id != pipeid) continue;
            
        if(mode==R_MODE_TRX) nrf->stopListening(); // Set to TX Mode for transaction

        if(nrf_last_transmit_index != i){
            nrf->openWritingPipe(nrf_pipe[i].address);  // Set Main TX address
            nrf_last_transmit_index = i;
        }

        nrf->write(raw_sentence, size);       
        if(mode==R_MODE_TRX) nrf->startListening(); // Set to RX Mode again
    }
}

uint8_t NTRP_Router::receivePipe(NTRP_Message_t* msg){
    if(mode==R_MODE_FULLTX) return 0;

    uint8_t pipe = 0;
    if(nrf->available(&pipe)){
        nrf->read(_buffer,NTRP_MAX_MSG_SIZE);
        NTRP_PackParse(&msg->packet,_buffer);

        msg->receiverID = NTRP_MASTER_ID;
        msg->talkerID = nrf_pipe[pipe].id;
        msg->packetsize = NTRP_MAX_PACKET_SIZE;
        return 1;
    }
    return 0;
}
    
/* Router Handler : Communications Core Function 
*  Route the NTRP_Message_t to desired address
*  It is not optimised for router.
*  USE CASE : General use case and debugging.
*/
void NTRP_Router::route(NTRP_Message_t* msg){
    
switch (msg->receiverID)
{
    case NTRP_MASTER_ID:transmitMaster(msg);break;                      /* ReceiverID Master */
    case NTRP_ROUTER_ID:routerCOM(&msg->packet,msg->packetsize);break;  /* ReceiverID Router */
    default:{
        if(!transmitPipe(msg->receiverID,&msg->packet,msg->packetsize)){ /* Search NRF pipes for Receiver Hit*/
            debug("transmitPipe Error :" + msg->receiverID);
        }
        break;
    }     
}
}

/* Router Handler : Router Commands */
void NTRP_Router::routerCOM(NTRP_Packet_t* cmd, uint8_t size){

    /* SWITCH TO ROUTER COMMAND */
    switch (cmd->header){
    case NTRP_MSG:{
        debug("Router Message ACK");
        break;
    }
    case R_OPENPIPE:
        if(size<7) return; /* Required byte length */ 

        NTRP_Pipe_t pipe;
        pipe.id =           cmd->dataID; /* Reference PIPE id char : '1','2'... */
        pipe.channel =      cmd->data.bytes[0];
        pipe.bandwidth =    cmd->data.bytes[1];

        for(uint8_t i = 0; i<5 ; i++){
            pipe.address[i] = cmd->data.bytes[i+2];   
        }

        if(openPipe(pipe)){debug("NRF Pipe Opened");}
        else{debug("NRF Pipe Error");}
    break;
    case R_TRX:
        debug("NRF TRX");
        mode = R_MODE_TRX; break;
    case R_FULLRX:
        debug("NRF FULLRX");
        mode = R_MODE_FULLRX; break;
    case R_FULLTX:
        debug("NRF FULLTX");
        nrf->stopListening();
        mode = R_MODE_FULLTX; break;
    case R_CLOSEPIPE:
        /*Not Implemented*/
    break;
    case R_EXIT:
        /*Not Implemented*/
    break;
    default:
    break;
}
}

uint8_t NTRP_Router::openPipe(NTRP_Pipe_t cmd){    
    if(nrf_pipe_index>=NRF_MAX_PIPE_SIZE) return 0;
    //TODO: nrf->setChannel(cmd.channel);
    //TODO: nrf->setSpeed(speeds[cmd.speedbyte])
    nrf->openReadingPipe(nrf_pipe_index, cmd.address); 
    nrf->startListening();

    nrf_pipe[nrf_pipe_index] = cmd;
    nrf_pipe_index++;     
    return 1;
}

void NTRP_Router::closePipe(char id){
    /*Not Implemented*/
}

void NTRP_Router::_timeout_tick(uint16_t tick){
    _timer+=tick;
    delayMicroseconds(tick);
}
