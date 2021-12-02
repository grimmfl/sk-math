import os
import sys
from string import digits
from typing import Dict

from compiler.executer import Executer
from compiler.top_down_parser import TopDownParser
from editor import Editor

VALID_INPUTS = digits + "*/+-^. "


def show_help():
    print("-f <FILEPATH> | Execute file")
    print("-h            | Help")


def config() -> Dict:
    switch = {
        "-f": None,
        "-h": show_help,
    }
    for i in range(1, len(sys.argv)):
        if sys.argv[i] in switch.keys():
            if switch[sys.argv[i]] is None:
                switch[sys.argv[i]] = sys.argv[i + 1]
            else:
                switch[sys.argv[i]]()
    return switch


def file_to_text(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def run(text: str, parser: TopDownParser, executer: Executer):
    parsed = parser.parse(text)
    executer.execute(parsed)


if __name__ == "__main__":
    if "--dev" not in sys.argv:
        sys.tracebacklimit = 0
    p = TopDownParser()
    e = Executer()
    c: Dict = config()
    if c["-f"] is not None:
        if not(c["-f"].endswith(".skm")):
            raise Exception("File needs to have .skm ending.")
        code = file_to_text(c["-f"])
        run(code, p, e)
    else:
        while True:
            editor = Editor()
            code = editor.text
            os.system("cls")
            print(code)
            print("\n>> ", end="")
            run(code, p, e)
            input("\nEnter    Write new code")
