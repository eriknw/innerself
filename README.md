# Innerself

[![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%20PyPy-blue)](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%20PyPy-blue)
[![Version](https://img.shields.io/pypi/v/innerself.svg)](https://pypi.org/project/innerself/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/eriknw/innerself/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/eriknw/innerself.svg?branch=master)](https://travis-ci.org/eriknw/innerself)
[![Coverage Status](https://coveralls.io/repos/eriknw/innerself/badge.svg?branch=master)](https://coveralls.io/r/eriknw/innerself)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

```python
class Zen:
    @innerself
    def __init__(self, the, path, to, enlightenment):
        your_innerself = f'is {the} {path} {to} {enlightenment}'

    @innerself(readonly=True)
    def chaos(self, dont, let, the, anger, and_chaos, control, you):
         return f'{you} {control} your own {path} {to} {enlightenment}'

>>> zen = Zen('the', 'path', 'to', 'enlightenment')
>>> zen.your_innerself
'is the path to enlightenment'

>>> zen.chaos("don't", 'let', 'the', 'anger', 'and chaos', 'control', 'you')
'you control your own path to enlightenment'

>>> hasattr(zen, 'enlightenment')
True

>>> hasattr(zen, 'anger')
False
```
**To install:** `pip install innerself`
