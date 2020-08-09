import re

import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id

def is_string(x):
    return isinstance(x,astroid.nodes.Const) and x.pytype()=="builtins.str"


@apply_id
class KeyChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'key-checker'
    priority = -1
    msgs = {
        'E10': (
            'The entire Key should be inside a single string! You should use:`%s` instead!',
            "key-separated-strings",
            ""
        ),
    }


    def visit_call(self,node):
        if node.func.as_string()=="Key":
            s = list(filter(is_string,node.args))
            if len(s)<=1:
                return 
            js = ",".join(x.value for x in s)
            text = 'Key("{}")'.format(re.sub(r",{2,}",r",",js))
            self.add_message("key-separated-strings", node=node,args=text)

