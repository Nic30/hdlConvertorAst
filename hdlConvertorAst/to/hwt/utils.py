from hdlConvertorAst.to.basic_hdl_sim_model.utils import verilog_slice_to_width
from hdlConvertorAst.hdlAst import HdlValueInt, HdlOpType, HdlOp, HdlValueId
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword


def BitsT(width, is_signed=False, bits_cls_name="Bits"):
    """
    Create an AST expression of Bits type constructor
    (reg/std_logic_vector equivalent for hwt)

    :type width: iHdlExpr
    """
    width = verilog_slice_to_width(width)

    if isinstance(width, int):
        width = HdlValueInt(width, None, None)

    args = [
        HdlValueId(bits_cls_name, obj=LanguageKeyword()),
        width,
    ]
    if is_signed is not None:
        args.append(HdlValueInt(int(is_signed), None, None))

    return HdlOp(HdlOpType.CALL, args)
