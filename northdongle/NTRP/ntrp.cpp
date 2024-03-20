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

#include <stdint.h>
#include "ntrp.h"

uint8_t NTRP_Parse(NTRP_Message_t* ref, const uint8_t* raw_sentence){
	if(raw_sentence[0]!=NTRP_STARTBYTE) return 0;
	ref->talkerID    = raw_sentence[1];
	ref->receiverID  = raw_sentence[2];
	ref->packetsize  = raw_sentence[3];

	if(!(ref->packetsize>2))return 0;

	ref->packet.header = raw_sentence[4];
	ref->packet.dataID = raw_sentence[5];
	for(uint8_t i = 0; i+2<ref->packetsize;i++){
		ref->packet.data.bytes[i] = raw_sentence[i+6];
	}

	if(raw_sentence[ref->packetsize+4] != NTRP_ENDBYTE) return 0;
	return 1;
}

uint8_t NTRP_PackParse(NTRP_Packet_t* ref, const uint8_t* raw_packet){
	ref->header = raw_packet[0];
	ref->dataID = raw_packet[1];
	for(uint8_t i = 0; i<sizeof(NTRP_Data_t) ;i++){
		ref->data.bytes[i] = raw_packet[i+2];
	}
	return 1;
}

uint8_t NTRP_Unite(uint8_t* ref, const NTRP_Message_t* message){
	ref[0] = NTRP_STARTBYTE;
	ref[1] = message->talkerID;
	ref[2] = message->receiverID;
	ref[3] = message->packetsize;
	uint8_t status = NTRP_PackUnite(&ref[4],message->packetsize,&message->packet);
	ref[message->packetsize+4] = NTRP_ENDBYTE;
	return status;
}

uint8_t NTRP_PackUnite(uint8_t* ref, uint8_t size, const NTRP_Packet_t* packet){
	if(size<2) return 0;
	ref[0] = packet->header;
	ref[1] = packet->dataID;
	for(uint8_t i = 0; i<(size-2) ;i++){
		ref[i+2] = packet->data.bytes[i];
		if(i+2>NTRP_MAX_PACKET_SIZE) break;
	}
	return 1;
}

