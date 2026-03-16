"""
Reads a construct.bk file and compiles the project accordingly to the instructions
"""
from enum import Enum
from builder.cmd import (cmd_set, cmd_get, cmd_project_type)


class Keywords(Enum):
    SET = 0,
    GET = 1,


class Lexer():
    data = 0

    def __init__(self, data):
        self.data = data


    """
    Reads a line and returns the according instruction
    """
    def run_command(self, line: str):
        keywords: list[str] = line.split(' ')
        instruction = keywords[0]
        keywords.pop(0)

        match instruction:
            case "SET":
                cmd_set(self.data, keywords)
            case "GET":
                cmd_get(self.data, keywords[0])
            case "PROJECT_TYPE":
                cmd_project_type(self.data, line)
            case _:
                print(f'Undefined command {instruction}')

        return keywords


    def parse_file(self):
        path = self.data['PATH']
        f = open(f'{path}/project.bk', 'r')
        for line in f:
            self.run_command(line)
        f.close()


    def get_project_type(self):
        return self.data["PROJECT_TYPE"]