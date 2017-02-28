from distutils.core import setup, Extension
setup(name='intervalTree', version='1.0', ext_modules=[Extension('intervalTree', ['interval_tree.c'])])
