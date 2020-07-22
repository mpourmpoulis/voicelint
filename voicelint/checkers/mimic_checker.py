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
            'Returns a non-unique constant.',
            "mimic-separated-strings",
            'All constants returned in a function should be unique.'
        ),
    }


    def visit_call(self,node):
    	# print("data")
    	# print(node.func.as_string())
    	if node.func.as_string()=="Mimic":
    		if not all(isinstance(x,astroid.nodes.Const) and x.pytype()=="builtins.str"
    				and len(x.value.strip().split())==1 for x in node.args):

    			self.add_message("mimic-separated-strings", node=node)
    