#include "message_io.h"

#include <iostream>
void read_message(buffer& buf)
{
	buf.length = read_cmd(buf.bytes);
}


bool handle_message(const buffer& buf)
{
	buf.bytes[buf.length] = 0;
	//write_cmd(buf.bytes, buf.length);
	write_cmd((const byte*)"helo", 4);
	return true;
}


// Straight from Erlang documentation basically
int read_exact(byte *buf, int len) {
    int i, got=0;
    do {
        if ((i = read(0, buf+got, len-got)) <= 0)
            return(i);
        got += i;
    } while (got<len);
    return len;
}

int read_cmd(byte* buf) {
    int len;
    if (read_exact(buf, 4) != 4)
        return(-1);
    len = (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3];
	int read_length = read_exact(buf, len);
	if (read_length != len) {
		printf("read only %i of %i", read_length, len);
	}
	return read_length;
}

int write_exact(const byte *buf, int len) {
    int i, wrote = 0;
    do {
        if ((i = write(1, buf+wrote, len-wrote)) <= 0)
            return (i);
        wrote += i;
    } while (wrote<len);
    return len;
}

int write_cmd(const byte *buf, int len) {
    byte size_buf[4];
    size_buf[0] = (len >> 24) & 0xff;
    size_buf[1] = (len >> 16) & 0xff;
    size_buf[2] = (len >> 8) & 0xff;
    size_buf[3] = len & 0xff;
    write_exact(size_buf, 4);
    return write_exact(buf, len);
}

