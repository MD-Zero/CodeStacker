#include <iostream>

#include "Foo/Foo.hpp"
#include "Bar/Bar.hpp"

int main()
{
    foo::Foo foo{};

    foo.doNothing();

    return 0;
}
