from git import TagReference

from builder.builder import Builder
from core import log
from core.fs import clone_repo, get_latest_tag
from core.scheduler.task import Task
from web.controllers import project_controller


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
        project_controller.set_latest_version(self._project.id, get_latest_tag(self.path))


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


class BuildTask(Task):
    def __init__(self, project):
        super().__init__(project)


    def run(self):
        project_controller.set_project_build_status(self._project.id, 2)
        b = Builder(self._project)
        status, log =  b.compile()

        if status:
            tag: TagReference = get_latest_tag(self._project.path)
            project_controller.set_project_build_status(self._project.id, 3)
            project_controller.set_latest_version(self._project.id, tag.name)
            return
        project_controller.set_project_build_status(self._project.id, 1)


