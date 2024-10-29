# sacr-parser

## Installation

```
pip install git+https://github.com/naitian/sacr-parser
```

## Usage

```py
from sacr_parser.parser import parse

text = '{person:name="Alice" Hello {animal:type="Cat" Friendly!}} some extra text'
annotations = parse(text)
```