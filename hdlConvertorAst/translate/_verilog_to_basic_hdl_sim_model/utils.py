from hdlConvertorAst.hdlAst._expr import HdlOp, HdlOpType, HdlValueId
from hdlConvertorAst.hdlAst import HdlValueInt
from builtins import isinstance


def to_property_call(o, prop_name):
    """
    :note: a * b -> a.prop_name(b)
    :type o: HdlOp
    """
    o.fn = HdlOpType.CALL
    o.ops[0] = hdl_getattr(o.ops[0], prop_name)
    return o


def hdl_name_prefix(prefix_name, o):
    """
    :type o: HdlValueId
    :type prefix_name: iHdlExpr
    :return: HdlOp
    """
    assert isinstance(o, HdlValueId), o
    return HdlOp(HdlOpType.DOT, [prefix_name, o])


def hdl_getattr(o, prop_name):
    """
    :type o: iHdlExpr
    :type prop_name: str
    :return: HdlOp
    """
    return HdlOp(HdlOpType.DOT, [o, HdlValueId(prop_name)])


def hdl_call(o, args):
    """
    :type o: iHdlExpr
    :type args: List[iHdlExpr]
    :return: HdlOp
    """
    return HdlOp(HdlOpType.CALL, [o, ] + args)


def hdl_index(o, i):
    """
    :type o: iHdlExpr
    :type args: List[iHdlExpr]
    :return: HdlOp
    """
    return HdlOp(HdlOpType.INDEX, [o, i])


def hdl_or(*args):
    first = True
    res = None
    for o in args:
        if first:
            res = o
            first = False
        else:
            res = HdlOp(HdlOpType.OR, [res, o])
    assert res is not None
    return res


def hdl_downto(msb, lsb):
    return HdlOp(HdlOpType.DOWNTO, [msb, lsb])


def hdl_map_asoc(o1, o2):
    """
    :type o1: iHdlExpr
    :type o2: iHdlExpr
    :return: HdlOp
    """
    return HdlOp(HdlOpType.MAP_ASSOCIATION, [o1, o2])


def hdl_add_int(a, b):
    """
    :type a: iHdlExpr
    :type b: int
    :return: iHdlExpr
    """
    if b == 0:
        return a
    elif isinstance(a, HdlValueInt):
        return HdlValueInt(int(a.val) + b, a.val, a.base)
    elif isinstance(a, HdlOp) and a.fn == HdlOpType.ADD:
        o0, o1 = a.ops
        if isinstance(o1, HdlValueInt):
            return hdl_add_int(o0, int(o1) + b)
    elif isinstance(a, HdlOp) and a.fn == HdlOpType.SUB:
        o0, o1 = a.ops
        if isinstance(o1, HdlValueInt):
            return hdl_sub_int(o0, int(o1) - b)

    return HdlOp(HdlOpType.ADD, [a, HdlValueInt(b, None, None)])


def hdl_sub_int(a, b):
    """
    :type a: iHdlExpr
    :type b: int
    :return: iHdlExpr
    """
    if b == 0:
        return a
    elif isinstance(a, HdlValueInt):
        return HdlValueInt(int(a.val) - b, a.val, a.base)
    elif isinstance(a, HdlOp) and a.fn == HdlOpType.ADD:
        o0, o1 = a.ops
        if isinstance(o1, HdlValueInt):
            return hdl_add_int(o0, int(o1) - b)
    elif isinstance(a, HdlOp) and a.fn == HdlOpType.SUB:
        o0, o1 = a.ops
        if isinstance(o1, HdlValueInt):
            return hdl_sub_int(o0, int(o1) + b)

    return HdlOp(HdlOpType.SUB, [a, HdlValueInt(b, None, None)])

