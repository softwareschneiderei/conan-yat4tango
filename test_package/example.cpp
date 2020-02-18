#include <yat4tango/ExceptionHelper.h>

int main() {
    yat::Exception inner;
    yat4tango::YATDevFailed outer(inner);
}
