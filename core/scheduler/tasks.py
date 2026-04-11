from builder.builder import Builder
from core import log
from core.fs import clone_repo
from core.scheduler.task import Task
from persistance.models import Project


class CloneTask(Task):
    path = None
    url = None

    def __init__(self, project):
        super().__init__(project)
        self.path = project.path
        self.url = project.repo


    def run(self):
        log.debug(f"Cloning {self.url} to {self.path}", file=__class__)
        clone_repo(self.url, self.path)


class SetupTask(Task):
    """
    Sets up a new project with the set compiler
    """
    path = None
    url = None

    def __init__(self, project):
        super().__init__(project)


    def run(self):
        Builder(self._project)


class CompileTask(Task):
    def __init__(self, project):
        super().__init__(project)


    def run(self):
        b = Builder(self._project)
        b.compile()