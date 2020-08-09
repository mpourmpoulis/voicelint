import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id

def is_string(x):
    return isinstance(x,astroid.nodes.Const) and x.pytype()=="builtins.str"

@apply_id
class MimicChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'mimic-checker'
    priority = -1
    msgs = {
        'E01': (
            'Mimic should accept single word strings separated by `,` eg %s',
            "mimic-separated-strings",
            ""
        ),
        'E02': (
            'Strings in Mimic should consist of a single word,instead of `%s` you should use `%s`', 
            "mimic-single-word-strings",
            ""
        ),
        'E03': (
        	"Mimic can only accept `extra` as keyword argument, in case you want to fetch the Mimic content from a spoken extra. Other names are going to raise an exception during runtime",
        	"mimic-invalid-keyword",
        	""
        )

    }


    def visit_call(self,node):
        if node.func.as_string()=="Mimic":
            if not all(is_string(x) for x in node.args):
                args = 'Mimic("hello","world") vs Mimic(["hello","world"])'
                if node.args and isinstance(node.args[0],(astroid.List,astroid.Tuple)):
                    elements = node.args[0].elts
                    temporary = []
                    for e in elements:
                        if is_string(e) and len(e.value.strip().split())!=1:
                            temporary.append(",".join('"%s"'%x for x in e.value.strip().split()))
                        else:
                            temporary.append(e.as_string())
                    args = 'Mimic(%s)' % ','.join(temporary)
                self.add_message("mimic-separated-strings", node=node,args=args)
            else:
                for s in node.args:
                    if len(s.value.strip().split())!=1:
                        text = ",".join('"%s"'%x for x in s.value.strip().split())
                        self.add_message("mimic-single-word-strings", node=s,args=(s.as_string(),text))
            if node.keywords and any(x.arg != "extra" for x in node.keywords):
            	self.add_message("mimic-invalid-keyword", node=node)

