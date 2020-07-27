import re
import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id




@apply_id
class RuleDetailsChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = 'rule-details-checker'
    priority = -1
    msgs = {
        'E05': (
            "It appears that in your rule details you are declaring the grammar to be CCR, but your rule "
             + " is merrily `MappingRule`, when it should be `MergeRule`",
            "mapping-rule-is-not-ccr",
            ""
        ),
        'E06': (
            "CCRType.GLOBAL cannot be used with contexts, whether application aka `executable`,`title`" + 
            ",... or Function Contexts (`function_context`). You need to use `CCRType.APP` in both cases!",
            "global-no-context",
            ''
        )

    }

    def visit_module(self, node):
        self.cl = {}

    def visit_classdef(self,node):
        self.cl[node.name] = [x.as_string() for x in node.bases]

    def visit_return(self,node):
        if not isinstance(node.parent,astroid.FunctionDef) or node.parent.name!="get_rule":
            return 
        if not node.is_tuple_return():   return 
        name = node.value.getitem(astroid.Const(0)).as_string()
        if name not in self.cl: return 
        details = node.value.getitem(astroid.Const(1))
        if not isinstance(details,astroid.Call): return 
        try : 
            ccrtype = next(x.value for x in details.keywords if x.arg == "ccrtype") 
            if self.cl[name] == ["MappingRule"]:
                self.add_message("mapping-rule-is-not-ccr",node=node)
            if ccrtype.as_string()=="CCRType.GLOBAL":
                if any(x for x in details.keywords if x.arg in ["executable","title","handle","function_context"]):
                    self.add_message("global-no-context",node=node)

        except StopIteration:
            pass







        


