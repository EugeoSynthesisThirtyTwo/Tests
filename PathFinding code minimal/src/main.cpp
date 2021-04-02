#include <iostream>
#include <vector>
#include <fstream>

#include "grid.h"
#include "AStar.h"

void savePath(std::string filePath, const std::vector<std::pair<int, int>>& path)
{
	std::ofstream ofs = std::ofstream(filePath);

	if (ofs.is_open())
	{
		int imax = path.size() - 1;
		int dx, dy;

		for (int i = 0; i < imax; i++)
		{
			dx = path[i + 1].first - path[i].first;
			dy = path[i + 1].second - path[i].second;

			if (dx == -1)
			{
				if (dy == -1)
					ofs << '7';
				else if (dy == 0)
					ofs << '6';
				else if (dy == 1)
					ofs << '5';
			}
			else if (dx == 0)
			{
				if (dy == -1)
					ofs << '0';
				else if (dy == 1)
					ofs << '4';
			}
			else if (dx == 1)
			{
				if (dy == -1)
					ofs << '1';
				else if (dy == 0)
					ofs << '2';
				else if (dy == 1)
					ofs << '3';
			}
		}

		ofs.close();
	}
	else
	{
		throw "can't open " + filePath;
	}
}

int main(int argc, char** argv)
{
	if (argc != 7)
	{
		std::cerr << "format : ./PathFinding map.bin x_start y_start x_end y_end path.txt";
		exit(EXIT_FAILURE);
	}

	Grid grid = Grid::load(argv[1]);
	AStar astar(grid);
	std::vector<std::pair<int, int>> path = astar.findPath(
		std::stoi(argv[2]), std::stoi(argv[3]),
		std::stoi(argv[4]), std::stoi(argv[5])
	);

	savePath(argv[6], path);

	std::cout << "success" << std::endl;

	return 0;
}