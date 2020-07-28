import re
import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


from voicelint.utility import apply_id




@apply_id
class PauseChecker(BaseChecker):
    __implements__ = IAstroidChecker
    name = 'pause-checker'
    priority = -1
    msgs = {
        "E09":(
            "The time you want to pause should be specified in a string format" + 
            "For example instead of using `Pause(10)` you should be using `Pause('10')`!" + 
            "Additionally, if you want the time to depend on one of the extras spoken in utterance" + 
            "eg `sleep_time` you can do `Pause('%(sleep_time)d')`" + 
            "Please also note that the amount specified is in hundredths of a second so 10 = 100ms",
            
            'pause-requires-string',
            ""
        )
    }

    def visit_call(self,node):
        if node.func.as_string()=="Pause":
            if any(x for x in node.args if isinstance(x,astroid.Const) and x.pytype() != "builtins.str"):
                self.add_message("pause-requires-string", node=node)






        


