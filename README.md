# voicelint

`voicelint`  is a `pylint` plug-in/extension designed to aid users of [Caster](https://github.com/dictation-toolbox/Caster),a [dragonfly](https://github.com/dictation-toolbox/dragonfly) based toolkit for programming by voice, when writing their own grammars by catching some common or annoying mistakes. 

## Contents

<!-- MarkdownTOC  autolink="true" -->

- [Getting Started](#getting-started)
- [Currently Recognized Errors/Mistakes](#currently-recognized-errorsmistakes)
	- [Mimic Errors](#mimic-errors)
	- [Pause errors](#pause-errors)
	- [Forgeting Conditional Import](#forgeting-conditional-import)
	- [Various Rule Details Errors](#various-rule-details-errors)
	- [Key-Text-Mouse Separated strings Errors](#key-text-mouse-separated-strings-errors)
	- [BringApp and StartApp no dynamic strings](#bringapp-and-startapp-no-dynamic-strings)
- [License](#license)

<!-- /MarkdownTOC -->

## Getting Started

In case you have never heard before,[pylint](https://www.pylint.org/) is a popular static analysis tool, which can help you catch various errors and/or help you improve code quality. You can install it with `pip`

```python
python3 -m pip install pylint
```

and can be integrated with many editors via available extensions. For instance, you can follow instructions [here](https://code.visualstudio.com/docs/python/linting) for VSCode and for sublime you can use [SublimeLinter](https://packagecontrol.io/packages/SublimeLinter) in combination with [SublimeLinter-pylint](https://packagecontrol.io/packages/SublimeLinter-pylint)

Once you have done that, you need to install `voicelint` by similarly executing

```python
python37 -m pip install voicelint
```

and configure `pylint` to use this plug-in for our grammars!

Now the easiest way to configure `pylint` is via a `.pylintrc` file, which you should place in the root directory you interested in. For our use case, that is the rules folder of the caster user directory, so it should be something like

```
C:\Users\%USERNAME%\AppData\Local\caster\rules
```

if you're in the latest version of caster. To tell `pylint` to load our plug-in, we need to set the `load-plugins` setting, so our file should look something like

```python
[MASTER]
load-plugins=voicelint
```

Now we are goot and set with that,we are now faced with a different technicality that does not have to do with our plug-in but rather linting caster grammars in general. In particular, python allows manipulating during runtime  the set of directories it searches for modules import, which creates headaches for static analysis tools as they cannot know in advance which directories will be added or removed. Caster relies heavily on these feature and as a consequence pylint will complain about being unable to find the `castervoice` modules.

To sidestep this issue, we need to inform pylint of the directories Castor adds to the path and we can do that by adding the following lines (adjust for the paths used in your computer)

```
[MASTER]
init-hook='import sys; sys.path.append("C:\\Users\\%USERNAME%\\AppData\\Local\\caster\\rules"); sys.path.append("C:\\Users\\%USERNAME%\\Documents\\Github\\Caster")'

load-plugins=voicelint
```

and now you should be up and running!!! 


## Currently Recognized Errors/Mistakes

Not that many for the time being but I hope they help!

### Mimic Errors

```python
Mimic(["hello","world"]) # wrong
Mimic("hello world") # wrong

vs 

Mimic("hello","world") # `,` separated single words


Mimic(keyword_name_other_than_extra="something") # only allowed keyword is `extra` 
```

### Pause errors

```python
Pause(10) 

vs

Pause("10") # must be a string instead of integer 
```

### Forgeting Conditional Import

When importing support files, 99% of the time you should be using try except blocks to allow overriding from the user directory

```python
from castervoice.rules.apps.editor.eclipse_rules.eclipse_support import ec_con

vs

try: # Try first loading from caster user directory
    from eclipse_support import ec_con
except ImportError:    
    from castervoice.rules.apps.editor.eclipse_rules.eclipse_support import ec_con


```

### Various Rule Details Errors

for example

```python
class ExampleRule(MergeRule):
	blah,blah,blah


def get_rule():
	return ExampleRule,RuleDetails(ccrtype=CCRType.GLOBAL,executable="chrome")	

	vs 

	return ExampleRule,RuleDetails(ccrtype=CCRType.APP,executable="chrome")	
```

and many others for the current version of Caster (28/07/2020)


### Key-Text-Mouse Separated strings Errors

All the key presses should be in a single string

```python
Key("c-a","c-c")
Text("nice","day")
Mouse("[12,100]","(4,5)")
vs

Key("c-a,c-c")
Text("nice day")
Mouse("[12,100],(4,5)")
```

### BringApp and StartApp no dynamic strings

```python
BringApp("program","%(data)s")

vs 

Function(lambda data: BringApp('program',data.format()).execute())
```

## License

voicelint is licensed under 2-clause BSD 

```
BSD 2-Clause License

Copyright (c) 2020, Kitsios Panagiotis
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
