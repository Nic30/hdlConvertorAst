from hdlConvertorAst.to.json import ToJson
from hdlConvertorAst.hdlAst._bases import iHdlObj
from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlDirection


class ToJsonDebug(ToJson):
    """
    HdlConverto AST -> json (dict/list/str/int/None composed object)
    An invalid object are converted to str using its __repr__()
    """
    def visit_HdlIdDef(self, o):
        try:
            return ToJson.visit_HdlIdDef(self, o)
        except Exception:
            if isinstance(o, HdlIdDef):
                raise
            return repr(o)

    def visit_HdlDirection(self, o):
        if not isinstance(o, HdlDirection):
            return repr(o)
        else:
            return super(ToJsonDebug, self).visit_HdlDirection(o)

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        :return: iHdlExpr
        """
        try:
            return super(ToJsonDebug, self).visit_iHdlExpr(o)
        except Exception:
            if o.__class__.__repr__ is iHdlObj.__repr__:
                # in order to prevent infinite loop if there is something
                # wrong in serializer code itself
                raise
            return repr(o)
