import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id

@apply_id
class MimicChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'mimic-checker'
    priority = -1
    msgs = {
        'E01': (
            'Mimic should accept single word strings separated by `,` eg Mimic("hello","world") vs Mimic(["hello","world"])',
            "mimic-separated-strings",
            ""
        ),
        'E02': (
            'Strings in Mimic should consist of a single word,eg Mimic("hello","world") vs Mimic("hello world")',
            "mimic-single-word-strings",
            ""
        ),
        'E03': (
        	"Mimic can only accept `extra` as keyword argument, in case you want to fetch the Mimi content from a spoken extra. Other names are going to raise an exception during runtime",
        	"mimic-invalid-keyword",
        	""
        )

    }


    def visit_call(self,node):
        if node.func.as_string()=="Mimic":
            if not all(isinstance(x,astroid.nodes.Const) and x.pytype()=="builtins.str" for x in node.args):
               self.add_message("mimic-separated-strings", node=node)
            else:
                for s in node.args:
                    if len(s.value.strip().split())!=1:
                    	self.add_message("mimic-single-word-strings", node=s)
            if node.keywords and any(x.arg != "extra" for x in node.keywords):
            	self.add_message("mimic-invalid-keyword", node=node)

