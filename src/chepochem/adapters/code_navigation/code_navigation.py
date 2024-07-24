from abc import ABC, abstractmethod
from pathlib import Path

from attr import frozen

from chepochem.models.position import Position


@frozen(slots=True)
class Definition(ABC):
    file: Path
    position: Position

    @property
    @abstractmethod
    def start_position(self) -> Position:
        """Get start position of the definition in the file"""

    @property
    @abstractmethod
    def end_position(self) -> Position:
        """Get end position of the definition in the file"""


class CodeNavigation(ABC):
    @classmethod
    @abstractmethod
    def load_project(cls, project: Path):
        """Loading project from path

        Args:
            project (Path): path to project
        """

    @abstractmethod
    def get_definitions(self, file: Path) -> list[Definition]:
        """Load all definitions from file in the current project

        Args:
            file (Path): path to file with code
        """

    @abstractmethod
    def get_references(self, file: Path, position: Position) -> list[Definition]:
        """Load all references to the definition in the project

        Args:
            file (Path): path to file with code
            position (Position): position of the definition in the file

        Returns:
            list[Definition]: list of references
        """
