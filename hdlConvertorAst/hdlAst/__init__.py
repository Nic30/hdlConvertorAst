"""
This package contains the containers
for Hardware Description Language Abstract Syntax Tree (HDL AST)

(System) Verilog/VHDL can be converted by this format and back using this library
Main container is HdlContext which can store all other objects.

:note: this module is using PEP484 type hints, and the type hints are in comments
    to sustain Python 2.7 compatibility
:attention: this module is just simple format of HDL and does not performs all check,
    e.g. you can use a string as a type of the port,
    but such a module generally can not be synthetised to a hardware

:attention: classes in his module are used from C++
"""

from hdlConvertorAst.hdlAst._bases import (
    iHdlObj, iHdlObjInModule, iHdlObjWithName, iHdlStatement)
from hdlConvertorAst.hdlAst._defs import HdlFunctionDef, HdlIdDef
from hdlConvertorAst.hdlAst._expr import (
    HdlAll, HdlOpType, HdlOp, HdlDirection, HdlValueInt, HdlValueId,
    HdlOthers, HdlTypeAuto, HdlTypeType, HdlTypeSubtype, HdlExprNotImplemented,
    iHdlExpr)
from hdlConvertorAst.hdlAst._statements import (
    HdlImport, HdlStmAssign, HdlStmBlockJoinType, HdlStmBlock, HdlStmBreak,
    HdlStmCaseType, HdlStmCase, HdlStmContinue, HdlStmFor, HdlStmForIn, HdlStmIf,
    HdlStmProcess, HdlStmRepeat, HdlStmReturn, HdlStmWait, HdlStmWhile)
from hdlConvertorAst.hdlAst._structural import (
    HdlCompInst, HdlContext, HdlModuleDec, HdlModuleDef, HdlValueIdspace,
    HdlLibrary)
from hdlConvertorAst.hdlAst._typeDefs import (
    iHdlTypeDef, HdlClassType, HdlClassDef, HdlPhysicalDef, HdlEnumDef, HdlTypeBitsDef)
from hdlConvertorAst.hdlAst.utils import CodePosition

NON_INSTANCIABLE_NODES = {
    HdlAll,
    HdlOthers,
    HdlTypeType,
    HdlTypeSubtype,
    HdlTypeAuto,
}