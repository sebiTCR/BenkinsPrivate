import json
import os
import subprocess

from core import log
from web.controllers import project_controller


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



class KicadCompiler(Compiler):
    _project_path = ''

    def __init__(self, path):
        self._project_path = path


    def setup(self):
        if not os.path.exists(f"{self._project_path}/build"):
            os.mkdir(f"{self._project_path}/build")
        self._run_drc_checks()


    def compile(self) -> (bool, list):
        status, violations = self._run_drc_checks()
        if status:
           return (status, violations)
        self._export()
        return (status, violations)


    def _get_kicad_specific_file(self, suffix: str) -> str:
        pcb = None

        for f in os.listdir(self._project_path):
            ext = f.split(".")[-1]
            if ext == suffix:
                pcb = f
        if pcb is None:
            log.error(f"No *.{suffix} file was found in {self._project_path}!")
            return ""
        return f"{self._project_path}/{pcb}"


    def _run_drc_checks(self) -> (bool, list):
        subprocess.run(['kicad-cli', 'pcb', 'drc', '-o', f'{self._project_path}/drc.json', '--format', 'json', self._get_kicad_specific_file("kicad_pcb")])
        data: dict = None

        with open(f"{self._project_path}/drc.json") as f:
            data = json.loads(f.read())

        for violation in data["violations"]:
            if violation["severity"] == "error":
                log.error("Found violations in PCB!")
                return (False, data["violations"])
        return (True, data["violations"])


    def _export(self):
        subprocess.run(['kicad-cli', 'pcb', 'export', 'gerbers', '--output', f'{self._project_path}/build', self._get_kicad_specific_file("kicad_pcb")])
