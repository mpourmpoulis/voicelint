import re
import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id

message = '''
If you are seeing these error message, then you are probably trying to import data
From a support file in a way that does not take into account that support files can 
be overwritten from the user directory. 

The proper way to import from support files is to use a try except construction,
so that the growler first attempts to load from the user directory and if support file
is not there, we fall back into caster proper!

for instance suppose that you need something from alphabet support and 

try :
    from castervoice.rules.core.alphabet_rules.alphabet_support import something
except ImportError:
    from alphabet_rules.alphabet_support import something
'''
message = " ".join(message.splitlines())

@apply_id
class ConditionalImportChecker(BaseChecker):
    __implements__ = IAstroidChecker
    pattern  = re.compile(r"castervoice\.rules\.(apps|ccr|core)\.(.*)")
    name = 'conditional-import-checker'
    priority = -1
    msgs = {
        'E04': (
            message,
            "no-conditional-import",
            ""
        ),

    }

    def visit_importfrom(self,node):
        if node.modname:
            m = ConditionalImportChecker.pattern.match(node.modname)
            if m:
                if not isinstance(node.parent,astroid.ExceptHandler):
                    self.add_message("no-conditional-import",node=node)
                elif not node.parent.body or node not in node.parent.body:
                    self.add_message("no-conditional-import",node=node)



        


