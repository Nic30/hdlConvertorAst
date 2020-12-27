import keyword
import sys

SIMMODEL_KEYWORDS = keyword.kwlist + [
    # BasicRtlSimModel properties
    'sim',
    '_interfaces',
    '_processes',
    '_units',
    '_outputs',
    '_init_body',
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
    'sensitivity',
    'connectSimPort',
    'sim_eval_cond',
    'slice',
]

if sys.version_info[0] <= 2:
    SIMMODEL_KEYWORDS.append("None")
