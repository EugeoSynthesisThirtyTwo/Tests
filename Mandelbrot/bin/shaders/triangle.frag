#version 330 core

layout(location = 0) out vec4 color;

uniform vec4 screenRect;
uniform vec4 mandelRect;
uniform unsigned int maxIterations;

// interpolate a in [b, c] to [d, e]
float map(float a, float b, float c, float d, float e)
{
	return (a - b) / (c - b) * (e - d) + d;
}

vec2 getCoord()
{
	return vec2(
		map(gl_FragCoord.x, screenRect.x, screenRect.x + screenRect.z, mandelRect.x, mandelRect.x + mandelRect.z),
		map(gl_FragCoord.y, screenRect.y, screenRect.y + screenRect.w, mandelRect.y, mandelRect.y + mandelRect.w)
	);
}

unsigned int mandelbrot(vec2 z0)
{
	unsigned int iterations = 0u;
	vec2 z;
	float temp;

	while (iterations != maxIterations && z.x * z.x + z.y * z.y < 2)
	{
		temp = z.x * z.x - z.y * z.y + z0.x;
		z.y = 2 * z.x * z.y + z0.y;
		z.x = temp;
		iterations++;
	}

	return iterations;
}

vec4 colorFromIterations(vec2 z0, unsigned int iterations)
{
	if (iterations == maxIterations)
		return vec4(0.0, 0.0, 0.0, 0.0);

	float t = float(iterations) / 500.0;// - (z0.x * z0.x + z0.y * z0.y) / 500.0;
		
	return vec4(
		(1.0 - cos(200 * t)) / 2.0,
		(1.0 - cos(200 * t + 1.0)) / 2.0,
		(1.0 + sin(200 * t)) / 2.0,
		1.0
	);
}

void main()
{
	vec2 z0 = getCoord();
	unsigned int iterations = mandelbrot(z0);
	color = colorFromIterations(z0, iterations);
}
