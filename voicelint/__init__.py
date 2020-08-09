from voicelint.checkers import (
	MimicChecker,ConditionalImportChecker,RuleDetailsChecker,PauseChecker,KeyChecker
)



def register(linter):
	linter.register_checker(MimicChecker(linter))
	linter.register_checker(ConditionalImportChecker(linter))
	linter.register_checker(RuleDetailsChecker(linter))
	linter.register_checker(PauseChecker(linter))
	linter.register_checker(KeyChecker(linter))
