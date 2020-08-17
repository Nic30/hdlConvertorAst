# hdlConvertorAst
[![Travis-ci Build Status](https://travis-ci.org/Nic30/hdlConvertorAst.png?branch=master)](https://travis-ci.org/Nic30/hdlConvertorAst)
[![PyPI version](https://badge.fury.io/py/hdlConvertorAst.svg)](http://badge.fury.io/py/hdlConvertorAst)
[![Python version](https://img.shields.io/pypi/pyversions/hdlConvertorAst.svg)](https://img.shields.io/pypi/pyversions/hdlConvertorAst.svg)
[![Coverage Status](https://coveralls.io/repos/github/Nic30/hdlConvertorAst/badge.svg?branch=master)](https://coveralls.io/github/Nic30/hdlConvertorAst?branch=master)
[![Documentation Status](https://readthedocs.org/projects/hdlconvertorast/badge/?version=latest)](https://hdlconvertorast.readthedocs.io/en/latest/?badge=latest)
 
This library contains universal [HDL AST nodes](https://github.com/Nic30/hdlConvertorAst/tree/master/hdlConvertorAst/hdlAst/__init__.py) (Hardware Description Language Abstract Syntax Tree = objects for representation of code constructs) for SystemVerilog, VHDL and others. This AST can be generated from SV/VHDL code by [hdlConvertor](https://github.com/Nic30/hdlConvertor) and it can also be converted to VHDL/SV/JSON/SystemC/... and other formats using [hdlConvertorAst.to module](https://github.com/Nic30/hdlConvertorAst/tree/master/hdlConvertorAst/to).
Note that the conversion of AST of different languages requires an extra care.
E. g. the VHDL AST and SV AST will have a different type names and thus the direct transpilation using [hdlConvertorAst.to module](https://github.com/Nic30/hdlConvertorAst/tree/master/hdlConvertorAst/to) will not yield working code. If source and target language differs the translation is required. For this translations and post processing you can use [hdlConvertorAst.translate module](https://github.com/Nic30/hdlConvertorAst/tree/master/hdlConvertorAst/translate)

Doc shared with [hdlConvertor](https://github.com/Nic30/hdlConvertor).

### Intended as a support library for
  * code generators
  * code parsers
  * document generators
  * compilers/transpilers

### Supported languages
  * [IEEE 1076-2008 (VHDL 2008)](https://ieeexplore.ieee.org/document/4772740) and all previous standard, (currently without `tool_directive` and `PSL`)
  * [IEEE 1800-2017 (SystemVerilog 2017)](https://ieeexplore.ieee.org/document/8299595) and all previous standards.
  * SystemC 2.3.3
  * HdlConvertor JSON
  * pycocotb basic_rtl_sim_model (python interpreted RTL simulator)
  * hwt (hardware construction framework (HCL) with algorithmic synthesis (HLS))


### List of selected unique features of this library
  * single straightforward universal AST for all languages, wide spectrum of import/export languages
  * automatic parenthesis resolution in expressions based on operator priority/associativity
  * clever white-spaces, constant and expression formating 
  * comments preserved as doc of objects

### Installation

```bash
# note this may be older version than you see in repo
sudo pip3 install hdlConvertorAst

# or download repository and run
sudo python3 setup.py install

# if you are using version from git rather uninstall
# old library first if required
# sudo pip3 uninstall hdlConvertorAst
```
