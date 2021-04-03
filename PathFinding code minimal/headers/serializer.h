#pragma once

#include <string>

#include "better_vector.h"

/*
  Pour tout type T dont la taille peut etre
  entierement connue avec sizeof(T) :

  serialize<T>(buffer, value) : ajoute value,
  de type T, dans buffer.

  unserialize<T>(buffer, cursor) : renvoie une
  variable de type T lue dans buffer, et decale cursor.
*/

namespace serializer
{
	bool isLittleEndian();

	char swap(char byte);

	template<typename T>
	void serialize(BetterVector<char>& buffer, T value)
	{
		char* pointer = (char*)&value;

		if (isLittleEndian())
		{
			for (size_t i = 0; i < sizeof(T); i++)
				buffer.push_back(pointer[i]);
		}
		else
		{
			for (size_t i = sizeof(T) - 1; i >= 0; i--)
				buffer.push_back(swap(pointer[i]));
		}
	}

	template<typename T>
	T unserialize(const char* buffer, int& cursor)
	{
		T result;
		char* pointer = (char*)&result;

		for (size_t i = 0; i < sizeof(T); i++)
			pointer[i] = buffer[cursor++];

		return result;
	}

	void serializeString(BetterVector<char>& buffer, const std::string& value);

	std::string unserializeString(const char* buffer, int& cursor);
}