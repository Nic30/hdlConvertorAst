from hdlConvertorAst.hdlAst import HdlValueId, HdlOpType, HdlValueInt, HdlOp, iHdlExpr
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword

NONE = HdlValueId("None")


def BitsT(width, is_signed=False, bits_cls_name="Bits3t"):
    """
    Create an AST expression of Bits type constructor
    (reg/std_logic_vector equivalent for BasicHdlSimModel)

    :type width: iHdlExpr
    """
    if isinstance(width, HdlOp):
        if width.fn == HdlOpType.DOWNTO:
            high, low = width.ops
            if isinstance(low, (int, HdlValueInt)) and isinstance(high, (int, HdlValueInt)):
                assert int(low) == 0
                width = int(high) + 1
            else:
                width = HdlOp(HdlOpType.ADD,
                              [HdlOp(HdlOpType.SUB, [high, low]),
                              HdlValueInt(1, None, None)])
        else:
            raise NotImplementedError(width)

    if isinstance(width, int):
        width = HdlValueInt(width, None, None)

    c = HdlOp(HdlOpType.CALL, [
        HdlValueId(bits_cls_name, obj=LanguageKeyword()),
        width,
        NONE if is_signed is None else HdlValueInt(int(is_signed), None, None)
    ])
    return c


def sensitivityByOp(op):
    """
    Get sensitivity type for operator.

    :type op: HdlOpType
    :return: Tuple[sensitive on rising edge, sensitive to falling edge]
    """

    if op == HdlOpType.RISING:
        return (True, False)
    elif op == HdlOpType.FALLING:
        return (False, True)
    else:
        raise TypeError(op)
