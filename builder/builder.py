import os.path
import subprocess

import builder.compilers as compilers
from builder.lexer import Lexer


class Builder:
    lexer = None
    compiler: compilers.Compiler = None
    _initialized: bool = False

    metadata: dict[str, str] = {
        "NAME": "My Project",
        "VERSION": "1.2.6",
        "PROJECT_TYPE": "NONE",
        "REPO": "https://your-repo.com/project.git",
    }

    def __init__(self, path):
        if(os.path.isfile(path + 'project.bk') == False):
            print(f"project.bk was not found in {path + 'project.bk'}")
            return

        self.metadata["PATH"] = path
        self.project_path = path
        self.lexer = Lexer(self.metadata)


    def compile(self):
        self.compiler.compile()


    def setup(self):
        self.lexer.parse_file()
        self.compiler = self._set_compiler(self.lexer.get_project_type(), self.project_path)
        self.compiler.setup()


    """
    Clones a github repo
    """
    def fetch(self, repo: str):
        subprocess.run(['git', 'clone', repo, self.project_path])

    """
    Selects the right compiler based on the PROJECT_TYPE variable
    :return Compiler object
    """
    def _set_compiler(self, project_type: str,  project_path: str) -> compilers.Compiler:
        c: compilers.Compiler = compilers.Compiler(project_path)
        project_type = project_type.upper()

        match project_type:
            case "MESON":
                c = compilers.Meson(project_path)
            case _:
                print(f'ERR: Unknown project type "{project_type}"!')
                print("Currently using the default compiler (that doesn't do any shit)")

        return c

