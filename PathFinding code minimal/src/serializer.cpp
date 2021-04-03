#include "serializer.h"

namespace serializer
{
	static bool endianChecked = false;
	static bool littleEndian = false;
}

bool serializer::isLittleEndian()
{
	if (endianChecked)
		return littleEndian;

	short int number = 0x1;
	char* numPtr = (char*)&number;
	littleEndian = (numPtr[0] == 0);
	endianChecked = true;

	return littleEndian;
}

char serializer::swap(char byte)
{
	byte = (byte & 0xF0) >> 4 | (byte & 0x0F) << 4;
	byte = (byte & 0xCC) >> 2 | (byte & 0x33) << 2;
	byte = (byte & 0xAA) >> 1 | (byte & 0x55) << 1;
	return byte;
}

void serializer::serializeString(BetterVector<char>& buffer, const std::string& value)
{
	serialize<size_t>(buffer, value.size());

	for (char c : value)
		serialize<char>(buffer, c);
}

std::string serializer::unserializeString(const char* buffer, int& cursor)
{
	size_t size = unserialize<size_t>(buffer, cursor);

	std::string result;
	result.resize(size);

	for (size_t i = 0; i < size; i++)
		result[i] = unserialize<char>(buffer, cursor);

	return result;
}