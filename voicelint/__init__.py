from voicelint.checkers import MimicChecker,ConditionalImportChecker,RuleDetailsChecker



def register(linter):
	linter.register_checker(MimicChecker(linter))
	linter.register_checker(ConditionalImportChecker(linter))
	linter.register_checker(RuleDetailsChecker(linter))
