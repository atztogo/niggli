from distutils.core import setup, Extension
from numpy.distutils.misc_util import get_numpy_include_dirs

include_dirs = ['./src']
sources = ['./src/niggli.c']
extra_compile_args = []
extra_link_args = []

define_macros = []
# define_macros = [('NIGGLI_WARNING', None),
#                  ('NIGGLI_DEBUG', None)]

extension = Extension('niggli._niggli',
                      include_dirs=include_dirs + get_numpy_include_dirs(),
                      sources=['_niggli.c'] + sources,
                      extra_compile_args=extra_compile_args,
                      extra_link_args=extra_link_args,
                      define_macros=define_macros)

version_nums = [None, None, None]
with open(include_dirs[0] + "/version.h") as w:
    for line in w:
        for i, chars in enumerate(("MAJOR", "MINOR", "MICRO")):
            if chars in line:
                version_nums[i] = int(line.split()[2])

if None in version_nums:
    print("Failed to get version number in setup.py.")
    raise

setup(name='niggli',
      version="%d.%d.%d" % tuple(version_nums),
      description='This is the niggli module.',
      author='Atsushi Togo',
      author_email='atz.togo@gmail.com',
      url='https://github.com/atztogo/niggli',
      packages=['niggli'],
      requires=['numpy'],
      provides=['niggli'],
      platforms=['all'],
      ext_modules=[extension])
