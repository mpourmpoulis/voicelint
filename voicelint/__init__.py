from voicelint.checkers import MimicChecker,ConditionalImportChecker



def register(linter):
	linter.register_checker(MimicChecker(linter))
	linter.register_checker(ConditionalImportChecker(linter))
