## PIE

[![PyPI version](https://img.shields.io/pypi/v/painless-import-extension.svg)](https://pypi.org/project/painless-import-extension)
[![Build Status](https://travis-ci.com/thautwarm/PIE.svg?branch=master)](https://travis-ci.com/thautwarm/PIE)
[![codecov](https://codecov.io/gh/thautwarm/PIE/branch/master/graph/badge.svg)](https://codecov.io/gh/thautwarm/PIE)
[![MIT License](https://img.shields.io/badge/license-MIT-Green.svg?style=flat)](https://github.com/thautwarm/EBNFParser/blob/boating-new/LICENSE)


## Installation & Documentation

`pip install painless-import-extension`.

Basically there's only one thing exported from package `pie`:

```python
from pie import LoaderForBetterLife
```

It's an abstract generic type. When you want to load a file to type `A`,
write such a loader:

```python
class ALoader(LoaderForBetterLife[A]):
    pass
```

**IDEs and static type checkers will help you to finish the following steps of implementing your expecting loader, and this is what I'd call a documentation here.**


### Motivation

Fuck it, I must say something at first.

Once you use the Python import hooks to support files with extensions other than '.py',
you will feel extremely disgusting, and if you're expert enough to use Python internal stuffs
to track the implementation of `PathFinder.find_spec`(usually `sys.meta_path[2].find_spec` or  `sys.meta_path[1].find_spec`),
the awfulness of the module finding mechanism will lead you to a strong suspicion of the reliability of Python `import` statements,
and finally, likely to bring about the crash of one's faith in writing reliable codes.

I for one encountered this, and fortunately I didn't jump down from my dormitory after working with that for months(and knew it for years).

Hence, I realized that it should be my duty to keep people away from being killed when working with Python's module finding mechanism,
which might save several people's lives.


### What is PIE?

PIE, aka **painless-import-extension**, is not aimed at providing a higher level interface of Python's
import system, but is actually useful for solving most of the related problems.

Technically, PIE "did nothing", all the codes involved in this project are so far pretty easy,
that even a newbie to Python could understand it thoroughly with any question. However,
PIE is useful, because it shows a **healthy mental model** for using Python import system,
in a simplest way, and also a most practical way if you want to use the same module file search strategy of Python's.

For instance, if you want to import `data.json` via PIE, other than the JSON file,
you should also prepare a file with just suffix changed to `.py`(hence you got `data.py`), and
fill the following contents:

```python
from pie.json_loader import JsonLoader

data = JsonLoader(__file__, __name__).load()
```

where, `JsonLoader(__file__, __name__).load()` will load the JSON data.

Looks trivial? Yes, that's expected, and I'm telling you that this way is powerful,
and subtly, much more powerful than `json.load(pathlib.Path(__file__).with_suffix('.json').open())`.

### A PIE loader, and what happened when invoking `LoaderForBetterLife.load()`?

Given such a file directory:

```
- proj
    - data.json
    - data.py
```

And we fill `data.py` with 

```python
from pie.json_loader import JsonLoader

data = JsonLoader(__file__, __name__).load()
```

Next, when you're import `proj.data`,

- for the first time,
  things similar to `json.load` happened, JSON is loaded from `data.json`.
  However, a default caching system is introduced, and when you exit
  current Python interpreter, and reopen the interpreter to import
  `proj.data`

- for the second time, `json.load` might not be invoked.
    There're some cases:
    - when `proj/data.json` doesn't exist, we'll get the JSON
      from a binary file cached on disk.
    - when `proj/data.json` exists, we'll check if the content
      of `proj/data.json` has changed. If true, we import `proj/data.json`
      just as what we did at the first time; otherwise, we use the cached
      binary contents.

Things become quite useful when you're loading DSLs(domain specific languages),
or other programming languages that compile to the Python.

For example, we give an implementation of loading the script of [muridesu](https://github.com/LanguageAsGarbage/muridesu-lang) language(Python 3.7 only).

Check `test/zenzen_muridesu.py`, note that if you're using an IDE,
you will have a good experience of auto completion and static checking
due to our thorough support of Python type hints.

```python
from pathlib import Path
from typing import Union, Tuple
from muridesu.parse_stmts import parse_stmts as parse
from pie import LoaderForBetterLife
from types import CodeType
import marshal


class MuridesuLoader(LoaderForBetterLife[CodeType]):
    def source_to_prog(self, src: bytes, path: Path):
        mod = parse(src.decode('utf8'), str(path.absolute()))
        code = compile(mod, self.file.with_suffix(self.suffix()), 'exec')
        return code

    def load_program(self, b: bytes):
        return marshal.loads(b)

    def dump_program(self, prog: CodeType):
        return marshal.dumps(prog)

    def suffix(self) -> Union[str, Tuple[str, ...]]:
        return '.muridesu'


exec(MuridesuLoader(__file__, __name__).load(), globals())
```

In `test/zenzen_muridesu.muridesu`, write down
```
class Animal {
    func bark(self){
        print("hoho")
    }
}

class Dog <: Animal {
    bark = fn (self) -> {
        print("dogy")
    }
}

list(
    map(
        fn (it) -> {
            print(it.__class__)
            it.bark()
        },
        [Dog(), Animal()]
    )
)
```

Importing `test/zenzen_muridesu.py` will give following STD output:

```
<class '__main__.Dog'>
dogy
<class '__main__.Animal'>
hoho
```

### Conclusion

Make sure if you really want to introduce the complexity of `importlib`?

When you just need searching extension files just as searching normal python files,
use PIE.
