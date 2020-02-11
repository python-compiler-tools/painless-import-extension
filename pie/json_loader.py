from importlib._bootstrap_external import _path_split
from pathlib import Path
from pie import LoaderForBetterLife
import json
import pickle

class JsonLoader(LoaderForBetterLife[dict]):
    def load_program(self, b: bytes):
        return pickle.loads(b)

    def dump_program(self, prog) -> bytes:
        return pickle.dumps(prog)

    def source_to_prog(self, src: bytes, path: Path) -> dict:
        return json.loads(src)

    def suffix(self) -> str:
        return '.json'
