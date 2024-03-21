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
#include "ntrp.h"

/** raw_sentence to -> NTRP_Message_t
*   OUT ? parsed : parse error
*/
uint8_t NTRP_Parse(NTRP_Message_t* ref, const uint8_t* raw_sentence){
	if(raw_sentence[0]!=NTRP_STARTBYTE) return 0; /*NTRP Start byte needed*/
	ref->talkerID    = raw_sentence[1];
	ref->receiverID  = raw_sentence[2];
	ref->packetsize  = raw_sentence[3];
	
	ref->packet.header = raw_sentence[4];
	ref->packet.dataID = raw_sentence[5];
	for(uint8_t i = 0; i+2<ref->packetsize;i++){
		ref->packet.data.bytes[i] = raw_sentence[i+6];
		if(i == NTRP_MAX_PACKET_SIZE-2) break;
	}

	if(raw_sentence[ref->packetsize+4] != NTRP_ENDBYTE) return 0;
	return 1;
}

/** raw_sentence to -> NTRP_Packet_t
*   OUT ? parsed : parse error
*/
uint8_t NTRP_PackParse(NTRP_Packet_t* ref, const uint8_t* raw_packet){
	ref->header = raw_packet[0];
	ref->dataID = raw_packet[1];

	/** Zero fall detection
	 * If NRF module stays in the zero print status (prints just 000...00 )
	 * NTRP_PackUnite stops uniting the data. 
	*/
	if(ref->header == 0 && ref->dataID == 0){ 
		return 0;
		/* Debug "zero fall" */
	}

	for(uint8_t i = 0; i<sizeof(NTRP_Data_t) ;i++){
		ref->data.bytes[i] = raw_packet[i+2];
	}
	return 1;
}

/** NTRP_Message to -> raw_sentence
 *  OUT ? united : unite error
*/
uint8_t NTRP_Unite(uint8_t* ref, const NTRP_Message_t* message){
	ref[0] = NTRP_STARTBYTE;
	ref[1] = message->talkerID;
	ref[2] = message->receiverID;
	ref[3] = message->packetsize;
	if(NTRP_PackUnite(&ref[4],message->packetsize,&message->packet) == 0) return 0; /*Pack Parse error*/
	ref[message->packetsize+4] = NTRP_ENDBYTE;
	return 1;
}

/** NTRP_Packet to -> raw_sentence (ref)
 *  OUT ? united : unite error
*/
uint8_t NTRP_PackUnite(uint8_t* ref, uint8_t size, const NTRP_Packet_t* packet){
	if(size<2) return 0;	                /* Min pack size */
	if(size>NTRP_MAX_PACKET_SIZE) return 0; /* Max pack size */
	ref[0] = packet->header;
	ref[1] = packet->dataID;

	/* Illegal to unite 'NAK' with '0' DATA ID */
	if(packet->header == 0 && packet->dataID == 0){ return 0;}

	for(uint8_t i = 0; i<(size-2) ;i++){
		ref[i+2] = packet->data.bytes[i];
		if(i+2>NTRP_MAX_PACKET_SIZE) break;
	}
	return 1;
}

