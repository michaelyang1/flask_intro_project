from enum import IntEnum
import datetime
from typing import List, Dict
from dataclasses import dataclass
# enum for project status

class Status(IntEnum):
    ACTIVE, INACTIVE, COMPLETE = 1, 2, 3

# class for Task table
@dataclass
class Task:
    id: str
    name: str 
    date_created: datetime.date
    status: Status
    date_completed: datetime.date

# class for Project table
@dataclass
class Project:
    id: str
    name: str
    description: str
    pm_email: str
    date_created: datetime.date
    status: Status
    date_completed: datetime.date or None
    tasks: List[Task]

class Database:
    project_map: Dict[str, Project]

    def __init__(self):
        self.project_map = {}

    def add_project(self, project: Project):
        self.project_map[project.id] = project

    def get_project(self, project_id: str):
        
        return self.project_map[project_id]

    def get_all_projects(self):
        return list(self.project_map.values())

    def update_project(self, project_id: str, project: Project):
        self.project_map[project_id] = project

    def delete_project(self, project_id: str):
        del self.project_map[project_id]
