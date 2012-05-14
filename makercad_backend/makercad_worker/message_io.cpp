#include "message_io.h"
#include <iostream>

void read_message(buffer& buf)
{
	buf.length = read_cmd(buf.bytes);

}

bool handle_message(buffer& buf)
{
	if (buf.length <= 0) { // EOF or error
		/*
		if (std::cin.eof())
			std::cout << "EOF on stdin, quitting.";
		else
			std::cout << "Error on stdin, quitting.";
		*/
		return false;
	}

	if (buf.length != 2) {
		return false;
	}

	byte res = 0;
	if (buf.bytes[0] == 0){
		res = buf.bytes[1]-1;
	}
	else if (buf.bytes[0] == 1){
		res = buf.bytes[1]+1;
	}
	else {
		return false;
	}

	buf.length = 1;
	buf.bytes[0] = res;
	write_cmd(buf.bytes, buf.length);
	return true;
}


// Straight from Erlang documentation basically
int read_exact(byte *buf, int len) {
    int i, got=0;
    do {
		std::cin.read((char*)buf+got, len-got);
		if (std::cin.eof()) {
			return -1;
		}
		i = (int)std::cin.gcount();
        if (i <= 0)
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
	return read_length;
}

int write_exact(const byte *buf, int len) {

	std::cout.write((char*)buf, len);
    return len;
}

int write_cmd(const byte *buf, int len) {

	byte size_buf[4];
    size_buf[0] = (len >> 24) & 0xff;
    size_buf[1] = (len >> 16) & 0xff;
    size_buf[2] = (len >> 8) & 0xff;
    size_buf[3] = len & 0xff;
    write_exact(size_buf, 4);
	int ret = write_exact(buf, len);
	std::cout.flush();

	return ret;
}

