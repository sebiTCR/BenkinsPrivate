import subprocess


class Compiler:
    project_path = ''

    def __init__(self, path):
        self.project_path = path


    def setup(self):
        pass


    def compile(self):
        pass


class Meson(Compiler):
    def setup(self):
        subprocess.run(['meson', 'setup', f'{self.project_path}', f'{self.project_path}build'])


    def compile(self):
        subprocess.run(['meson', 'compile', '-C', f'{self.project_path}build'])
