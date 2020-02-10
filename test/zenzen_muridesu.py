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
