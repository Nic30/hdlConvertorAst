from hdlConvertorAst.hdlAst import HdlDirection, HdlValueId, HdlValueInt, \
    HdlOp, NON_INSTANCIABLE_NODES
from hdlConvertorAst.py_ver_compatibility import is_str
from hdlConvertorAst.to.hdl_ast_visitor import HdlAstVisitor
from hdlConvertorAst.hdlAst._typeDefs import iHdlTypeDef


class ToJson(HdlAstVisitor):

    def visit_HdlContext(self, context):
        """
        :type context: HdlContext
        """
        res = []
        for o in context.objs:
            d = self.visit_main_obj(o)
            res.append(d)
        return res

    def visit_HdlLibrary(self, o):
        """
        :type o: HdlLibrary
        """
        return self.visit_iHdlObjWithName(o)

    def visit_iHdlObjWithName(self, o):
        """
        :type o: iHdlObj
        """
        d = self.visit_iHdlObj(o)
        d["name"] = self.visit_iHdlExpr(o.name)
        return d

    def visit_CodePosition(self, o):
        """
        :type o: CodePosition
        """
        return (o.start_line, o.start_column, o.stop_line, o.stop_column)

    def visit_iHdlObj(self, o):
        """
        :type o: iHdlObj
        """
        d = {
            "__class__": o.__class__.__name__,
        }
        if o.doc:
            d["doc"] = self.visit_iHdlExpr(o.doc)
        if o.position:
            d["position"] = self.visit_CodePosition(o.position)
        return d

    def visit_HdlImport(self, o):
        """
        :type o: HdlImport
        """
        d = self.visit_iHdlObj(o)
        d["path"] = self.visit_iHdlExpr(o.path)
        return d

    def visit_HdlValueIdspace(self, o):
        """
        :type o: HdlValueIdspace
        """
        d = self.visit_iHdlObjWithName(o)
        d["objs"] = [self.visit_main_obj(o2) for o2 in o.objs]
        d["declaration_only"] = o.declaration_only
        return d

    def visit_HdlDirection(self, o):
        """
        :type o: HdlDirection
        """
        if o is None or o == HdlDirection.UNKNOWN:
            return None
        else:
            return o.name

    def visit_HdlIdDef(self, o):
        """
        :type o: HdlIdDef
        """
        d = self.visit_iHdlObjWithName(o)

        for flag_name in ["is_latched", "is_const", "is_static",
                          "is_virtual", ]:
            if getattr(o, flag_name):
                d[flag_name] = True
        d["type"] = self.visit_iHdlExpr(o.type)
        if o.value is not None:
            d["value"] = self.visit_iHdlExpr(o.value)
        d["direction"] = self.visit_HdlDirection(o.direction)
        return d

    def visit_HdlModuleDec(self, o):
        """
        :type o: HdlModuleDec
        """
        d = self.visit_HdlValueIdspace(o)
        d["params"] = [self.visit_HdlIdDef(p) for p in o.params]
        d["ports"] = [self.visit_HdlIdDef(p) for p in o.ports]
        return d

    def visit_HdlModuleDef(self, o):
        """
        :type o: HdlModuleDec
        """
        d = self.visit_iHdlObjWithName(o)
        if o.dec is not None:
            d["dec"] = self.visit_HdlModuleDec(o.dec)
        if o.module_name is not None:
            d["module_name"] = self.visit_iHdlExpr(o.module_name)
        d["objs"] = [self.visit_main_obj(o2) for o2 in o.objs]
        return d

    def _visit_iHdlStatement(self, o):
        """
        :type o: iHdlStatement
        """
        d = self.visit_iHdlObj(o)
        d["labels"] = [self.visit_iHdlExpr(str(x)) for x in o.labels]
        if o.in_preproc:
            d["in_preproc"] = True
        return d

    def visit_HdlCompInst(self, o):
        """
        :type o: HdlCompInst
        """
        d = self.visit_iHdlObjWithName(o)
        if o.module_name is not None:
            d["module_name"] = self.visit_iHdlExpr(o.module_name)
        d["param_map"] = [self.visit_iHdlExpr(pm) for pm in o.param_map]
        d["port_map"] = [self.visit_iHdlExpr(pm) for pm in o.port_map]
        return d

    def visit_HdlFunctionDef(self, o):
        """
        :type o: HdlFunctionDef
        """
        d = self.visit_iHdlObjWithName(o)
        for f in ["is_declaration_only",
                  "is_operator",
                  "is_static",
                  "is_task",
                  "is_virtual",
                  ]:
            if getattr(o, f):
                d[f] = True
        if o.return_t is not None:
            d["return_t"] = self.visit_iHdlExpr(o.return_t)
        d["params"] = [self.visit_HdlIdDef(v) for v in o.params]
        d["body"] = [self.visit_main_obj(o2) for o2 in o.body]
        return d

    def visit_HdlClassDef(self, o):
        """
        :type o: HdlClassDef
        """
        d = self.visit_iHdlObjWithName(o)
        d["members"] = [HdlAstVisitor.visit_iHdlObj(self, m) for m in o.members]
        d["type"] = o.type.name
        d["base_types"] = [self.visit_iHdlExpr(t) for t in o.base_types]
        d["is_virtual"] = o.is_virtual
        d["is_packed"] = o.is_packed
        return d

    def visit_HdlPhysicalDef(self, o):
        """
        :type o: HdlPhysicalDef
        """
        d = self.visit_iHdlObjWithName(o)
        d["range"] = self.visit_iHdlExpr(o.range)
        d["members"] = [self.visit_iHdlExpr(v) for v in o.members]
        return d
    
    def visit_HdlEnumDef(self, o):
        """
        :type o: HdlEnumDef
        """
        d = self.visit_iHdlObjWithName(o)
        d["values"] = [self.visit_iHdlExpr(v) for v in o.values]
        return d

    def visit_HdlStmProcess(self, o):
        """
        :type o: HdlStmProcess
        """
        d = self._visit_iHdlStatement(o)
        if o.sensitivity is not None:
            d["sensitivity"] = [self.visit_iHdlExpr(x) for x in o.sensitivity]
        d["body"] = self.visit_iHdlStatement(o.body)
        return d

    def visit_HdlStmIf(self, o):
        """
        :type o: HdlStmIf
        """
        d = self._visit_iHdlStatement(o)
        d["cond"] = self.visit_iHdlExpr(o.cond)
        d["if_true"] = self.visit_iHdlStatement(o.if_true)
        d["elifs"] = [
            [self.visit_iHdlExpr(c), self.visit_iHdlStatement(stm)]
            for c, stm in o.elifs
        ]
        if o.if_false is not None:
            d["if_false"] = self.visit_iHdlStatement(o.if_false)
        return d

    def visit_HdlStmBlockJoinType(self, o):
        """
        :type o: HdlStmBlockJoinType
        """
        return o.name

    def visit_HdlStmBlock(self, o):
        """
        :type o: HdlStmBlock
        """
        d = self._visit_iHdlStatement(o)
        d["join_t"] = self.visit_HdlStmBlockJoinType(o.join_t)
        d["body"] = [self.visit_main_obj(o2) for o2 in o.body]
        return d

    def visit_HdlStmCase(self, o):
        """
        :type o: HdlStmCase

        :return: True if requires ;\n after end
        """
        d = self._visit_iHdlStatement(o)
        d["type"] = o.type.name
        d["switch_on"] = self.visit_iHdlExpr(o.switch_on)
        d["cases"] = [
            [self.visit_iHdlExpr(c), self.visit_iHdlStatement(stm)]
            for c, stm in o.cases
        ]
        if o.default is not None:
            d["default"] = self.visit_iHdlStatement(o.default)
        return d

    def visit_HdlStmWait(self, o):
        """
        :type o: HdlStmWait
        """
        d = self._visit_iHdlStatement(o)
        d["val"] = self.visit_iHdlExpr(o.val)
        return d

    def visit_HdlStmFor(self, o):
        """
        :type o: HdlStmFor
        """
        d = self._visit_iHdlStatement(o)
        d["init"] = self.visit_iHdlStatement(o.init)
        d["cond"] = self.visit_iHdlExpr(o.cond)
        d["step"] = self.visit_iHdlStatement(o.step)
        d["body"] = self.visit_iHdlStatement(o.body)
        return d

    def visit_HdlStmForIn(self, o):
        """
        :type o: HdlStmForIn
        """
        d = self._visit_iHdlStatement(o)
        d["var_defs"] = [self.visit_main_obj(o2) for o2 in o.var_defs]
        d["collection"] = self.visit_iHdlExpr(o.collection)
        d["body"] = self.visit_iHdlStatement(o.body)
        return d

    def visit_HdlStmWhile(self, o):
        """
        :type o: HdlStmWhile
        """
        d = self._visit_iHdlStatement(o)
        d["cond"] = self.visit_iHdlExpr(o.cond)
        d["body"] = self.visit_iHdlStatement(o.body)
        return d

    def visit_HdlStmRepeat(self, o):
        """
        :type o: HdlStmRepeat
        """
        d = self._visit_iHdlStatement(o)
        d["n"] = self.visit_iHdlExpr(o.n)
        d["body"] = self.visit_iHdlStatement(o.body)
        return d

    def visit_HdlStmAssign(self, o):
        """
        :type o: HdlStmAssign
        """
        d = self._visit_iHdlStatement(o)
        if o.event_delay is not None:
            d["event_delay"] = self.visit_iHdlExpr(o.event_delay)
        if o.time_delay is not None:
            d["time_delay"] = self.visit_iHdlExpr(o.time_delay)
        d["src"] = self.visit_iHdlExpr(o.src)
        d["dst"] = self.visit_iHdlExpr(o.dst)
        d["is_blocking"] = bool(o.is_blocking)
        return d

    def visit_HdlStmReturn(self, o):
        """
        :type o: HdlStmReturn
        """
        d = self._visit_iHdlStatement(o)
        if o.val is not None:
            d["val"] = self.visit_iHdlExpr(o.val)
        return d

    def visit_HdlStmContinue(self, o):
        """
        :type o: HdlStmContinue
        """
        return self._visit_iHdlStatement(o)

    def visit_HdlStmBreak(self, o):
        """
        :type o: HdlStmBreak
        """
        return self._visit_iHdlStatement(o)

    def visit_iHdlExpr(self, o):
        """
        :type o: iHdlExpr
        :return: iHdlExpr
        """
        if isinstance(o, HdlValueId):
            return o.val
        elif is_str(o) or o is None:
            d = {
                "__class__": "str",
                "val": o
            }
        elif isinstance(o, HdlValueInt):
            d = self.visit_HdlValueInt(o)
        elif isinstance(o, HdlOp):
            d = self.visit_HdlOp(o)
        elif isinstance(o, (list, tuple, dict)):
            if isinstance(o, dict):
                items = []
                for _k, _v in o.items():
                    k = self.visit_iHdlExpr(_k)
                    v = self.visit_iHdlExpr(_v)
                    items.append((k, v))
            else:
                items = [self.visit_iHdlExpr(o2) for o2 in o]

            d = {
                "__class__": o.__class__.__name__,
                "items": items,
            }
        elif isinstance(o, iHdlTypeDef):
            return HdlAstVisitor.visit_iHdlObj(self, o)
        elif isinstance(o, float):
            return o
        elif o in NON_INSTANCIABLE_NODES:
            d = {
                "__class__": o.__name__,
            }
        else:
            raise NotImplementedError(
                "Unexpected object of type " + str(type(o)))
        return d

    def visit_HdlValueInt(self, o):
        """
        :type o: HdlValueInt
        """
        if isinstance(o.val, int) and o.bits is None and o.base is None:
            return o.val

        d = {
            "__class__": o.__class__.__name__,
            "val": o.val,
        }
        if o.bits is not None:
            d["bits"] = o.bits
        if o.base is not None:
            d["base"] = o.base
        return d

    def visit_HdlOp(self, o):
        """
        :type o: HdlOp
        :return: iHdlExpr
        """
        d = {
            "__class__": o.__class__.__name__,
            "ops": [self.visit_iHdlExpr(op) for op in o.ops],
            "fn": o.fn.name
        }
        return d
