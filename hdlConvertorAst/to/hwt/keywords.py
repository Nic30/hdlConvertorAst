import keyword


HWT_KEYWORDS = keyword.kwlist + [
    # imports
    'hwt', 'Unit', "Param", "Signal",
    "power", "Concat", "If", "Switch",
    "HArray", "HArrayVal", "Bits", "INT", "SLICE",
    "HEnum", "SliceVal", "_",
]
