from enum import Enum
from typing import List, Optional, Union, Tuple

from hdlConvertorAst.hdlAst._bases import iHdlStatement, iHdlObj
from hdlConvertorAst.hdlAst._expr import iHdlExpr


class HdlImport(iHdlStatement):
    """
    The import statements used in VHDL

    :note: note that this does not corresponds to include as include
            is processed by preprocessor
    :ivar ~.path: the list of names which are in the import
    """
    __slots__ = ["path", ]

    def __init__(self, path):
        """
        :type path: List[Union[HdlValueId, HdlAll]]
        """
        super(HdlImport, self).__init__()
        self.path = path


class HdlStmNop(iHdlStatement):
    """
    Nop statement in HDL
    """
    __slots__ = []


class HdlStmBlockJoinType(Enum):
    """
    Python equivalent of C++ hdlConvertor::hdlAst::HdlStmBlockJoinType
    """
    (
        SEQ,  # sequential block
        PAR_JOIN,  # parallel block where we are wainting on all threads
        PAR_JOIN_ANY,  # parallel block where we are wainting on first finished thread
        PAR_JOIN_NONE,  # parallel block where we are are not waiting on any thread
    ) = range(4)


class HdlStmBlock(iHdlStatement):
    """
    Block of statements in HDL
    """
    __slots__ = ["join_t", "body", ]

    def __init__(self):
        super(HdlStmBlock, self).__init__()
        self.join_t = HdlStmBlockJoinType.SEQ  # type: HdlStmBlockJoinType
        self.body = []  # type: List[iHdlObj]


class HdlStmAssign(iHdlStatement):
    """
    HDL assignment statement

    :ivar ~.src: the source
    :ivar ~.dst: the destination
    :ivar ~.is_blocking: flag if true assignment should be evaluated immediately
        else the assignment is evaluated after end of the current event

    :ivar ~.time_delay: delay which waits for a specified time
    :ivar ~.event_delay: delay which waits for a specified event
    :note: Evaluation of assignments with delay specified
           is generaly not synthetisable.
           If statement is blocking the current statement waits
           until the condition is met and then continues.
           If the assignment is not blocking the code continues
           and this statement is executed asynchronously
           after condition is met.
    """
    __slots__ = ["src", "dst", "is_blocking", "time_delay", "event_delay"]

    def __init__(self, src, dst, time_delay=None, event_delay=None):
        super(HdlStmAssign, self).__init__()
        self.src = src  # type: iHdlExpr
        self.dst = dst  # type: iHdlExpr
        self.is_blocking = False  # type: bool
        self.time_delay = time_delay  # type Optional[iHdlExpr]
        self.event_delay = event_delay  # type Optional[List[iHdlExpr]]


class HdlStmIf(iHdlStatement):
    """
    HDL if statement

    :ivar ~.cond: condition in if statement
    :ivar ~.if_true: block of statements which is in if true branch
    :ivar ~.elifs: type: List[Tuple[iHdlExpr, iHdlStatement]]
                  = list of (condition, statement list)
    """
    __slots__ = ["cond", "if_true", "elifs", "if_false"]

    def __init__(self):
        super(HdlStmIf, self).__init__()
        self.cond = None  # type: iHdlExpr
        self.if_true = None  # type: iHdlStatement
        self.elifs = []  # type: List[Tuple[iHdlExpr, iHdlStatement]]
        self.if_false = None  # type: Optional[iHdlStatement]

class HdlStmProcessTriggerConstrain(Enum):
    """
    This enum is used to mark SystemVerilog always construct type variants.

    :note: just always is marked with None, this enum specifies only special always construct variants
        namely always_comb, always_ff, always_latch
    """
    (COMB, FF, LATCH) = range(3)


class HdlStmProcess(iHdlStatement):
    """
    HDL process statement
    the container of statements with the sensitivity specified

    :ivar ~.sensitivity: optional list of expressions which specifies
        the trigger signals of the evaluation of the process
    :note: sensitivity = None means that the process is executed immediately
        sensitivity = [] means the process is never executed
    :note: Verilog always #time construct is translated to process
           without sensitivity and wait #time as a first statement in body.
    """
    __slots__ = ["sensitivity", "body", "trigger_constrain"]

    def __init__(self):
        super(HdlStmProcess, self).__init__()
        self.sensitivity = None  # type: Optional[List[iHdlExpr]]
        self.trigger_constrain = None # type: Optional[HdlStmProcessTriggerConstrain]
        self.body = None  # type: iHdlStatement


class HdlStmCaseType(Enum):
    (CASE, CASEX, CASEZ) = range(3)

class HdlStmCaseUniqConstrain(Enum):
    """
    Used to desinguis between system verilog case variants
    """
    (UNIQUE, UNIQUE0, PRIORITY) = range(3)

class HdlStmCase(iHdlStatement):
    """
    HDL case statement
    """
    __slots__ = ["type", "switch_on", "cases", "default", "uniq_constrain"]

    def __init__(self):
        super(HdlStmCase, self).__init__()
        self.type = HdlStmCaseType.CASE
        self.switch_on = None  # type: iHdlExpr
        self.uniq_constrain = None # type: Optional[HdlStmCaseUniqConstrain]
        self.cases = []  # type: List[Tuple[iHdlExpr, iHdlStatement]]
        self.default = None  # type: Optional[iHdlStatement]


class HdlStmFor(iHdlStatement):
    """
    HDL for statement

    for (init, cond, step)
        body
    """
    __slots__ = ["init", "cond", "step", "body"]

    def __init__(self):
        super(HdlStmFor, self).__init__()
        self.init = None  # type: iHdlStatement
        self.cond = None  # type: iHdlExpr
        self.step = None  # type: iHdlStatement
        self.body = None  # type: iHdlStatement


class HdlStmForIn(iHdlStatement):
    """
    HDL for in statement

    for var in collection:
        body

    :note: corresponds to VHDL "for" and is used also for Verilog "repeat"
    """
    __slots__ = ["var_defs", "collection", "body"]

    def __init__(self):
        super(HdlStmForIn, self).__init__()
        self.var_defs = []  # type: List[iHdlObj]
        self.collection = None  # type: iHdlExpr
        self.body = None  # type: iHdlStatement


class HdlStmWhile(iHdlStatement):
    """
    HDL while statement

    while cond:
        body
    """
    __slots__ = ["cond", "body"]

    def __init__(self):
        super(HdlStmWhile, self).__init__()
        self.cond = None  # type: iHdlExpr
        self.body = None  # type: iHdlStatement


class HdlStmRepeat(iHdlStatement):
    """
    HDL repeat statement

    for _ in range(n):
        body
    """
    __slots__ = ["n", "body"]

    def __init__(self):
        super(HdlStmRepeat, self).__init__()
        self.n = None  # type: iHdlExpr
        self.body = None  # type: iHdlStatement


class HdlStmReturn(iHdlStatement):
    """
    HDL return statement
    """
    __slots__ = ["val"]

    def __init__(self):
        super(HdlStmReturn, self).__init__()
        self.val = None  # type: iHdlExpr


class HdlStmWait(iHdlStatement):
    """
    HDL wait statement

    This is generally not synthetisable to hardware and is used in simulations.
    """
    __slots__ = ["val"]

    def __init__(self):
        super(HdlStmWait, self).__init__()
        self.val = []  # type: List[iHdlExpr]


class HdlStmBreak(iHdlStatement):
    """
    HDL break statement
    """
    __slots__ = []


class HdlStmContinue(iHdlStatement):
    """
    HDL continue statement
    """
    __slots__ = []


class HdlStmThrow(iHdlStatement):
    """
    HDL throw (raise) statement
    """
    __slots__ = ["val"]

    def __init__(self):
        super(HdlStmThrow, self).__init__()
        self.val = None  # type: iHdlExpr


ALL_STATEMENT_CLASSES = (
    HdlStmNop,
    HdlStmBlock,
    HdlStmAssign,
    HdlStmIf,
    HdlStmProcess,
    HdlStmCase,
    HdlStmFor,
    HdlStmForIn,
    HdlStmWhile,
    HdlStmRepeat,
    HdlStmReturn,
    HdlStmWait,
    HdlStmBreak,
    HdlStmContinue,
    HdlStmThrow,
)
