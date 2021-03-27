#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

setup(name='ProjectScribbleLib',
      version='0.1',
      description='Project Scribble Library',
      long_description="Library just for interacting with the project scribble bot.",

      url='https://github.com/Invalid-Entry/ProjectScribble',
      
      author='James Taylor',
      author_email='jmons@users.noreply.github.com',
      license='MIT',

      classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
      ],

      packages=find_packages(),
      install_requires=['pillow', 'rich', 'simplification']
     )
