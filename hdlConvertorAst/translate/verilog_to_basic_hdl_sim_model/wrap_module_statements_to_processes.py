from hdlConvertorAst.hdlAst._expr import HdlOp, HdlValueId, HdlOpType
from hdlConvertorAst.hdlAst._statements import HdlStmAssign, HdlStmProcess
from hdlConvertorAst.hdlAst._structural import HdlModuleDef
from hdlConvertorAst.hdlAst import HdlValueInt


def collect_hdl_ids(expr, res):
    """
    :type expr: iHdlExpr
    :type res: Set[HdlValueId]
    """
    if isinstance(expr, HdlOp):
        for o in expr.ops:
            collect_hdl_ids(o, res)
    elif isinstance(expr, HdlValueId):
        res.add(expr)
    elif isinstance(expr, (HdlValueInt, bool, int, str, float)):
        pass
    else:
        raise NotImplementedError(expr)


def collect_indexes(expr):
    """
    Collect indexes from expression with optional index operator

    :type expr: iHdlExpr
    """
    if isinstance(expr, HdlOp) and expr.fn == HdlOpType.INDEX:
        assert len(expr.ops) == 2, expr.ops
        for i in collect_indexes(expr.ops[0]):
            yield i
        yield expr.ops[1]


def wrap_module_statements_to_processes(context):
    """
    Wrap statements which are not in any process instance in HdlStmProcess instance

    :type context: HdlContext
    """
    for o in context.objs:
        if isinstance(o, HdlModuleDef):
            objs = o.objs
            for i, obj in enumerate(objs):
                if isinstance(obj, HdlStmAssign):
                    p = HdlStmProcess()
                    p.body = obj
                    p.sensitivity = set()
                    for _i in collect_indexes(obj.dst):
                        collect_hdl_ids(_i, p.sensitivity)
                    collect_hdl_ids(obj.src, p.sensitivity)
                    objs[i] = p
