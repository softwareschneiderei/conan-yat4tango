import os
import shutil

from conans import ConanFile, CMake, tools


# From https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth/31039095
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)

    root_files = os.listdir(src)
    if ignore:
        excluded = ignore(src, root_files)
        root_files = [x for x in root_files if x not in excluded]

    for item in root_files:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


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

