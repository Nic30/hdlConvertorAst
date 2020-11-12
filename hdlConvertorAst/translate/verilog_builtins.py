from hdlConvertorAst.to.verilog.keywords import IEEE1800_2017_DOLAR_SYMBOLS
from hdlConvertorAst.translate.common.discover_declarations import BuiltIn


def propopulate_verilog_builtins(name_scope):
    """
    :type name_scope: NameScope
    """
    for kw in IEEE1800_2017_DOLAR_SYMBOLS:
        name_scope.register_name(kw, BuiltIn(kw))

    name_scope.register_name('void', BuiltIn('void'))
