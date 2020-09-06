#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from setuptools import find_packages, setup
import sys


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

deps = ["typing", "future"] if sys.version_info[0] == 2 else None

setup(
    name='hdlConvertorAst',
    version='0.5',
    description='A library of AST nodes for HDL languages (Verilog, VHDL, ...) and transpiler/compiler utilities',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Nic30/hdlConvertorAst',
    author='Michal Orsak',
    author_email='michal.o.socials@gmail.com',
    keywords=['hdl', 'vhdl', 'verilog', 'systemverilog',
              'parser', 'preprocessor', 'antlr4', 'ast', 'code-generator'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
    ],
    license="MIT",
    packages=[p for p in find_packages() if p != "tests"],
    test_suite='tests.all.suite',
    install_requires=deps,
    test_require=deps,
)
