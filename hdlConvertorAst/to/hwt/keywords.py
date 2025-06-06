import keyword
import sys


HWT_KEYWORDS = keyword.kwlist + [
    '__debug__',
    # imports
    'hwt', 'HwModule', "HwParam", "HwIOSignal",
    "Concat", "If", "Switch",
    "HArray", "HBits", "INT", "SLICE", "STR", "BIT", "FLOAT64",
    "HEnum", "_", "rename_signal",
]

if sys.version_info[0] <= 2:
    HWT_KEYWORDS.append("None")
