from voicelint.checkers import MimicChecker



def register(linter):
	linter.register_checker(MimicChecker(linter))
