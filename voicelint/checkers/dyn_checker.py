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
        "E11":(
            '%s does not support %s syntax! You should probably refactor this into something like ' + 
            '`Function(lambda %s: %s(%s).execute())`',
            "no-dyn-strings",
            ""
        )
    }


    def visit_call(self,node):
        name = node.func.as_string()
        if name in ["Key","Text","Mouse"]:
            s = list(filter(is_string,node.args))
            if len(s)<=1:
                return 
            js = ("," if name!="Text" else " ").join(x.value for x in s)
            text = '{}("{}")'.format(name,re.sub(r",{2,}",r",",js))
            self.add_message("dyn-separated-strings", node=node,args=(name,text))

        if name in ["BringApp","StartApp"]:
            if any(x for x in node.args if is_string(x) and re.fullmatch(r"%\((\w+)\)s",x.value)):
                temporary,mistakes = [],[]
                for a in node.args:
                    if is_string(a):
                        m = re.fullmatch(r"%\((\w+)\)s",a.value)
                        if m:
                            mistakes.append(m.group(1))
                            temporary.append(m.group(1) + ".format()")
                        else:
                            temporary.append(a.as_string())
                    else:
                        temporary.append(a.as_string())
                args = (name,"%(" + mistakes[0] + ")s",",".join(mistakes),name,",".join(temporary))
                self.add_message("no-dyn-strings", node=node,args=args)
