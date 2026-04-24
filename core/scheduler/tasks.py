import os.path
from zipfile import ZipFile
from glob import glob

from git import TagReference

from builder.builder import Builder
from core import log
from core.fs import clone_repo, get_latest_tag
from core.scheduler.scheduler import get_scheduler
from core.scheduler.task import Task
from web.controllers import project_controller, build_controller


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
        project_controller.set_latest_version(self._project.id, get_latest_tag(self.path).name)


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


    #TODO: Return the log to the HTTP request
    def run(self):
        project_controller.set_project_build_status(self._project.id, 2)
        build_path = f"{os.getenv("BUILD_PATH")}/{self._project.name}"
        b = Builder(self._project)
        status, log =  b.compile()

        if status:
            tag: TagReference = get_latest_tag(self._project.path)
            project_controller.set_project_build_status(self._project.id, 3)
            project_controller.set_latest_version(self._project.id, tag.name)
            get_scheduler().register_task(PackageTask(self._project))
            build_controller.create_new_build(self._project, version=tag.name, path = f"{build_path}/{tag.name}.zip", logs=log)
            return
        project_controller.set_project_build_status(self._project.id, 1)


class PackageTask(Task):
    def __init__(self, project):
        super().__init__(project)

    def run(self):
        build_path = f"{os.getenv("BUILD_PATH")}/{self._project.name}"
        log.debug(f"Packaging build: {build_path}")
        if not os.path.exists(build_path):
            os.mkdir(build_path)
        with ZipFile(f'{build_path}/{self._project.version}.zip', 'w') as z:
            for f in glob(f"{self._project.path}/build/*"):
                z.write(f)
