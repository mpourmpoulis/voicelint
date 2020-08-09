import re

import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id

def is_string(x):
    return isinstance(x,astroid.nodes.Const) and x.pytype()=="builtins.str"


@apply_id
class DynStrChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'dyn-checker'
    priority = -1
    msgs = {
        'E10': (
            'The entire %s spec should be inside a single string! You should use:`%s` instead!',
            "dyn-separated-strings",
            ""
        ),
    }


    def visit_call(self,node):
        name = node.func.as_string()
        if name in ["Key","Text","Mouse"]:
            s = list(filter(is_string,node.args))
            if len(s)<=1:
                return 
            js = ("," if name!="Text" else "").join(x.value for x in s)
            text = '{}("{}")'.format(name,re.sub(r",{2,}",r",",js))
            self.add_message("dyn-separated-strings", node=node,args=(name,text))

