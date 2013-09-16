#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(  name='pyQrJotari',
        version='1.1',
        author='Loy van Beek',
        author_email='loy.vanbeek@gmail.com',
        scripts=['gui.py'],
        url='https://github.com/yol/pyQrJotari',
        description='Read QR-codes and display the Jotari activity',
        long_description="Kids can use this to scan their personal QR-code and the program will show what activity is next for them",
        install_requires=["PIL"]
)
