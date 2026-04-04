import os.path
import subprocess

import builder.compilers as compilers
import core.fs
from builder.lexer import Lexer
from core import log, fs
from persistance.models import Project


class Builder:
    """
    Builder class. Configures a project from the *project.bk* file. Contains a lexer that parses the config file, storing
    the settings inside the database for late use.
    """

    compiler: compilers.Compiler = None
    _project: Project = None
    _initialized: bool = False


    def __init__(self, project: Project):
        """
        Initialize the builder in an existing repository.
        :param path: Repository path. Make sure the path ends with "/".
        """
        path = project.path

        if os.path.exists(path):
            fs.clone_repo(project.repo)
        if(os.path.isfile(path + 'project.bk') == False):
            log.fatal(f"project.bk was not found in {path + 'project.bk'}")
            return

        self._project = project
        self.compiler = self._set_compiler(project.type, path)
        self.compiler.setup()


    def compile(self):
        self.compiler.compile()


    def fetch(self, repo: str):
        """
        Checks a repo for updates
        .. deprecated:: 1.0.0
        :param repo: Repo URL
        """
        fs.clone_repo(self._project.repo, self._project.path)


    def _set_compiler(self, project_type: str,  project_path: str) -> compilers.Compiler:
        """
        Selects the right compiler based on the PROJECT_TYPE variable
        :param project_type
        :param project_path
        :return: Compiler object
        """
        c: compilers.Compiler = compilers.Compiler(project_path)
        project_type = project_type.upper()

        match project_type:
            case "MESON":
                c = compilers.Meson(project_path)
            case _:
                print(f'ERR: Unknown project type "{project_type}"!')
                print("Currently using the default compiler (that doesn't do any shit)")

        return c