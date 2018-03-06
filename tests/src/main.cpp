#include <iostream>

#include <GLFW/glfw3.h>

#include "Foo/Foo.hpp"
#include "Bar/Bar.hpp"

int main()
{
    foo::Foo foo {};
    bar::Bar bar {};

    foo.doNothing();
    bar.doNothing();

    GLFWwindow * window { nullptr };

    if (!glfwInit()) return -1;

    window = glfwCreateWindow(640, 480, "Hello World", nullptr, nullptr);

    if (!window)
    {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    while (!glfwWindowShouldClose(window))
    {
        glClear(GL_COLOR_BUFFER_BIT);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    return 0;
}
