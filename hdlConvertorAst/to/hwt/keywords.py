import keyword
import sys


HWT_KEYWORDS = keyword.kwlist + [
    # imports
    'hwt', 'Unit', "Param", "Signal",
    "power", "Concat", "If", "Switch",
    "HArray", "HArrayVal", "Bits", "INT", "SLICE",
    "HEnum", "SliceVal", "_",
]

if sys.version_info[0] <= 2:
    HWT_KEYWORDS.append("None")
