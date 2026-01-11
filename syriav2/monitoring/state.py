from abc import ABC, abstractmethod
from .models import ProjectStageUpdate
from projects.models import Project

class ProjectStageState(ABC):
    @abstractmethod
    def handle(self, update: ProjectStageUpdate):
        pass

class StageOneState(ProjectStageState):
    def handle(self, update):
        update.project.status = 'in_progress'
        update.project.save()

class StageSevenState(ProjectStageState):
    def handle(self, update):
        update.project.status = 'completed'
        update.project.is_cancelled = False
        update.project.save()


class StageStateFactory:
    @staticmethod
    def get_state(stage_number):
        if stage_number == 7:
            return StageSevenState()
        else:
            return StageOneState()  
