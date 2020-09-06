import json

from hdlConvertorAst import hdlAst
from hdlConvertorAst.hdlAst import HdlContext, CodePosition, HdlOpType,\
    HdlDirection, HdlStmBlockJoinType, HdlValueInt, HdlValueId, HdlStmCase, HdlStmCaseType,\
    NON_INSTANCIABLE_NODES
from hdlConvertorAst.py_ver_compatibility import is_str


KNOWN_NODES = {
    cls_name: getattr(hdlAst, cls_name)
    for cls_name in dir(hdlAst) if cls_name.startswith("Hdl")
}
KNOWN_NODES.update({
    "dict": dict,
    "list": list,
    "tuple": tuple,
    "str": str,
})


def _parse_hdlConvertor_json(j):
    # handle primitive types
    if j is None:
        return j
    elif isinstance(j, float):
        return j
    elif is_str(j):
        return HdlValueId(j)
    elif isinstance(j, int):
        return HdlValueInt(j, None, None)
    elif isinstance(j, list):
        return [_parse_hdlConvertor_json(_j) for _j in j]

    # load a hdlAst object
    cls = j["__class__"]
    cls = KNOWN_NODES[cls]
    consumed = {"__class__", }
    if cls in NON_INSTANCIABLE_NODES:
        assert len(j) == 1
        return cls

    elif cls in (dict, list, tuple):
        _items = j["items"]
        items = [_parse_hdlConvertor_json(i) for i in _items]
        if cls is dict:
            return {k: v for k, v in items}
        elif cls is tuple:
            return tuple(items)
        else:
            return items

    elif cls is str:
        return j["val"]

    elif cls is HdlValueInt:
        return HdlValueInt(j["val"], j.get("bits", None), j.get("base", None))

    argc = cls.__init__.__code__.co_argcount
    if argc == 1:
        o = cls()
    else:
        # load argumets for __init__
        argv = []
        # 1st is self
        arg_names = cls.__init__.__code__.co_varnames[1:argc]
        for a in arg_names:
            v = j.get(a, None)
            if a == "fn":
                v = getattr(HdlOpType, v)
            else:
                v = _parse_hdlConvertor_json(v)
            argv.append(v)
            consumed.add(a)
        o = cls(*argv)

    not_consumed = set(j.keys()).difference(consumed)
    if not_consumed:
        # load rest of the properties which were not in __init__ params
        for k in not_consumed:
            v = j[k]
            # there are few cases where object class is not specified specified
            # explicitly we have to handle them first
            if k == "position":
                _v = CodePosition()
                (
                    _v.start_line,
                    _v.start_column,
                    _v.stop_line,
                    _v.stop_column
                ) = v
            elif k == "direction":
                if v is None:
                    _v = v
                else:
                    _v = getattr(HdlDirection, v)
            elif k == "join_t":
                _v = getattr(HdlStmBlockJoinType, v)
            elif cls is HdlStmCase and k == "type":
                _v = getattr(HdlStmCaseType, v)
            else:
                _v = _parse_hdlConvertor_json(v)
            setattr(o, k, _v)

    return o


def parse_hdlConvertor_json(j):
    """
    Convert loaded JSON (structure composed of list, dict, str, int, float, None)

    :return: HdlContext
    """
    assert isinstance(j, list), j
    ctx = HdlContext()
    for jo in j:
        o = _parse_hdlConvertor_json(jo)
        ctx.objs.append(o)
    return ctx


def parse_hdlConvertor_json_str(j_str):
    j = json.loads(j_str)
    return parse_hdlConvertor_json(j)


def parse_hdlConvertor_json_file(file_name):
    with open(file_name) as f:
        j = json.load(f)
        return parse_hdlConvertor_json(j)


if __name__ == "__main__":
    import os
    f_name = os.path.join(os.path.dirname(__file__), "..",
                          "tests", "data", "dff_async_reset.Verilog.json")
    print(parse_hdlConvertor_json_file(f_name))
