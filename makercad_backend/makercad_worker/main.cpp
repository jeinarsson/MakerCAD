

#include "makercad_worker.h"
#include "message_io.h"

#define BUFFER_SIZE 10*1024*1024

int main(int argc, char* argv[])
{
	buffer buf;
	buf.bytes = new byte[BUFFER_SIZE]; 
	do
	{
		read_message(buf);
	} while(handle_message(buf));

	delete buf.bytes;
}