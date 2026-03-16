import subprocess
from builder.compilers.compiler import Compiler


class MesonCompiler(Compiler):
    _project_path = ''

    def __init__(self, path):
        self._project_path = path


    def setup(self):
        subprocess.run(['meson', 'compile', '-c', f'{self._project_path}build'])


    def compile(self):
        subprocess.run(['meson', 'setup', f'{self._project_path}', f'{self._project_path}build'])