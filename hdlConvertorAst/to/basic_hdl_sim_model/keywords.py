import keyword
import sys

SIMMODEL_KEYWORDS = keyword.kwlist + [
    # BasicRtlSimModel properties
    'sim',
    '_hwIOs',
    '_processes',
    '_subHwModules',
    '_outputs',
    '_init_body',
    '__debug__',
    '__init__',
    '__new__',
    '__getattr__',
    '__getattribute__',
    '__setattr__',
    '__setattribute__',
    # imports
    'pyMathBitPrecise',
    'hwtSimApi',
    'Array3t',
    'Array3val',
    'Bits3t',
    'Bits3val',
    'define_Enum3t',
    'BasicRtlSimModel',
    'BasicRtlSimProxy',
    'bitsBitOp__ashr',
    'bitsBitOp__lshr',
    'bitsBitOp__ror',
    'bitsBitOp__rol',
    'sensitivity',
    'connectSimPort',
    'sim_eval_cond',
    'slice',
]

if sys.version_info[0] <= 2:
    SIMMODEL_KEYWORDS.append("None")
