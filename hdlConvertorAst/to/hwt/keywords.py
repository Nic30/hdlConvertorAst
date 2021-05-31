import keyword
import sys


HWT_KEYWORDS = keyword.kwlist + [
    # imports
    'hwt', 'Unit', "Param", "Signal",
    "Concat", "If", "Switch",
    "HArray", "Bits", "INT", "SLICE", "STR", "BIT", "FLOAT64",
    "HEnum", "_", "rename_signal",
]

if sys.version_info[0] <= 2:
    HWT_KEYWORDS.append("None")
