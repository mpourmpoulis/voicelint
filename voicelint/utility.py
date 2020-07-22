PACKAGE_ID = str(98)

def apply_id(checker):
	checker.msgs = {k[0] + PACKAGE_ID + k[1:]:v for k,v in checker.msgs.items()}
	return checker	