#include <stdint.h>
//#include <string.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
using namespace std;


#include "ntrp_router.h"

#define SERIAL_TIMEOUT_MS    100




NTRP_Router::NTRP_Router(SERIAL_DEF* serial_port_x, RADIO_DEF* radio){
    serial_port = serial_port_x;
    nrf = radio;
    nrf_pipe_index = 0;
    nrf_last_transmit_index = -1;
    _ready = false;
}

uint8_t NTRP_Router::sync(uint16_t timeout_ms){

    char syncdata[] = "---";
    _timer = 0;
    while (serial_port->available()<3){
        serial_port->print(NTRP_SYNC_DATA);
        _timeout_tick(100);
        if(_timer>timeout_ms)return 0;
    }

    syncdata[0] = serial_port->read();
    syncdata[1] = serial_port->read();
    syncdata[2] = serial_port->read();
    if(strcmp(syncdata,NTRP_PAIR_DATA)!=0)return 0;

    _ready = true;
    return 1;

}



void NTRP_Router::debug(const char* msg){
    NTRP_Message_t temp;
    temp.talkerID = NTRP_ROUTER_ID;
    temp.receiverID = NTRP_MASTER_ID;

    uint8_t i = 0;
    temp.packet.header = NTRP_MSG;
    while(i<=(NTRP_MAX_PACKET_SIZE-2) && msg[i]!=0x00){
        temp.packet.data.bytes[i] = msg[i];
        i++;    
    }
    temp.packet.dataID = i;
    temp.packetsize = i+2;
    transmitMaster(&temp);
}


void NTRP_Router::task(void){
    /* Continously checks serial port for catch a success ntrp_message */
    static NTRP_Message_t ntrp_message;
    if(receiveMaster(&ntrp_message)){
        route(&ntrp_message);
    }

    /* Continously checks nrf buffer for catch a success ntrp_message */
    if(receivePipe(&ntrp_message))
        route(&ntrp_message); 
    }
}


/* Transmit the NTRP_Message_t to MASTER COMPUTER */
void NTRP_Router::transmitMaster(const NTRP_Message_t* msg){
    if(!_ready)return;
    uint8_t* raw_sentence = (uint8_t*)malloc((msg->packetsize+5));
    NTRP_Unite(raw_sentence, msg);
    serial_port->write(raw_sentence,msg->packetsize+5);
    free(raw_sentence);
}

/* Receive the NTRP_Message_t from MASTER COMPUTER */
uint8_t NTRP_Router::receiveMaster(NTRP_Message_t* msg){
    if(!_ready)return 0;
    if(!serial_port->available())return 0;
    _buffer[0] = serial_port->read();
    if(_buffer[0]!=NTRP_STARTBYTE)return 0;

    _timer = 0;
    while((serial_port->available()<3) && (_timer<SERIAL_TIMEOUT_MS)){
        _timeout_tick(1);}

    for (uint8_t i = 0; i < 3; i++)
    {
        _buffer[i+1] = serial_port->read();
    }
    uint8_t packetsize = _buffer[3];

    _timer = 0;
    while((serial_port->available()<packetsize+1) && (_timer<SERIAL_TIMEOUT_MS)){
        _timeout_tick(1);}

    for (uint8_t i = 0; i < packetsize+1; i++)
    {
        _buffer[i+4] = serial_port->read();
    }

    return NTRP_Parse(msg,_buffer);
}


/* Transmit the NTRP_Message_t to TARGET NRF PIPE */
uint8_t NTRP_Router::transmitPipe( uint8_t pipeid, const NTRP_Packet_t* packet,uint8_t size){

    uint8_t isFound = 0;
    for (uint8_t i = 0; i < nrf_pipe_index; i++)
    {
        if(nrf_pipe[i].id != pipeid) continue;

        isFound = 1;    
        nrf->stopListening(); // Set to TX Mode for transaction
        if(nrf_last_transmit_index != i){
            nrf->openWritingPipe(nrf_pipe[i].address);
            nrf_last_transmit_index = i;
        }
        uint8_t* raw_sentence = (uint8_t*)malloc(size);
        NTRP_PackUnite(raw_sentence,size,packet);
        nrf->write(raw_sentence,size);
        free(raw_sentence);
        nrf->startListening(); // Set to RX Mode again
    }
    return isFound;
}

void NTRP_Router::transmitPipeFast(uint8_t pipeid,const uint8_t* raw_sentence, uint8_t size){
    for (uint8_t i = 0; i < nrf_pipe_index; i++)
    {
        if(nrf_pipe[i].id != pipeid) continue;
            
        nrf->stopListening(); // Set to TX Mode for transaction

        if(nrf_last_transmit_index != i){
            nrf->openWritingPipe(nrf_pipe[i].address);  // Set Main TX address
            nrf_last_transmit_index = i;
        }

        nrf->write(raw_sentence, size);       
        nrf->startListening(); // Set to RX Mode again
    }
}

uint8_t NTRP_Router::receivePipe(NTRP_Message_t* msg){
    uint8_t pipe;
    if(!nrf->available(&pipe))return 0;
    debug("ReceivedNRF");
    // nrf->read(_buffer,NTRP_MAX_MSG_SIZE);
    // NTRP_PackParse(&msg->packet,_buffer);

    // msg->receiverID = NTRP_MASTER_ID;
    // msg->talkerID = nrf_pipe[pipe].id;
    // msg->packetsize = NTRP_MAX_PACKET_SIZE;
    return 1;
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
            debug("NRF Pipe not found :" + msg->receiverID);
        }
        break;
    }     
}
}

/* Router Handler : Router Commands */
void NTRP_Router::routerCOM(NTRP_Packet_t* cmd, uint8_t size){

    // char head[] = "Header =     ";
    // sprintf(&head[9],"%d",(int)cmd->header);
    // debug(head);

    /*SWITCH TO ROUTER COMMAND*/
switch (cmd->header)
{
    case NTRP_MSG:{
        debug("Router Message ACK");
        break;
    }
    case R_OPENPIPE:
        if(size<8) return; /* Required byte length */ 

        NTRP_Pipe_t pipe;
        pipe.id = cmd->dataID; /* Reference PIPE id : '1','2'... */
        pipe.channel = cmd->data.bytes[0];
        pipe.speedbyte = cmd->data.bytes[1];

        for(uint8_t i = 0; i<5 ; i++){
            pipe.address[i] = cmd->data.bytes[i+2];   
        }

        if(openPipe(pipe)){debug("NRF Pipe Opened");}
        else{debug("NRF Pipe Error");}
    break;
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
    delay(tick);
}
