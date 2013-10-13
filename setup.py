#!/usr/bin/env python

try:
    from distutils.core import setup
except ImportError:
    try:
        from setuptools import setup
    except ImportError:
        print "Use the binary installers..."

setup(  name='pyQrJotari',
        version='1.1',
        author='Loy van Beek',
        author_email='loy.vanbeek@gmail.com',
        scripts=['gui.py', 'csv_interface.py'],
        url='https://github.com/yol/pyQrJotari',
        description='Read QR-codes and display the Jotari activity',
        long_description="Kids can use this to scan their personal QR-code and the program will show what activity is next for them",
        install_requires=["PIL", "bottle", "dateutil"]
)
