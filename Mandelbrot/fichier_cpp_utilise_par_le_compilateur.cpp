#include <iostream>
#include <fstream>
#include <sstream>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#define WIDTH 1600
#define HEIGHT 900

std::string readShader(std::string filePath)
{
	std::ifstream ifs(filePath);

	if (ifs.fail())
	{
		std::cerr << "Error: can't open " << filePath << std::endl;
		exit(EXIT_FAILURE);
	}

	return std::string(std::istreambuf_iterator<char>(ifs), std::istreambuf_iterator<char>());
}

static unsigned int compileShader(const std::string& source, unsigned int type)
{
	unsigned int id = glCreateShader(type);
	const char* src = source.c_str();

	glShaderSource(id, 1, &src, nullptr);
	glCompileShader(id);

	int result;
	glGetShaderiv(id, GL_COMPILE_STATUS, &result);

	if (result == GL_FALSE)
	{
		int length;
		glGetShaderiv(id, GL_INFO_LOG_LENGTH, &length);

		char* message = new char[length];
		glGetShaderInfoLog(id, length, &length, message);

		std::cout << "Failed to compile " << (type == GL_FRAGMENT_SHADER ? "fragment" : "vertex") << " shader." << std::endl;
		std::cout << message << std::endl;

		glDeleteShader(id);
		delete[] message;

		return 0;
	}

	return id;
}

static unsigned int createShader(const std::string& vertexShader, const std::string& fragmentShader)
{
	unsigned int program = glCreateProgram();
	unsigned int vs = compileShader(vertexShader, GL_VERTEX_SHADER);
	unsigned int fs = compileShader(fragmentShader, GL_FRAGMENT_SHADER);

	glAttachShader(program, vs);
	glAttachShader(program, fs);
	glLinkProgram(program);
	glValidateProgram(program);
	
	glDeleteShader(vs);
	glDeleteShader(fs);

	return program;
}

float map(float a, float b, float c, float d, float e)
{
	return (a - b) / (c - b) * (e - d) + d;
}

int main(int argc, char** argv)
{
	GLFWwindow* window;

	/* Initialize the library */
	if (!glfwInit())
		return -1;

	/* Create a windowed mode window and its OpenGL context */
	window = glfwCreateWindow(WIDTH, HEIGHT, "Hello World", NULL, NULL);

	if (!window)
	{
		glfwTerminate();
		exit(EXIT_FAILURE);
	}

	/* Make the window's context current */
	glfwMakeContextCurrent(window);

	GLenum err = glewInit();

	if (GLEW_OK != err)
	{
	  /* Problem: glewInit failed, something is seriously wrong. */
		std::cerr << "Error: " << glewGetErrorString(err) << std::endl;
		exit(EXIT_FAILURE);
	}

	std::cout << "Status: Using GLFW " << glGetString(GL_VERSION) << std::endl;
	std::cout << "Status: Using GLEW " << glewGetString(GLEW_VERSION) << std::endl;

	constexpr int sizeVertex = 2 * 4;
	float positions[sizeVertex] = {
		-1.0f,  1.0f,
		 1.0f,  1.0f,
		 1.0f, -1.0f,
		-1.0f, -1.0f
	};

	constexpr int sizeIndices = 6;
	unsigned int indices[sizeIndices] = {
		0, 1, 2,
		0, 3, 2
	};

	unsigned int buffer;
	glGenBuffers(1, &buffer);
	glBindBuffer(GL_ARRAY_BUFFER, buffer);
	glBufferData(GL_ARRAY_BUFFER, sizeVertex * sizeof(float), positions, GL_STATIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), 0);

	unsigned int ibo;
	glGenBuffers(1, &ibo);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeIndices * sizeof(unsigned int), indices, GL_STATIC_DRAW);

	std::string vertexShader = readShader("shaders/triangle.vert");
	std::string fragmentShader = readShader("shaders/triangle.frag");

	unsigned int shader = createShader(vertexShader, fragmentShader);
	glUseProgram(shader);

	int frameLocation = glGetUniformLocation(shader, "frame");
	int screenRectLocation = glGetUniformLocation(shader, "screenRect");

	int frame = 0;

	/* Loop until the user closes the window */
	while (!glfwWindowShouldClose(window))
	{
		/* Render here */
		glClear(GL_COLOR_BUFFER_BIT);

		glUniform1ui(frameLocation, frame);
		glUniform4f(screenRectLocation, 0, 0, WIDTH, HEIGHT);

		glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, nullptr);

		/* Swap front and back buffers */
		glfwSwapBuffers(window);

		/* Poll for and process events */
		glfwPollEvents();

		frame++;
	}

	glfwTerminate();
	return 0;
}