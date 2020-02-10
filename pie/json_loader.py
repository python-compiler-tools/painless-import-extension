from pathlib import Path
from pie import LoaderForBetterLife, T
import json
import pickle


class JsonLoader(LoaderForBetterLife[dict]):
    def load_program(self, b: bytes) -> T:
        return pickle.loads(b)

    def dump_program(self, prog: T) -> bytes:
        return pickle.dumps(prog)

    def source_to_prog(self, src: bytes, path: Path) -> dict:
        return json.loads(src)

    def suffix(self) -> str:
        return '.json'
