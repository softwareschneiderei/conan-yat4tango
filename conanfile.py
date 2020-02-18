from conans import ConanFile, CMake, tools


class Yat4TangoConan(ConanFile):
    name = "yat4tango"
    version = "1.9.7"
    license = "GPL-2.0-or-later"
    author = "marius.elvert@softwareschneiderei.de"
    url = "https://github.com/softwareschneiderei/conan-yat4tango"
    description = "yat4tango is Tango oriented specialization of the yat C++ framework"
    topics = ("utility", "control-system",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    requires = ["yat/1.11.1@softwareschneiderei/stable", "cpptango/9.3.3@softwareschneiderei/stable"]
    exports_sources = ["cmake_fixes.patch"]
    no_copy_source = True

    def source(self):
        tag = "svn://svn.code.sf.net/p/tango-cs/code/share/yat4tango/tags/YAT4Tango-1.9.7"
        svn = tools.SVN()
        svn.checkout(tag)
        self.output.info("Applying patch")
        tools.patch(patch_file="cmake_fixes.patch")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        CMake(self).install()

    def package_info(self):
        self.cpp_info.libs = ["yat4tango"]
