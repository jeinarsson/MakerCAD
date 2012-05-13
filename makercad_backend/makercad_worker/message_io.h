#ifndef MESSAGE_IO_H
#define MESSAGE_IO_H

#include "makercad_worker.h"

struct buffer {
	int length;
	byte *bytes;
};

void read_message(buffer& buf);
bool handle_message(const buffer& buf);


int read_exact(byte *buf, int len);
int read_cmd(byte* buf);
int write_exact(const byte *buf, int len);
int write_cmd(const byte *buf, int len);

#endif