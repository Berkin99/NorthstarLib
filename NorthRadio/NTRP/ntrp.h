/**
 *  __  __ ____ _  __ ____ ___ __  __
 *  \ \/ // __// |/ //  _// _ |\ \/ /
 *   \  // _/ /    /_/ / / __ | \  /
 *   /_//___//_/|_//___//_/ |_| /_/
 *
 *  Yeniay Flight Controller Firmware
 *
 *  Copyright (C) 2023 Yeniay
 *
 * 	This program is part of the Autonomus
 * 	UAV Flight Control System :
 *
 * 	[ Yeniay Flight Controller Firmware ]
 *
 * 	- Yeniay Autonomus Commander Software
 * 	- Yeniay Swarm Commander Software
 * 	- Yeniay Roller Firmware
 */

#ifndef __NTRP_H__
#define __NTRP_H__

#include <stdint.h>

#define NTRP_SYNC_DATA     "*NC"
#define NTRP_PAIR_DATA     "*OK"
#define NTRP_STARTBYTE     '*'
#define NTRP_ENDBYTE       '\n'
#define NTRP_ROUTER_ID     'E'
#define NTRP_MASTER_ID     '0'

#define NTRP_MAX_MSG_SIZE 		32
#define NTRP_MAX_PACKET_SIZE 	28

typedef enum{
  NTRP_NAK 		= 0,
  NTRP_ACK 		= 1,
  NTRP_MSG 		= 2, /*Debug Message + NOP*/
  NTRP_CMD 		= 3, /*Commander + CMD ID + COMMANDARGV*/
  NTRP_GET 		= 4, /*Param Get + ParamID*/
  NTRP_SET 		= 5, /*Param Set + ParamID + DATA*/
  NTRP_LOG		= 6, /*Log Data  + ParamID + Frequency*/	
  NTRP_RUN		= 7, /*Func Run  + FuncID */
}NTRP_Header_e;

typedef union
{
	int8_t     INT8_d;
	int16_t    INT16_d;
	int32_t    INT32_d;
	uint8_t    UINT8_d;
	uint16_t   UINT16_d;
	uint32_t   UINT32_d;
	float 	   FLOAT_d;

	/* (...) */
    uint8_t bytes[26];
}NTRP_Data_t;

typedef struct{
    uint8_t header;
    uint8_t dataID;
	NTRP_Data_t data;
}NTRP_Packet_t;

typedef struct{
	char talkerID;
	char receiverID;
	uint8_t packetsize;
	NTRP_Packet_t packet;
}NTRP_Message_t;

uint8_t NTRP_Parse(NTRP_Message_t* ref, const uint8_t* raw_sentence);
uint8_t NTRP_PackParse(NTRP_Packet_t* ref, const uint8_t* raw_packet);

uint8_t NTRP_Unite(uint8_t* ref, const NTRP_Message_t* message);
uint8_t NTRP_PackUnite(uint8_t* ref, uint8_t size, const NTRP_Packet_t* packet);

#endif /* __NTRP_H__ */
